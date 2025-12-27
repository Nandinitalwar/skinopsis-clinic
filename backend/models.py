from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class Sex(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class Medication(BaseModel):
    title: str
    instructions: List[str]

class PrescriptionData(BaseModel):
    patient_name: str = ""
    age_years: str = ""
    sex: str = ""
    diagnosis: str = ""
    symptom_duration: str = ""
    presenting_symptoms: List[str] = Field(default_factory=list)
    allergies: str = ""
    current_medications: str = ""
    past_medical_history: str = ""
    medications: List[Medication] = Field(default_factory=list)
    followup_text: str = ""
    date: str = ""
    
    def to_template_dict(self) -> Dict[str, str]:
        """Convert to template variables with computed blocks"""
        presenting_symptoms_block = "\n".join([f"• {symptom}" for symptom in self.presenting_symptoms]) if self.presenting_symptoms else ""
        
        treatment_plan_parts = []
        for med in self.medications:
            if med.title:
                parts = [med.title]
                for instruction in med.instructions:
                    if instruction:
                        parts.append(f"• {instruction}")
                treatment_plan_parts.append("\n".join(parts))
        
        treatment_plan_block = "\n\n".join(treatment_plan_parts)
        
        return {
            "patient_name": self.patient_name,
            "age_years": self.age_years,
            "sex": self.sex,
            "diagnosis": self.diagnosis,
            "symptom_duration": self.symptom_duration,
            "presenting_symptoms_block": presenting_symptoms_block,
            "allergies": self.allergies,
            "current_medications": self.current_medications,
            "past_medical_history": self.past_medical_history,
            "treatment_plan_block": treatment_plan_block,
            "followup_text": self.followup_text,
            "date": self.date or datetime.now().strftime("%B %d, %Y")
        }

class PrescriptionCreate(BaseModel):
    transcript: Optional[str] = None
    audio_file: Optional[str] = None

class PrescriptionResponse(BaseModel):
    id: str
    warnings: List[str]
    preview_pdf_url: str
    structured_data: PrescriptionData

class PrescriptionStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"

class PrescriptionRecord(BaseModel):
    id: str
    status: PrescriptionStatus
    structured_data: PrescriptionData
    raw_transcript: str = ""
    clean_transcript: str = ""
    warnings: List[str] = Field(default_factory=list)
    created_at: datetime
    approved_at: Optional[datetime] = None
    preview_pdf_path: Optional[str] = None
    final_pdf_path: Optional[str] = None
    docx_path: Optional[str] = None