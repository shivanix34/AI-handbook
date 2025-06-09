from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
import pathlib
import threading

from backend.main_leadgen import run_full_leadgen_batch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = pathlib.Path(__file__).parent.resolve()
UPLOAD_DIR = BASE_DIR / "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Global dictionaries for progress and file paths
task_progress = {}
task_files = {}

@app.get("/")
def root():
    return {"message": "B2B Lead Enrichment API is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is healthy"}

def background_process(task_id: str, input_path: pathlib.Path, output_path: pathlib.Path):
    try:
        def progress_callback(percent):
            task_progress[task_id] = percent
        
        run_full_leadgen_batch(str(input_path), str(output_path), chunksize=100, progress_callback=progress_callback)

        task_progress[task_id] = 100
        task_files[task_id] = str(output_path)

        # Remove input file after processing
        if input_path.exists():
            input_path.unlink()

    except Exception as e:
        task_progress[task_id] = -1  # indicate error
        print(f"Error processing task {task_id}: {e}")

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    task_id = uuid.uuid4().hex
    input_path = UPLOAD_DIR / f"temp_{task_id}.csv"
    output_path = UPLOAD_DIR / f"output_{task_id}.csv"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task_progress[task_id] = 0

    # Run the processing in a separate thread to avoid blocking
    threading.Thread(target=background_process, args=(task_id, input_path, output_path), daemon=True).start()

    return {"task_id": task_id}

@app.get("/progress/{task_id}")
def get_progress(task_id: str):
    if task_id not in task_progress:
        return JSONResponse(status_code=404, content={"error": "Invalid task ID"})
    percent = task_progress[task_id]
    if percent == -1:
        return JSONResponse(status_code=500, content={"error": "Processing failed"})
    return {"percentage": percent}

@app.get("/download/{task_id}")
def download_result(task_id: str):
    if task_id not in task_files:
        return JSONResponse(status_code=404, content={"error": "Result not ready or invalid task ID"})
    file_path = pathlib.Path(task_files[task_id])
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(str(file_path), media_type="text/csv", filename="final_enriched_leads.csv")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
