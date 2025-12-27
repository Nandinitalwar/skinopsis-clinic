import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from models import PrescriptionRecord, PrescriptionStatus, PrescriptionData

class PrescriptionStorage:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.prescriptions_file = self.data_dir / "prescriptions.json"
        self.audit_dir = self.data_dir / "audit"
        self.audit_dir.mkdir(exist_ok=True)
        
        # Initialize prescriptions file if it doesn't exist
        if not self.prescriptions_file.exists():
            self._save_prescriptions({})
    
    def _load_prescriptions(self) -> Dict[str, dict]:
        """Load all prescriptions from storage"""
        try:
            with open(self.prescriptions_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_prescriptions(self, prescriptions: Dict[str, dict]):
        """Save all prescriptions to storage"""
        with open(self.prescriptions_file, 'w') as f:
            json.dump(prescriptions, f, indent=2, default=str)
    
    def save_prescription(self, prescription: PrescriptionRecord) -> str:
        """Save a prescription record"""
        prescriptions = self._load_prescriptions()
        
        # Convert to dict for JSON serialization
        prescription_dict = prescription.dict()
        
        prescriptions[prescription.id] = prescription_dict
        self._save_prescriptions(prescriptions)
        
        # Save audit log
        self._save_audit_log(prescription.id, prescription_dict)
        
        return prescription.id
    
    def get_prescription(self, prescription_id: str) -> Optional[PrescriptionRecord]:
        """Retrieve a prescription by ID"""
        prescriptions = self._load_prescriptions()
        
        if prescription_id in prescriptions:
            prescription_dict = prescriptions[prescription_id]
            # Convert datetime strings back to datetime objects
            if prescription_dict.get('created_at'):
                prescription_dict['created_at'] = datetime.fromisoformat(prescription_dict['created_at'])
            if prescription_dict.get('approved_at'):
                prescription_dict['approved_at'] = datetime.fromisoformat(prescription_dict['approved_at'])
            
            return PrescriptionRecord(**prescription_dict)
        
        return None
    
    def update_prescription(self, prescription_id: str, updates: Dict) -> bool:
        """Update a prescription with new data"""
        prescriptions = self._load_prescriptions()
        
        if prescription_id not in prescriptions:
            return False
        
        # Apply updates
        for key, value in updates.items():
            if key == 'structured_data' and isinstance(value, PrescriptionData):
                prescriptions[prescription_id][key] = value.dict()
            else:
                prescriptions[prescription_id][key] = value
        
        self._save_prescriptions(prescriptions)
        
        # Update audit log
        self._save_audit_log(prescription_id, prescriptions[prescription_id])
        
        return True
    
    def approve_prescription(self, prescription_id: str, final_pdf_path: str) -> bool:
        """Mark prescription as approved and set final PDF path"""
        updates = {
            'status': PrescriptionStatus.APPROVED,
            'approved_at': datetime.now(),
            'final_pdf_path': final_pdf_path
        }
        
        return self.update_prescription(prescription_id, updates)
    
    def list_prescriptions(self, limit: int = 50) -> List[Dict]:
        """List all prescriptions with basic metadata"""
        prescriptions = self._load_prescriptions()
        
        result = []
        for prescription_id, data in prescriptions.items():
            result.append({
                'id': prescription_id,
                'patient_name': data.get('structured_data', {}).get('patient_name', ''),
                'status': data.get('status', ''),
                'created_at': data.get('created_at', ''),
                'approved_at': data.get('approved_at', '')
            })
        
        # Sort by creation date (newest first)
        result.sort(key=lambda x: x['created_at'], reverse=True)
        
        return result[:limit]
    
    def _save_audit_log(self, prescription_id: str, prescription_data: dict):
        """Save audit log entry for a prescription"""
        audit_file = self.audit_dir / f"{prescription_id}.json"
        
        # Load existing audit log or create new one
        audit_log = []
        if audit_file.exists():
            try:
                with open(audit_file, 'r') as f:
                    audit_log = json.load(f)
            except json.JSONDecodeError:
                audit_log = []
        
        # Add new entry
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'data': prescription_data
        }
        audit_log.append(audit_entry)
        
        # Save updated audit log
        with open(audit_file, 'w') as f:
            json.dump(audit_log, f, indent=2, default=str)
    
    def get_audit_log(self, prescription_id: str) -> List[Dict]:
        """Get audit log for a prescription"""
        audit_file = self.audit_dir / f"{prescription_id}.json"
        
        if not audit_file.exists():
            return []
        
        try:
            with open(audit_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []