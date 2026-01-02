# 🎬 AI Video Segmenter

A lightning-fast, web-based video segmentation tool powered by **YOLOv8** and **FastAPI**. hosted on **Hugging Face Spaces (ZeroGPU)** and **Vercel**.

## 🚀 Live Demo
- **Frontend:** [Link to your Vercel App]
- **Backend API:** [Link to your Hugging Face Space]

## 🛠️ Tech Stack
- **Frontend:** React.js (Vite), CSS Modules
- **Backend:** Python, FastAPI, OpenCV, PyTorch
- **AI Model:** YOLOv8-Small (Segmentation)
- **Infrastructure:** Docker, Hugging Face Spaces (GPU), Vercel

## ✨ Features
- **GPU-Accelerated:** Utilizes Hugging Face ZeroGPU for fast inference.
- **End-to-End Pipeline:** Drag-and-drop UI -> Compressed Upload -> AI Processing -> WebM Streaming.
- **Smart Resizing:** Automatically downscales 4K/1080p video to 720p for optimal web performance.
- **Cross-Platform:** Works on mobile and desktop browsers (WebM VP9 codec).

## ⚙️ Local Installation
1. Clone the repo
2. Backend: `pip install -r requirements.txt` then `uvicorn main:app`
3. Frontend: `npm install` then `npm run dev`
