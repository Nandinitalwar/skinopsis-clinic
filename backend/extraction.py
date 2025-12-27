import os
import json
import logging
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from models import PrescriptionData, Medication

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExtractor:
    """
    AI-powered medical data extraction system with regex fallback
    """
    
    def __init__(self):
        self.warnings = []
        self.use_ai = bool(os.getenv('OPENAI_API_KEY'))
        
        if self.use_ai:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                logger.info("AI extraction enabled with OpenAI")
            except ImportError:
                logger.warning("OpenAI package not installed, falling back to regex")
                self.use_ai = False
            except Exception as e:
                logger.warning(f"AI initialization failed: {e}, falling back to regex")
                self.use_ai = False
    
    def extract_from_transcript(self, transcript: str) -> Tuple[PrescriptionData, List[str]]:
        """Extract structured data using AI or regex fallback"""
        self.warnings = []
        
        if not transcript or not transcript.strip():
            return self._get_demo_data(), ["Empty transcript provided"]
        
        if self.use_ai:
            return self._extract_with_ai(transcript.strip())
        else:
            return self._extract_with_regex(transcript.strip())
    
    def _extract_with_ai(self, transcript: str) -> Tuple[PrescriptionData, List[str]]:
        """Extract using OpenAI API"""
        try:
            prompt = self._create_ai_prompt(transcript)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical AI assistant specialized in extracting structured data from medical transcripts. Always respond with properly formatted JSON."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.1
            )
            
            ai_response = response.choices[0].message.content
            extracted_data = self._parse_ai_response(ai_response)
            
            return self._create_prescription_data(extracted_data), self.warnings
            
        except Exception as e:
            logger.error(f"AI extraction failed: {e}")
            self.warnings.append(f"AI extraction failed, using demo data: {str(e)}")
            return self._get_demo_data(), self.warnings
    
    def _create_ai_prompt(self, transcript: str) -> str:
        """Create AI extraction prompt"""
        return f"""
Analyze this medical transcript and extract structured data as JSON:

TRANSCRIPT:
{transcript}

Return JSON with this exact structure:
{{
    "patient_name": "Patient's full name (empty string if not found)",
    "age_years": "Age in years (empty string if not found)",
    "sex": "Male/Female/Other (empty string if not found)",
    "diagnosis": "Primary diagnosis (empty string if not found)",
    "symptom_duration": "Duration of symptoms (empty string if not found)",
    "presenting_symptoms": ["List of current symptoms"],
    "allergies": "Known allergies or 'No known allergies' (empty string if not found)",
    "current_medications": "Current medications (empty string if not found)",
    "past_medical_history": "Past medical history (empty string if not found)",
    "medications": [
        {{
            "title": "Medication name and dosage",
            "instructions": ["List of instructions"]
        }}
    ],
    "followup_text": "Follow-up instructions (empty string if not found)"
}}

IMPORTANT:
- Extract only information explicitly mentioned
- Use professional medical language
- Separate medication names from instructions
- Return only the JSON object
"""
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse AI JSON response"""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1:
                raise ValueError("No JSON found in response")
            
            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            self.warnings.append("AI response parsing failed")
            return self._get_empty_data_dict()
    
    def _extract_with_regex(self, transcript: str) -> Tuple[PrescriptionData, List[str]]:
        """Extract using improved regex patterns"""
        data = PrescriptionData()
        
        data.patient_name = self._extract_patient_name(transcript)
        data.age_years = self._extract_age(transcript)
        data.sex = self._extract_sex(transcript)
        data.diagnosis = self._extract_diagnosis(transcript)
        data.symptom_duration = self._extract_symptom_duration(transcript)
        data.presenting_symptoms = self._extract_presenting_symptoms(transcript)
        data.allergies = self._extract_allergies(transcript)
        data.current_medications = self._extract_current_medications(transcript)
        data.past_medical_history = self._extract_past_medical_history(transcript)
        data.medications = self._extract_medications(transcript)
        data.followup_text = self._extract_followup(transcript)
        data.date = datetime.now().strftime("%Y-%m-%d")
        
        # If critical fields missing, use demo data
        if not data.patient_name or not data.diagnosis:
            return self._get_demo_data(), ["Using demo data - regex extraction incomplete"]
        
        return data, self.warnings
    
    def _create_prescription_data(self, extracted_data: Dict[str, Any]) -> PrescriptionData:
        """Create PrescriptionData from extracted dict"""
        # Clean and validate data
        medications = []
        if "medications" in extracted_data and isinstance(extracted_data["medications"], list):
            for med in extracted_data["medications"]:
                if isinstance(med, dict) and "title" in med:
                    title = str(med["title"]).strip()
                    instructions = []
                    
                    if "instructions" in med and isinstance(med["instructions"], list):
                        instructions = [str(inst).strip() for inst in med["instructions"] if inst]
                    
                    if title:
                        medications.append(Medication(title=title, instructions=instructions))
        
        # Clean symptoms
        symptoms = []
        if "presenting_symptoms" in extracted_data and isinstance(extracted_data["presenting_symptoms"], list):
            symptoms = [str(symptom).strip() for symptom in extracted_data["presenting_symptoms"] if symptom]
        
        return PrescriptionData(
            patient_name=str(extracted_data.get("patient_name", "")).strip(),
            age_years=str(extracted_data.get("age_years", "")).strip(),
            sex=str(extracted_data.get("sex", "")).strip(),
            diagnosis=str(extracted_data.get("diagnosis", "")).strip(),
            symptom_duration=str(extracted_data.get("symptom_duration", "")).strip(),
            presenting_symptoms=symptoms,
            allergies=str(extracted_data.get("allergies", "")).strip(),
            current_medications=str(extracted_data.get("current_medications", "")).strip(),
            past_medical_history=str(extracted_data.get("past_medical_history", "")).strip(),
            medications=medications,
            followup_text=str(extracted_data.get("followup_text", "")).strip(),
            date=datetime.now().strftime("%Y-%m-%d")
        )
    
    def _get_empty_data_dict(self) -> Dict[str, Any]:
        """Empty data structure"""
        return {
            "patient_name": "",
            "age_years": "",
            "sex": "",
            "diagnosis": "",
            "symptom_duration": "",
            "presenting_symptoms": [],
            "allergies": "",
            "current_medications": "",
            "past_medical_history": "",
            "medications": [],
            "followup_text": ""
        }
    
    def _get_demo_data(self) -> PrescriptionData:
        """Clean demo data for testing"""
        return PrescriptionData(
            patient_name="Sarah Johnson",
            age_years="34",
            sex="Female",
            diagnosis="Acute bacterial sinusitis",
            symptom_duration="5 days",
            presenting_symptoms=[
                "Nasal congestion",
                "Thick yellow nasal discharge",
                "Facial pain and pressure",
                "Headache",
                "Reduced sense of smell"
            ],
            allergies="No known allergies",
            current_medications="Ibuprofen 400mg as needed for pain relief",
            past_medical_history="No significant past medical history",
            medications=[
                Medication(
                    title="Amoxicillin-Clavulanate 875mg/125mg",
                    instructions=["Take twice daily with food", "Continue for 10 days"]
                ),
                Medication(
                    title="Saline nasal rinses",
                    instructions=["Use twice daily"]
                )
            ],
            followup_text="Follow up in 7-10 days if symptoms do not improve or worsen. Return immediately if severe headache, vision changes, or high fever develops.",
            date=datetime.now().strftime("%Y-%m-%d")
        )
    
    # Regex extraction methods (fallback)
    def _extract_patient_name(self, text: str) -> str:
        match = re.search(r'(?i)patient\s+is\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', text)
        return match.group(1) if match else ""
    
    def _extract_age(self, text: str) -> str:
        match = re.search(r'(\d{1,3})[-\s]*year[-\s]*old', text, re.IGNORECASE)
        return match.group(1) if match else ""
    
    def _extract_sex(self, text: str) -> str:
        if re.search(r'\bfemale\b', text, re.IGNORECASE):
            return "Female"
        elif re.search(r'\bmale\b', text, re.IGNORECASE):
            return "Male"
        return ""
    
    def _extract_diagnosis(self, text: str) -> str:
        match = re.search(r'(?i)presenting\s+with\s+([^.]+?)\.', text)
        return match.group(1).strip().title() if match else ""
    
    def _extract_symptom_duration(self, text: str) -> str:
        match = re.search(r'(?i)(?:for\s+)?(\d+\s+(?:days?|weeks?|months?))', text)
        return match.group(1) if match else ""
    
    def _extract_presenting_symptoms(self, text: str) -> List[str]:
        match = re.search(r'(?i)(?:presenting\s+)?symptoms\s+include\s+([^.]+?)\.', text)
        if match:
            parts = re.split(r',\s*|\s+and\s+', match.group(1))
            return [part.strip().title() for part in parts if part.strip()]
        return []
    
    def _extract_allergies(self, text: str) -> str:
        if re.search(r'(?i)no\s+known\s+allergies', text):
            return "No known allergies"
        match = re.search(r'(?i)allergic\s+to\s+([^.]+)', text)
        return match.group(1).strip() if match else ""
    
    def _extract_current_medications(self, text: str) -> str:
        match = re.search(r'(?i)currently\s+taking\s+([^.]+?)\.', text)
        return match.group(1).strip() if match else ""
    
    def _extract_past_medical_history(self, text: str) -> str:
        if re.search(r'(?i)no\s+significant\s+past\s+medical\s+history', text):
            return "No significant past medical history"
        return ""
    
    def _extract_medications(self, text: str) -> List[Medication]:
        medications = []
        match = re.search(r'(?i)(?:prescribing|prescribe)\s+([^.]+?)(?:\s+to\s+be\s+taken\s+([^.]+?))?\.', text)
        if match:
            med_name = match.group(1).strip()
            instructions = []
            if match.group(2):
                inst_parts = re.split(r',\s*|\s+and\s+', match.group(2))
                instructions = [part.strip().capitalize() for part in inst_parts if part.strip()]
            medications.append(Medication(title=med_name.title(), instructions=instructions))
        return medications
    
    def _extract_followup(self, text: str) -> str:
        parts = []
        match = re.search(r'(?i)follow\s+up\s+([^.]+?)\.', text)
        if match:
            parts.append(match.group(1).strip())
        match = re.search(r'(?i)return\s+([^.]+?)\.', text)
        if match:
            parts.append("Return " + match.group(1).strip())
        return '. '.join(parts)