# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository houses multiple projects:
1. **Prescription Drafting System** (Current implementation) - AI-powered prescription generation from audio/text
2. **AI Agent** (Planned future project)

## Development Commands

### Backend (FastAPI + Python)
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py  # Start development server on :8000
python test_api.py  # Run API tests
pip install -r requirements.txt  # Install dependencies
```

### Frontend (Next.js + TypeScript)
```bash
cd frontend
npm run dev  # Start development server on :3000
npm run build  # Build for production
npm install  # Install dependencies
```

### Prerequisites Check
- Python 3.11+, Node.js 20.9.0+, FFmpeg, LibreOffice required
- Template file at `templates/prescription_template.docx` must exist

## Architecture Overview

### Backend Architecture (FastAPI)
- **main.py**: FastAPI application with CORS, file serving, core endpoints
- **models.py**: Pydantic models for data validation and serialization
- **transcription.py**: faster-whisper integration for audio→text
- **extraction.py**: Rule-based text parsing for medical data extraction
- **document_service.py**: docxtpl template filling + LibreOffice PDF conversion
- **storage.py**: JSON-based persistence with audit logging

### Data Flow Pipeline
```
Audio/Text → Transcript → Structured Data → DOCX Template → PDF
```

### Frontend Architecture (Next.js)
- **app/page.tsx**: Main single-page application with 3-step workflow
- **components/AudioRecorder.tsx**: MediaRecorder API + file upload
- **components/PrescriptionForm.tsx**: Dynamic form for medical data editing
- **components/PDFViewer.tsx**: Embedded PDF preview with fallbacks

### Key Design Patterns
- **Template-driven**: All formatting owned by Word template, code never modifies layout
- **Audit-first**: Complete trail from raw input to final PDF
- **Approval-gated**: Explicit doctor approval required before final PDF
- **Local-first**: No external APIs for core functionality

### Data Models
```typescript
PrescriptionData {
  patient_name, age_years, sex, diagnosis, symptom_duration,
  presenting_symptoms[], allergies, current_medications, 
  past_medical_history, medications[{title, instructions[]}],
  followup_text, date
}
```

## Critical Implementation Details

### Template System
- Uses docxtpl with {{placeholder}} syntax
- Template at `templates/prescription_template.docx` is source of truth
- Computed fields: `presenting_symptoms_block`, `treatment_plan_block`
- Doctor signature embedded in template, never modified by code

### Medical Data Safety
- Never fabricates missing information
- Rule-based extraction with explicit warnings for ambiguous data
- Complete audit trail: raw_transcript → clean_transcript → structured_data → documents

### File Security
- Static file serving from `/data` with no traversal
- Temporary files properly cleaned
- Preview vs final file separation

## Common Development Tasks

### Adding New API Endpoints
1. Define Pydantic models in `models.py`
2. Add endpoint to `main.py` with proper error handling
3. Update test file `test_api.py`

### Modifying Data Extraction
- Edit `extraction.py` - rule-based patterns for medical text parsing
- Add comprehensive warnings for missing/ambiguous data
- Test with various transcript formats

### Frontend Component Updates
- All components use TypeScript with proper interfaces
- State management through useState/props (no external state library)
- Tailwind CSS for styling

### Testing Strategy
- Backend: `python test_api.py` for API endpoint testing
- Manual testing with sample_transcript.txt
- End-to-end workflow testing through frontend

## File Organization

### Generated Files Location
- `data/prescriptions.json` - Prescription metadata
- `data/audit/` - Per-prescription audit logs
- `data/*.pdf` - Preview and final PDFs
- `data/uploads/` - Temporary audio files

### Template Requirements
- Must create `templates/prescription_template.docx` manually
- See `templates/prescription_template_structure.md` for placeholder requirements
- Template validation via `/api/health` endpoint

## Technology Stack Specifics

### Backend Dependencies
- FastAPI for API framework
- faster-whisper for speech-to-text
- docxtpl for template filling
- LibreOffice headless for PDF conversion
- python-multipart for file uploads

### Frontend Dependencies
- Next.js 16 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- MediaRecorder API for audio recording

## Development Workflow

1. **Start both servers** (backend :8000, frontend :3000)
2. **Test with health check** - ensures template and dependencies are ready
3. **Use sample data** from sample_transcript.txt for testing
4. **Follow 3-step UI flow** - Input → Edit → Preview → Approve

## Medical Compliance Notes

This is a **drafting tool only**:
- Never auto-approves prescriptions
- Requires explicit doctor review and approval
- Maintains complete audit trail
- All formatting controlled by professional template
- Missing data flagged with warnings, never fabricated