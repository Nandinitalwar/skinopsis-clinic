import os
import uuid
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import aiofiles
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from models import (
    PrescriptionData, PrescriptionCreate, PrescriptionResponse, 
    PrescriptionRecord, PrescriptionStatus
)
# from transcription import TranscriptionService  # Temporarily disabled
from extraction import DataExtractor
from document_service import DocumentService
from storage import PrescriptionStorage

# Configuration
DATA_DIR = "../data"
TEMPLATE_PATH = "../templates/prescription_template.docx"
UPLOAD_DIR = f"{DATA_DIR}/uploads"

# Initialize services
app = FastAPI(title="Prescription System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services on startup
# transcription_service = None  # Temporarily disabled
data_extractor = None
document_service = None
storage = None

@app.on_event("startup")
async def startup_event():
    global data_extractor, document_service, storage
    
    # Create directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Initialize services
    # transcription_service = TranscriptionService()  # Temporarily disabled
    data_extractor = DataExtractor()
    document_service = DocumentService(TEMPLATE_PATH, DATA_DIR)
    storage = PrescriptionStorage(DATA_DIR)
    
    print("Services initialized successfully (audio transcription temporarily disabled)")

# Serve static files
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")

class UpdateDataRequest(BaseModel):
    structured_data: PrescriptionData

@app.post("/api/prescriptions", response_model=PrescriptionResponse)
async def create_prescription(
    transcript: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None)
):
    """
    Create a new prescription from audio or transcript
    """
    if not transcript and not audio_file:
        raise HTTPException(status_code=400, detail="Either transcript or audio file is required")
    
    prescription_id = str(uuid.uuid4())
    raw_transcript = ""
    clean_transcript = ""
    
    try:
        if audio_file:
            # Audio processing temporarily disabled
            raise HTTPException(status_code=501, detail="Audio transcription temporarily disabled. Please use text transcript instead.")
        
        elif transcript:
            raw_transcript = transcript
            clean_transcript = transcript
        
        # Extract structured data
        structured_data, warnings = data_extractor.extract_from_transcript(clean_transcript)
        
        # Generate preview documents
        try:
            docx_path, pdf_path = document_service.generate_prescription_pdf(
                structured_data, f"{prescription_id}_preview"
            )
        except Exception as e:
            warnings.append(f"Document generation warning: {str(e)}")
            docx_path = None
            pdf_path = None
        
        # Create prescription record
        prescription = PrescriptionRecord(
            id=prescription_id,
            status=PrescriptionStatus.DRAFT,
            structured_data=structured_data,
            raw_transcript=raw_transcript,
            clean_transcript=clean_transcript,
            warnings=warnings,
            created_at=datetime.now(),
            preview_pdf_path=pdf_path,
            docx_path=docx_path
        )
        
        # Save prescription
        storage.save_prescription(prescription)
        
        preview_pdf_url = f"/data/{prescription_id}_preview.pdf" if pdf_path else ""
        
        return PrescriptionResponse(
            id=prescription_id,
            warnings=warnings,
            preview_pdf_url=preview_pdf_url,
            structured_data=structured_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing prescription: {str(e)}")

@app.post("/api/prescriptions/{prescription_id}/render")
async def render_prescription(prescription_id: str, request: UpdateDataRequest):
    """
    Update prescription data and regenerate preview
    """
    # Get existing prescription
    prescription = storage.get_prescription(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    try:
        # Generate new preview documents
        docx_path, pdf_path = document_service.generate_prescription_pdf(
            request.structured_data, f"{prescription_id}_preview"
        )
        
        # Update prescription with new data
        updates = {
            'structured_data': request.structured_data,
            'preview_pdf_path': pdf_path,
            'docx_path': docx_path
        }
        
        storage.update_prescription(prescription_id, updates)
        
        preview_pdf_url = f"/data/{prescription_id}_preview.pdf"
        
        return {
            "preview_pdf_url": preview_pdf_url,
            "structured_data": request.structured_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering prescription: {str(e)}")

@app.post("/api/prescriptions/{prescription_id}/approve")
async def approve_prescription(prescription_id: str):
    """
    Approve prescription and generate final PDF
    """
    # Get existing prescription
    prescription = storage.get_prescription(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    if prescription.status == PrescriptionStatus.APPROVED:
        return {"message": "Prescription already approved", "final_pdf_url": f"/data/{prescription_id}_final.pdf"}
    
    try:
        # Generate final documents
        docx_path, pdf_path = document_service.generate_prescription_pdf(
            prescription.structured_data, f"{prescription_id}_final"
        )
        
        # Mark as approved
        storage.approve_prescription(prescription_id, pdf_path)
        
        final_pdf_url = f"/data/{prescription_id}_final.pdf"
        
        return {
            "message": "Prescription approved successfully",
            "final_pdf_url": final_pdf_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error approving prescription: {str(e)}")

@app.get("/api/prescriptions/{prescription_id}")
async def get_prescription(prescription_id: str):
    """
    Get prescription metadata and data
    """
    prescription = storage.get_prescription(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    
    preview_pdf_url = f"/data/{prescription_id}_preview.pdf" if prescription.preview_pdf_path else ""
    final_pdf_url = f"/data/{prescription_id}_final.pdf" if prescription.final_pdf_path else ""
    
    return {
        "id": prescription.id,
        "status": prescription.status,
        "structured_data": prescription.structured_data,
        "warnings": prescription.warnings,
        "created_at": prescription.created_at,
        "approved_at": prescription.approved_at,
        "preview_pdf_url": preview_pdf_url,
        "final_pdf_url": final_pdf_url
    }

@app.get("/api/prescriptions")
async def list_prescriptions():
    """
    List all prescriptions
    """
    return storage.list_prescriptions()

@app.get("/api/prescriptions/{prescription_id}/audit")
async def get_audit_log(prescription_id: str):
    """
    Get audit log for a prescription
    """
    audit_log = storage.get_audit_log(prescription_id)
    return {"audit_log": audit_log}

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    # Check template exists
    template_validation = document_service.validate_template()
    
    return {
        "status": "healthy",
        "services": {
            "transcription": "disabled (audio temporarily unavailable)",
            "extraction": "ready", 
            "document": "ready" if template_validation["valid"] else "error",
            "storage": "ready"
        },
        "template_validation": template_validation
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)