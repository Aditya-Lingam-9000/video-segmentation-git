import os
import shutil
import cv2
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO

# --- SMART IMPORT FOR GPU ---
try:
    import spaces
    print("Combined: Running in Cloud (GPU Enabled)")
except ImportError:
    print("Combined: Running Locally (CPU Only)")
    class spaces:
        @staticmethod
        def GPU(func):
            return func
# ----------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use 'Small' model
print("Loading AI Model...")
model = YOLO('yolov8n-seg.pt') 
print("Model Loaded!")

@app.post("/segment")
@spaces.GPU
async def process_video(file: UploadFile = File(...)):
    # 1. Save Input
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    shutil.copyfileobj(file.file, temp_input)
    temp_input.close()
    
    # 2. Prepare Output
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
    output_path = temp_output.name
    temp_output.close()

    try:
        # 3. Open Video
        cap = cv2.VideoCapture(temp_input.name)
        if not cap.isOpened():
            raise ValueError("Could not open uploaded video.")

        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

        # RESIZE LOGIC (To 720p for speed)
        target_width = 1280
        target_height = 720
        
        if original_width > 1280:
            width = target_width
            height = target_height
        else:
            width = original_width
            height = original_height

        # FIX 1: CHANGE CODEC TO VP9 (Better compatibility)
        fourcc = cv2.VideoWriter_fourcc(*'vp09') 
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Fallback if VP9 fails initialization
        if not out.isOpened():
            print("VP9 failed, falling back to mp4v")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if original_width > 1280:
                frame = cv2.resize(frame, (width, height))
            
            # FIX 2: MOVED 'retina_masks=False' TO HERE
            results = model(frame, stream=True, retina_masks=False)
            
            for result in results:
                # FIX 3: REMOVED ARGUMENT FROM PLOT()
                annotated_frame = result.plot()
                out.write(annotated_frame)

    except Exception as e:
        print(f"Error processing video: {e}")
        return {"error": str(e)}

    finally:
        cap.release()
        if 'out' in locals(): out.release()
        if os.path.exists(temp_input.name): os.remove(temp_input.name)

    return FileResponse(output_path, media_type="video/webm", filename="segmented.webm")