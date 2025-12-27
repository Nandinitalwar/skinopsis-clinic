# Prescription Drafting System

A local-first MVP system for generating prescription PDFs from audio recordings or text transcripts. This system serves as a drafting tool that requires explicit doctor approval before final PDF generation.

## 🔧 System Requirements

### Prerequisites
Before running this system, ensure you have the following installed:

1. **Python 3.11+**
2. **Node.js 20.9.0+** (for Next.js frontend)
3. **FFmpeg** (for audio processing)
4. **LibreOffice** (for PDF conversion)

### Installing Prerequisites

#### macOS
```bash
# Install Python (via Homebrew)
brew install python@3.11

# Install Node.js
brew install node

# Install FFmpeg
brew install ffmpeg

# Install LibreOffice
brew install --cask libreoffice
```

#### Ubuntu/Debian
```bash
# Install Python
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install FFmpeg
sudo apt install ffmpeg

# Install LibreOffice
sudo apt install libreoffice
```

#### Windows
1. Download Python 3.11 from [python.org](https://www.python.org/downloads/)
2. Download Node.js from [nodejs.org](https://nodejs.org/)
3. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
4. Download LibreOffice from [libreoffice.org](https://www.libreoffice.org/download/)

## 🏗️ Project Structure

```
skinopsis-clinic/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # Main FastAPI application
│   ├── models.py              # Pydantic data models
│   ├── transcription.py       # Audio transcription service
│   ├── extraction.py          # Text data extraction
│   ├── document_service.py    # DOCX/PDF generation
│   ├── storage.py             # Data persistence & audit
│   ├── requirements.txt       # Python dependencies
│   └── test_api.py           # API testing script
├── frontend/                   # Next.js React frontend
│   ├── app/
│   │   ├── page.tsx          # Main prescription interface
│   │   └── components/       # React components
│   │       ├── AudioRecorder.tsx
│   │       ├── PrescriptionForm.tsx
│   │       └── PDFViewer.tsx
│   ├── package.json          # Node.js dependencies
│   └── ...                   # Next.js configuration files
├── templates/                  # Document templates
│   ├── prescription_template.docx  # Word template (USER MUST CREATE)
│   └── prescription_template_structure.md
├── data/                      # Generated files & storage
└── sample_transcript.txt     # Example transcript for testing
```

## ⚠️ CRITICAL: Template Setup

**The system requires a properly formatted Word template file.**

1. **Create the template file:**
   ```
   templates/prescription_template.docx
   ```

2. **The template MUST include these exact placeholders:**
   - `{{patient_name}}`
   - `{{age_years}}`
   - `{{sex}}`
   - `{{diagnosis}}`
   - `{{symptom_duration}}`
   - `{{presenting_symptoms_block}}`
   - `{{allergies}}`
   - `{{current_medications}}`
   - `{{past_medical_history}}`
   - `{{treatment_plan_block}}`
   - `{{followup_text}}`
   - `{{date}}`

3. **Template requirements:**
   - Must be a `.docx` file created in Microsoft Word
   - Include doctor's letterhead and static information
   - **Embed the doctor's signature in the template** (do NOT modify signatures in code)
   - Use professional formatting (appropriate fonts, spacing, layout)
   - See `templates/prescription_template_structure.md` for detailed structure

## 🚀 Setup & Installation

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create Python virtual environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## 🏃‍♂️ Running the Application

### Start Backend Server
```bash
cd backend
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
python main.py
```
**Backend runs on:** http://localhost:8000

### Start Frontend Server
```bash
cd frontend
npm run dev
```
**Frontend runs on:** http://localhost:3000

## 📋 System Workflow

1. **Input Stage:**
   - Upload audio file, record audio, or paste text transcript
   - System processes input and extracts structured data

2. **Edit Stage:**
   - Review and edit extracted prescription data
   - Modify patient information, diagnosis, medications, etc.
   - System validates data completeness

3. **Preview Stage:**
   - View generated prescription PDF preview
   - System creates DOCX from template and converts to PDF
   - Review all details for accuracy

4. **Approval Stage:**
   - **Doctor must approve** before final PDF generation
   - System generates final, signed PDF for use

## 🧪 Testing the System

### Test with Sample Data
```bash
# Test the API endpoints
cd backend
python test_api.py
```

### Manual Testing
1. Start both backend and frontend servers
2. Open http://localhost:3000
3. Use the sample transcript from `sample_transcript.txt`
4. Follow the 3-step workflow in the UI

## 🔒 Security & Compliance

### Data Safety
- **Never fabricates medical information** - all data must be explicitly provided
- **Requires doctor approval** for final PDF generation
- Maintains complete audit trail for all prescriptions
- Stores all versions (raw transcript, cleaned transcript, structured data)

### Audit Trail
Every prescription maintains:
- Raw audio transcript
- Cleaned transcript
- Extracted JSON data
- Generated DOCX/PDF files
- Timestamps for all operations
- Approval status and timestamps

### File Security
- Generated files served safely from `/data` directory
- No directory traversal vulnerabilities
- Temporary files cleaned up appropriately

## 🛠️ Development Commands

### Backend
```bash
# Start development server
cd backend
python main.py

# Run tests
python test_api.py

# Install new dependencies
pip install <package> && pip freeze > requirements.txt
```

### Frontend
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Add new dependencies
npm install <package>
```

## 📁 Data Storage

### Generated Files
- `data/prescriptions.json` - Prescription metadata
- `data/audit/` - Audit logs per prescription
- `data/*.docx` - Generated Word documents
- `data/*.pdf` - Generated PDF files
- `data/uploads/` - Temporary audio uploads

### File Naming Convention
- Preview: `{prescription_id}_preview.pdf`
- Final: `{prescription_id}_final.pdf`
- DOCX: `{prescription_id}.docx`

## 🔍 API Endpoints

### Core Endpoints
- `POST /api/prescriptions` - Create from audio/transcript
- `POST /api/prescriptions/{id}/render` - Update and regenerate
- `POST /api/prescriptions/{id}/approve` - Approve for final PDF
- `GET /api/prescriptions/{id}` - Get prescription details
- `GET /api/prescriptions` - List all prescriptions
- `GET /api/health` - System health check

### Health Check
```bash
curl http://localhost:8000/api/health
```

## 🚨 Troubleshooting

### Common Issues

1. **LibreOffice not found:**
   ```
   Error: soffice command not found
   ```
   **Solution:** Install LibreOffice and ensure `soffice` is in PATH

2. **FFmpeg not available:**
   ```
   Error: ffmpeg not found
   ```
   **Solution:** Install FFmpeg using your system package manager

3. **Template not found:**
   ```
   Error: Template not found at templates/prescription_template.docx
   ```
   **Solution:** Create the Word template file with required placeholders

4. **Node.js version incompatibility:**
   ```
   Error: Unsupported engine
   ```
   **Solution:** Upgrade to Node.js 20.9.0 or higher

### Debug Mode
Set environment variables for additional logging:
```bash
export DEBUG=1
export LOG_LEVEL=DEBUG
```

## 📝 Important Notes

- **This is a drafting tool:** Final prescriptions require doctor verification and approval
- **Never auto-approve:** System prevents automatic approval without explicit doctor action
- **Template ownership:** All formatting, fonts, and signatures must be controlled by the template
- **Medical accuracy:** System warns when data is missing or ambiguous
- **Local-first:** All processing happens locally, no external API calls for core functionality

## 🤝 Contributing

1. Follow the existing code patterns
2. Test all changes thoroughly
3. Update documentation when adding features
4. Ensure security best practices
5. Never compromise medical data safety

## 📞 Support

For issues and questions:
1. Check this README for solutions
2. Review error logs in the console
3. Verify all prerequisites are installed
4. Test with the sample data provided