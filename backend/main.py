from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
from main_leadgen import run_full_leadgen_batch

app = FastAPI()

origins = [
    "http://localhost:3000",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "../data"  # Make sure this folder exists in your project root
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "B2B Lead Enrichment API is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is healthy"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    input_path = os.path.join(UPLOAD_DIR, f"temp_{uuid.uuid4().hex}.csv")
    output_path = os.path.join(UPLOAD_DIR, f"output_{uuid.uuid4().hex}.csv")

    # Save uploaded file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run your processing function
    run_full_leadgen_batch(input_path, output_path, chunksize=100)

    # Schedule cleanup of temp files after response
    def cleanup_files():
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except Exception as e:
            print(f"Cleanup error: {e}")

    if background_tasks:
        background_tasks.add_task(cleanup_files)

    # Return the output CSV file as response
    return FileResponse(output_path, media_type='text/csv', filename='final_enriched_leads.csv')
