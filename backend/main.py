from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
import pathlib

from main_leadgen import run_full_leadgen_batch

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = pathlib.Path(__file__).parent.resolve()
UPLOAD_DIR = BASE_DIR / "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "B2B Lead Enrichment API is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is healthy"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    input_path = UPLOAD_DIR / f"temp_{uuid.uuid4().hex}.csv"
    output_path = UPLOAD_DIR / f"output_{uuid.uuid4().hex}.csv"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        run_full_leadgen_batch(str(input_path), str(output_path), chunksize=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")

    def cleanup_files():
        try:
            if input_path.exists():
                input_path.unlink()
            if output_path.exists():
                output_path.unlink()
        except Exception as e:
            print(f"Cleanup error: {e}")

    background_tasks.add_task(cleanup_files)

    return FileResponse(str(output_path), media_type='text/csv', filename='final_enriched_leads.csv')

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
