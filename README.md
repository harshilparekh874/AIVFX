# AIVFX - Production AI Video & VFX Pipeline

A modular, scalable, and GPU-ready system for generating AI videos and extracting structured VFX layers (Foreground, Background, Depth, Segmentation, Optical Flow).

## 🚀 Features
- **AI Video Generation**: Stable Video Diffusion / ModelScope integration.
- **Layer Separation**: SAM-based foreground extraction with alpha masks.
- **Depth Estimation**: MiDaS DPT Large for high-resolution depth maps.
- **Motion Analysis**: Optical flow vector extraction for compositing.
- **Asset Packaging**: Automated metadata generation and production-ready zip bundles.
- **Modern UI**: Next.js 14 dashboard with real-time job tracking.

## 🏗️ Architecture
- **Frontend**: Next.js, tailwindcss, Framer Motion.
- **Backend**: FastAPI (Python 3.11), Celery, Redis.
- **Worker**: GPU-accelerated background processing.
- **Storage**: Filesystem-based job tracking.

## 🛠️ Setup

### Prerequisites
- Docker & Docker Compose
- NVIDIA GPU with [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) (for GPU acceleration)

### Run with Docker
```bash
# Clone the repository
git clone https://github.com/yourusername/AIVFX.git
cd AIVFX

# Start the environment
docker-compose up --build
```

### Local Backend Setup (No Docker)
1. **Redis**: Ensure Redis is running on `localhost:6379/0`.
2. **Backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate # or venv\Scripts\activate
   pip install -r requirements.txt
   python app/main.py
   ```
3. **Worker**:
   ```bash
   cd backend
   celery -A app.workers.celery_app worker --loglevel=info
   ```

## 📂 Project Structure
- `/backend`: FastAPI application and ML services.
- `/frontend`: Next.js dashboard.
- `/jobs`: Job metadata and transient files.
- `/outputs`: Final processed assets and bundles.

## 🧠 Scaling Strategy
- **Worker Horizontal Scaling**: Spin up multiple Celery workers across different GPU nodes.
- **Model Microservices**: Separate individual ML models into their own containers if needed for fine-grained resource allocation.
- **S3 Storage**: Swap the filesystem storage for AWS S3 or MinIO for multi-node deployments.

## Work In Progress

## ⚖️ License
MIT
