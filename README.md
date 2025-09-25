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

## ▶️ Running the Application

1. Clone this repository and enter the folder:

   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/rubixe.git
   cd rubixe
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
