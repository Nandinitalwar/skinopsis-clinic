'use client';

import { useState, useEffect } from 'react';

interface Medication {
  title: string;
  instructions: string[];
}

interface PrescriptionData {
  patient_name: string;
  age_years: string;
  sex: string;
  diagnosis: string;
  symptom_duration: string;
  presenting_symptoms: string[];
  allergies: string;
  current_medications: string;
  past_medical_history: string;
  medications: Medication[];
  followup_text: string;
  date: string;
}

interface PrescriptionFormProps {
  initialData: PrescriptionData;
  onSubmit: (data: PrescriptionData) => void;
}

export default function PrescriptionForm({ initialData, onSubmit }: PrescriptionFormProps) {
  const [formData, setFormData] = useState<PrescriptionData>(initialData);

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  const handleInputChange = (field: keyof PrescriptionData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSymptomsChange = (index: number, value: string) => {
    const newSymptoms = [...formData.presenting_symptoms];
    newSymptoms[index] = value;
    setFormData(prev => ({ ...prev, presenting_symptoms: newSymptoms }));
  };

  const addSymptom = () => {
    setFormData(prev => ({
      ...prev,
      presenting_symptoms: [...prev.presenting_symptoms, '']
    }));
  };

  const removeSymptom = (index: number) => {
    const newSymptoms = formData.presenting_symptoms.filter((_, i) => i !== index);
    setFormData(prev => ({ ...prev, presenting_symptoms: newSymptoms }));
  };

  const handleMedicationChange = (index: number, field: 'title', value: string) => {
    const newMedications = [...formData.medications];
    newMedications[index] = { ...newMedications[index], [field]: value };
    setFormData(prev => ({ ...prev, medications: newMedications }));
  };

  const handleMedicationInstructionChange = (medIndex: number, instrIndex: number, value: string) => {
    const newMedications = [...formData.medications];
    const newInstructions = [...newMedications[medIndex].instructions];
    newInstructions[instrIndex] = value;
    newMedications[medIndex] = { ...newMedications[medIndex], instructions: newInstructions };
    setFormData(prev => ({ ...prev, medications: newMedications }));
  };

  const addMedicationInstruction = (medIndex: number) => {
    const newMedications = [...formData.medications];
    newMedications[medIndex] = {
      ...newMedications[medIndex],
      instructions: [...newMedications[medIndex].instructions, '']
    };
    setFormData(prev => ({ ...prev, medications: newMedications }));
  };

  const removeMedicationInstruction = (medIndex: number, instrIndex: number) => {
    const newMedications = [...formData.medications];
    newMedications[medIndex] = {
      ...newMedications[medIndex],
      instructions: newMedications[medIndex].instructions.filter((_, i) => i !== instrIndex)
    };
    setFormData(prev => ({ ...prev, medications: newMedications }));
  };

  const addMedication = () => {
    setFormData(prev => ({
      ...prev,
      medications: [...prev.medications, { title: '', instructions: [''] }]
    }));
  };

  const removeMedication = (index: number) => {
    const newMedications = formData.medications.filter((_, i) => i !== index);
    setFormData(prev => ({ ...prev, medications: newMedications }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label htmlFor="patient_name" className="block text-sm font-medium text-gray-700">
            Patient Name
          </label>
          <input
            type="text"
            id="patient_name"
            value={formData.patient_name}
            onChange={(e) => handleInputChange('patient_name', e.target.value)}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
          />
        </div>

        <div>
          <label htmlFor="age_years" className="block text-sm font-medium text-gray-700">
            Age (years)
          </label>
          <input
            type="text"
            id="age_years"
            value={formData.age_years}
            onChange={(e) => handleInputChange('age_years', e.target.value)}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
          />
        </div>

        <div>
          <label htmlFor="sex" className="block text-sm font-medium text-gray-700">
            Sex
          </label>
          <select
            id="sex"
            value={formData.sex}
            onChange={(e) => handleInputChange('sex', e.target.value)}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
          >
            <option value="">Select...</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </div>

      <div>
        <label htmlFor="diagnosis" className="block text-sm font-medium text-gray-700">
          Diagnosis
        </label>
        <input
          type="text"
          id="diagnosis"
          value={formData.diagnosis}
          onChange={(e) => handleInputChange('diagnosis', e.target.value)}
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
        />
      </div>

      <div>
        <label htmlFor="symptom_duration" className="block text-sm font-medium text-gray-700">
          Symptom Duration
        </label>
        <input
          type="text"
          id="symptom_duration"
          value={formData.symptom_duration}
          onChange={(e) => handleInputChange('symptom_duration', e.target.value)}
          placeholder="e.g., 3 days, 2 weeks"
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Presenting Symptoms
        </label>
        {formData.presenting_symptoms.map((symptom, index) => (
          <div key={index} className="flex mb-2">
            <input
              type="text"
              value={symptom}
              onChange={(e) => handleSymptomsChange(index, e.target.value)}
              placeholder={`Symptom ${index + 1}`}
              className="flex-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
            />
            <button
              type="button"
              onClick={() => removeSymptom(index)}
              className="ml-2 text-red-600 hover:text-red-800"
            >
              Remove
            </button>
          </div>
        ))}
        <button
          type="button"
          onClick={addSymptom}
          className="text-blue-600 hover:text-blue-800 text-sm"
        >
          + Add Symptom
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label htmlFor="allergies" className="block text-sm font-medium text-gray-700">
            Allergies
          </label>
          <textarea
            id="allergies"
            rows={3}
            value={formData.allergies}
            onChange={(e) => handleInputChange('allergies', e.target.value)}
            placeholder="List known allergies or 'None known'"
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
          />
        </div>

        <div>
          <label htmlFor="current_medications" className="block text-sm font-medium text-gray-700">
            Current Medications
          </label>
          <textarea
            id="current_medications"
            rows={3}
            value={formData.current_medications}
            onChange={(e) => handleInputChange('current_medications', e.target.value)}
            placeholder="List current medications"
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
          />
        </div>

        <div>
          <label htmlFor="past_medical_history" className="block text-sm font-medium text-gray-700">
            Past Medical History
          </label>
          <textarea
            id="past_medical_history"
            rows={3}
            value={formData.past_medical_history}
            onChange={(e) => handleInputChange('past_medical_history', e.target.value)}
            placeholder="Relevant past medical history"
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-4">
          Treatment Plan / Medications
        </label>
        {formData.medications.map((medication, medIndex) => (
          <div key={medIndex} className="border border-gray-200 rounded-md p-4 mb-4">
            <div className="flex justify-between items-center mb-3">
              <h4 className="font-medium">Medication {medIndex + 1}</h4>
              <button
                type="button"
                onClick={() => removeMedication(medIndex)}
                className="text-red-600 hover:text-red-800 text-sm"
              >
                Remove Medication
              </button>
            </div>
            
            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700">
                Medication Name
              </label>
              <input
                type="text"
                value={medication.title}
                onChange={(e) => handleMedicationChange(medIndex, 'title', e.target.value)}
                placeholder="e.g., Amoxicillin 500mg"
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Instructions
              </label>
              {medication.instructions.map((instruction, instrIndex) => (
                <div key={instrIndex} className="flex mb-2">
                  <input
                    type="text"
                    value={instruction}
                    onChange={(e) => handleMedicationInstructionChange(medIndex, instrIndex, e.target.value)}
                    placeholder={`Instruction ${instrIndex + 1}`}
                    className="flex-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
                  />
                  <button
                    type="button"
                    onClick={() => removeMedicationInstruction(medIndex, instrIndex)}
                    className="ml-2 text-red-600 hover:text-red-800 text-sm"
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={() => addMedicationInstruction(medIndex)}
                className="text-blue-600 hover:text-blue-800 text-sm"
              >
                + Add Instruction
              </button>
            </div>
          </div>
        ))}
        <button
          type="button"
          onClick={addMedication}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          + Add Medication
        </button>
      </div>

      <div>
        <label htmlFor="followup_text" className="block text-sm font-medium text-gray-700">
          Follow-up Instructions
        </label>
        <textarea
          id="followup_text"
          rows={3}
          value={formData.followup_text}
          onChange={(e) => handleInputChange('followup_text', e.target.value)}
          placeholder="Follow-up instructions for the patient"
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
        />
      </div>

      <div>
        <label htmlFor="date" className="block text-sm font-medium text-gray-700">
          Date
        </label>
        <input
          type="date"
          id="date"
          value={formData.date}
          onChange={(e) => handleInputChange('date', e.target.value)}
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
        />
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          className="bg-blue-600 text-white px-6 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
        >
          Update Preview
        </button>
      </div>
    </form>
  );
}