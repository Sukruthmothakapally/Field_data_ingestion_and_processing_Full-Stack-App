from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import FileResponse
from inducedpolarization.survey import InducedPolarizationSurvey
from server.schemas import UploadResponse
import os

app = FastAPI()

os.makedirs("data", exist_ok=True)
@app.post("/upload/", response_model=UploadResponse)
async def upload_dataset(name: str = Form(...), date: str = Form(...), file: UploadFile = File(...)):
    file_location = f"data/{file.filename}"

    # ✅ Check file size safely
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)

    if size > 1 * 1024 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds 1GB limit.")

    # ✅ Write file in chunks
    with open(file_location, "wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            buffer.write(chunk)

    try:
        survey = InducedPolarizationSurvey.from_file(file_location)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    df = survey.data
    num_rows = len(df)
    columns = list(df.columns)

    return {
        "filename": file.filename,
        "name": name,
        "date": date,
        "status": "Success",
        "rows": num_rows,
        "line_count": df["Line"].nunique() if "Line" in df.columns else "N/A",
        "columns": columns
    }

@app.get("/download/{filename}")
async def download_dataset(filename: str, request: Request):
    file_path = f"data/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    survey = InducedPolarizationSurvey.from_file(file_path)
    df = survey.data

    metadata = {
        "filename": filename,
        "rows": len(df),
        "line_count": df["Line"].nunique() if "Line" in df.columns else "N/A",
        "columns": list(df.columns),
        "download_url": str(request.base_url) + f"download/file/{filename}"
    }
    return metadata

@app.get("/download/file/{filename}")
async def download_raw_file(filename: str):
    """
    Sends back the raw uploaded file for download.
    """
    file_path = f"data/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename, media_type="application/octet-stream")


