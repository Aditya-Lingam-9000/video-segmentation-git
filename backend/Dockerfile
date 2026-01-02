# 1. Use an official lightweight Python image
FROM python:3.9-slim

# 2. Set the working directory inside the server
WORKDIR /app

# 3. Install system dependencies required for OpenCV
# (Cloud servers are empty, so we must install these video tools manually)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy your requirements file
COPY requirements.txt .

# 5. Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your backend code
COPY . .

# 7. Create a temp folder for video processing with write permissions
RUN mkdir -p temp && chmod 777 temp

# 8. Start the server (Hugging Face uses port 7860 by default)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]