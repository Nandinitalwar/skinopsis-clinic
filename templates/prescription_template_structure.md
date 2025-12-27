# Prescription Template Structure

This file describes the structure needed for the prescription_template.docx file.

The template must include the following placeholders exactly as shown:

## Header Section
- Doctor's letterhead/clinic information (static content)
- Date: {{date}}

## Patient Information
- Patient Name: {{patient_name}}
- Age: {{age_years}} years
- Sex: {{sex}}

## Clinical Information
- Diagnosis: {{diagnosis}}
- Duration of Symptoms: {{symptom_duration}}

### Presenting Symptoms:
{{presenting_symptoms_block}}

### Allergies:
{{allergies}}

### Current Medications:
{{current_medications}}

### Past Medical History:
{{past_medical_history}}

## Treatment Plan
{{treatment_plan_block}}

## Follow-up Instructions
{{followup_text}}

## Signature Section
- Doctor's signature (embedded in template - do NOT modify in code)
- Doctor's name and credentials (static content)
- Medical license number (static content)

---

**IMPORTANT NOTES:**

1. The actual template must be a .docx file created in Microsoft Word
2. Use double curly braces {{placeholder}} for all variable fields
3. The signature must be embedded in the template itself
4. Format the template with appropriate fonts, spacing, and professional layout
5. The presenting_symptoms_block will be formatted with bullet points
6. The treatment_plan_block will include medication names and instructions with proper formatting

**Required placeholders:**
- {{patient_name}}
- {{age_years}}
- {{sex}}
- {{diagnosis}}
- {{symptom_duration}}
- {{presenting_symptoms_block}}
- {{allergies}}
- {{current_medications}}
- {{past_medical_history}}
- {{treatment_plan_block}}
- {{followup_text}}
- {{date}}