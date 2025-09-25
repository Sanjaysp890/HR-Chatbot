# 🚀 RAG HR Chatbot (Rubixe)

This project is a **Retrieval-Augmented Generation (RAG) HR Chatbot** containerized with Docker.  
It uses **FastAPI** as the backend (API) and **Streamlit** as the frontend (UI).  

---

## 📦 Docker Hub Repository (Single Repo with Tags)

All images are hosted in one Docker Hub repo:  
👉 https://hub.docker.com/r/sanjay1233/rubixe

Available tags:
- **Backend** → `sanjay1233/rubixe:backend`
- **Frontend** → `sanjay1233/rubixe:frontend`

---

## ⚙️ Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed  
- [Docker Compose](https://docs.docker.com/compose/install/) installed  
- `.env` file with your API keys  

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## ▶️ Running with Docker

1. Clone this repository and enter the folder:

   ```bash
   git clone https://github.com/Sanjaysp890/HR-Chatbot.git
   cd HR-Chatbot
   ```

2. Pull the images:

   ```bash
   docker compose pull
   ```

3. Start the containers:

   ```bash
   docker compose up -d
   ```

---

## ▶️ Running Locally (without Docker)

You can also run the chatbot locally using **Conda** or Python virtual environments.

### 1. Clone the repo
```bash
git clone https://github.com/Sanjaysp890/HR-Chatbot.git
cd HR-Chatbot
```

### 2. Create environment (Conda)
```bash
conda create -n ragchat python=3.11 -y
conda activate ragchat
```

*(or using `venv` if not using Conda)*  
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/Mac
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements_heavy.txt
```

### 4. Set environment variables
Create a `.env` file (based on `.env.example`) and add your keys:
```env
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DOCS_DIR=./docs
```

### 5. Start backend (FastAPI)
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Backend runs on:  
👉 http://localhost:8000/health  
👉 http://localhost:8000/docs  

### 6. Start frontend (Streamlit)
Open a new terminal (with env activated):
```bash
streamlit run ui_streamlit.py --server.port=8501
```

Frontend runs on:  
👉 http://localhost:8501  

---

## 🌐 Access the Services

- **Frontend (Streamlit UI)** → http://localhost:8501  
- **Backend Healthcheck** → http://localhost:8000/health  
- **Backend API Docs (Swagger UI)** → http://localhost:8000/docs

---

## 🛠️ Development Notes

- Backend uses **FastAPI** (`/query` endpoint).  
- Frontend uses **Streamlit** for the chatbot UI.  
- Healthchecks ensure services auto-restart if unhealthy.  
- Data (docs, vectorstore, uploads) persists via mounted volumes.  

---

## 📜 License

This project is for **internship assessment/demo purposes**.
