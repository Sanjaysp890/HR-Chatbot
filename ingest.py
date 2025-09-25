from pathlib import Path
import pickle
from sentence_transformers import SentenceTransformer
import faiss
from PyPDF2 import PdfReader

DATA_DIR = Path("data")
INDEX_DIR = Path("vectorstore")
INDEX_DIR.mkdir(exist_ok=True)

EMBED_MODEL = "all-MiniLM-L6-v2"

def read_pdf(path:Path):
    reader = PdfReader(path)
    texts = []
    for p in reader.pages:
        txt = p.extract_text()
        if txt:
            texts.append(txt)
    return "\n".join(texts)

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    i=0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def main(data_folder="data"):
    model = SentenceTransformer(EMBED_MODEL)
    docs = []
    for f in Path(data_folder).iterdir():
        if f.suffix.lower()==".pdf":
            txt = read_pdf(f)
            docs.append((f.name, txt))
    all_texts=[]
    for name, txt in docs:
        chunks = chunk_text(txt)
        for c in chunks:
            all_texts.append({"source":name, "text":c})
    texts = [t["text"] for t in all_texts]
    print(f"Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_DIR/"faiss.index"))
    with open(INDEX_DIR/"meta.pkl","wb") as f:
        pickle.dump(all_texts,f)
    print("Saved index and metadata to", INDEX_DIR)

if __name__=="__main__":
    main("data")
