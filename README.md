# 📁 File Sharing App

A minimal file sharing app built with **FastAPI** and **React (Vite)**, containerized using **Docker** and deployed with **Kubernetes**.

---

## ⚙️ Features

### 🚀 Backend (FastAPI)
- File Upload API with:
  - ✅ **UUID-based** storage
  - 📏 **Size limit** (10 MB)
  - ⏱️ **Rate limiting** (per IP)
  - 🧹 **Automatic cleanup** of expired files
- Download API via UUID
- Health check endpoint (`/status`)
- Integrated **logging**

### 🖥️ Frontend (React + Vite)
- Simple UI to upload and download files
- UUID displayed after upload
- Handles errors and download fallback gracefully

### ☸️ DevOps
- 📦 Dockerized (both frontend and backend)
- 🧩 Kubernetes deployment
- 🛡️ **Ingress with DNS routing**
- 🖧 Backend and frontend exposed via **custom DNS names**
- 🔒 Uses internal DNS (ClusterIP) for service-to-service communication

---

## 🛠️ Tech Stack
- **Backend**: FastAPI
- **Frontend**: React + Vite
- **Containerization**: Docker
- **Orchestration**: Kubernetes (with Traefik or NGINX Ingress)
- **Platform**: WSL2 (Linux-based)

---

## 🌐 Custom DNS
You can access the services using custom domain names via your ingress configuration:
- Frontend: `http://frontend.app.fastapi`
- Backend: `http://backend.app.fastapi`

Make sure these are mapped in your host system (e.g., `/etc/hosts` on Linux or `C:\Windows\System32\drivers\etc\hosts` on Windows).

---


