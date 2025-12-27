#!/usr/bin/env python3
"""
Test script for the prescription API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print("Health Check Response:")
        print(json.dumps(response.json(), indent=2))
        print(f"Status Code: {response.status_code}\n")
    except Exception as e:
        print(f"Health check failed: {e}\n")

def test_transcript_processing():
    """Test processing a text transcript"""
    sample_transcript = """
    Patient is Sarah Johnson, 34 year old female presenting with acute bronchitis. 
    She has been experiencing symptoms for about 5 days. Her presenting symptoms include 
    persistent dry cough, shortness of breath, mild fever, and chest discomfort. 
    She has no known allergies. She is not currently taking any medications. 
    No significant past medical history. I am prescribing Amoxicillin 500mg to be taken 
    three times daily for 7 days, and Dextromethorphan cough syrup to be taken as needed 
    for cough suppression. Patient should follow up in one week if symptoms persist or worsen. 
    Return sooner if experiencing difficulty breathing or high fever.
    """
    
    try:
        data = {"transcript": sample_transcript.strip()}
        response = requests.post(f"{BASE_URL}/api/prescriptions", data=data)
        
        print("Transcript Processing Response:")
        print(json.dumps(response.json(), indent=2))
        print(f"Status Code: {response.status_code}\n")
        
        if response.status_code == 200:
            return response.json()["id"]
    except Exception as e:
        print(f"Transcript processing failed: {e}\n")
    
    return None

def test_prescription_retrieval(prescription_id):
    """Test retrieving prescription details"""
    if not prescription_id:
        return
    
    try:
        response = requests.get(f"{BASE_URL}/api/prescriptions/{prescription_id}")
        print("Prescription Retrieval Response:")
        print(json.dumps(response.json(), indent=2))
        print(f"Status Code: {response.status_code}\n")
    except Exception as e:
        print(f"Prescription retrieval failed: {e}\n")

def test_prescription_update(prescription_id):
    """Test updating prescription data"""
    if not prescription_id:
        return
    
    updated_data = {
        "structured_data": {
            "patient_name": "Sarah Johnson",
            "age_years": "34",
            "sex": "Female",
            "diagnosis": "Acute Bronchitis",
            "symptom_duration": "5 days",
            "presenting_symptoms": ["Persistent dry cough", "Shortness of breath", "Mild fever", "Chest discomfort"],
            "allergies": "No known allergies",
            "current_medications": "None",
            "past_medical_history": "No significant past medical history",
            "medications": [
                {
                    "title": "Amoxicillin 500mg",
                    "instructions": ["Take three times daily", "Continue for 7 days", "Take with food if stomach upset occurs"]
                },
                {
                    "title": "Dextromethorphan cough syrup",
                    "instructions": ["Take as needed for cough", "Do not exceed 6 doses in 24 hours", "Take with plenty of water"]
                }
            ],
            "followup_text": "Follow up in one week if symptoms persist or worsen. Return sooner if experiencing difficulty breathing or high fever.",
            "date": "2024-12-27"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/prescriptions/{prescription_id}/render",
            json=updated_data
        )
        print("Prescription Update Response:")
        print(json.dumps(response.json(), indent=2))
        print(f"Status Code: {response.status_code}\n")
    except Exception as e:
        print(f"Prescription update failed: {e}\n")

if __name__ == "__main__":
    print("Testing Prescription API\n")
    print("=" * 50)
    
    # Test health check
    test_health_check()
    
    # Test transcript processing
    prescription_id = test_transcript_processing()
    
    # Test prescription retrieval
    test_prescription_retrieval(prescription_id)
    
    # Test prescription update
    test_prescription_update(prescription_id)
    
    print("Testing completed!")