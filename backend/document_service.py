import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from docxtpl import DocxTemplate
from models import PrescriptionData

class DocumentService:
    def __init__(self, template_path: str, output_dir: str):
        self.template_path = template_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Verify template exists
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found at {template_path}")
    
    def generate_docx(self, prescription_data: PrescriptionData, prescription_id: str) -> str:
        """
        Generate a filled DOCX file from the template
        Returns path to the generated DOCX file
        """
        try:
            # Load template
            doc = DocxTemplate(self.template_path)
            
            # Get template variables
            template_vars = prescription_data.to_template_dict()
            
            # Render document
            doc.render(template_vars)
            
            # Save filled document
            docx_path = self.output_dir / f"{prescription_id}.docx"
            doc.save(str(docx_path))
            
            return str(docx_path)
            
        except Exception as e:
            raise Exception(f"Error generating DOCX: {str(e)}")
    
    def convert_to_pdf(self, docx_path: str, prescription_id: str) -> str:
        """
        Convert DOCX to PDF using LibreOffice headless
        Returns path to the generated PDF file
        """
        try:
            pdf_path = self.output_dir / f"{prescription_id}.pdf"
            
            # Use LibreOffice to convert DOCX to PDF
            cmd = [
                "soffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", str(self.output_dir),
                docx_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise Exception(f"LibreOffice conversion failed: {result.stderr}")
            
            # Verify PDF was created
            if not pdf_path.exists():
                raise Exception("PDF file was not created")
            
            return str(pdf_path)
            
        except subprocess.TimeoutExpired:
            raise Exception("PDF conversion timed out")
        except Exception as e:
            raise Exception(f"Error converting to PDF: {str(e)}")
    
    def generate_prescription_pdf(self, prescription_data: PrescriptionData, prescription_id: str) -> tuple[str, str]:
        """
        Generate both DOCX and PDF files for a prescription
        Returns (docx_path, pdf_path)
        """
        docx_path = self.generate_docx(prescription_data, prescription_id)
        pdf_path = self.convert_to_pdf(docx_path, prescription_id)
        
        return docx_path, pdf_path
    
    def validate_template(self) -> Dict[str, Any]:
        """
        Validate that the template contains required placeholders
        """
        required_placeholders = {
            "patient_name", "age_years", "sex", "diagnosis",
            "symptom_duration", "presenting_symptoms_block",
            "allergies", "current_medications", "past_medical_history",
            "treatment_plan_block", "followup_text", "date"
        }
        
        try:
            with open(self.template_path, 'rb') as f:
                doc = DocxTemplate(f)
                # This is a simplified check - docxtpl doesn't provide easy placeholder extraction
                return {
                    "valid": True,
                    "message": "Template loaded successfully",
                    "required_placeholders": list(required_placeholders)
                }
        except Exception as e:
            return {
                "valid": False,
                "message": f"Template validation failed: {str(e)}",
                "required_placeholders": list(required_placeholders)
            }