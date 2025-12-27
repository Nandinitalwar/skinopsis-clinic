'use client';

import { useState } from 'react';
import PrescriptionForm from './components/PrescriptionForm';
import TextInput from './components/TextInput';
import PDFViewer from './components/PDFViewer';

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
  medications: Array<{
    title: string;
    instructions: string[];
  }>;
  followup_text: string;
  date: string;
}

interface PrescriptionResponse {
  id: string;
  warnings: string[];
  preview_pdf_url: string;
  structured_data: PrescriptionData;
}

export default function Home() {
  const [prescription, setPrescription] = useState<PrescriptionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState<'input' | 'edit' | 'preview'>('input');
  const [warnings, setWarnings] = useState<string[]>([]);

  const handleTranscriptSubmit = async (transcript: string) => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('transcript', transcript);

      const response = await fetch('http://localhost:8000/api/prescriptions', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to process prescription');
      }

      const result: PrescriptionResponse = await response.json();
      setPrescription(result);
      setWarnings(result.warnings);
      setCurrentStep('edit');
    } catch (error) {
      alert(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };


  const handleDataUpdate = async (updatedData: PrescriptionData) => {
    if (!prescription) return;

    try {
      const response = await fetch(`http://localhost:8000/api/prescriptions/${prescription.id}/render`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          structured_data: updatedData,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to update prescription');
      }

      const result = await response.json();
      setPrescription({
        ...prescription,
        structured_data: updatedData,
        preview_pdf_url: result.preview_pdf_url,
      });
      setCurrentStep('preview');
    } catch (error) {
      alert(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const handleApprove = async () => {
    if (!prescription) return;

    try {
      const response = await fetch(`http://localhost:8000/api/prescriptions/${prescription.id}/approve`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to approve prescription');
      }

      const result = await response.json();
      alert('Prescription approved! Final PDF is ready for download.');
      
      // Open the final PDF
      window.open(result.final_pdf_url, '_blank');
    } catch (error) {
      alert(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const resetForm = () => {
    setPrescription(null);
    setCurrentStep('input');
    setWarnings([]);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Prescription Drafting System</h1>
          <p className="text-gray-600 mt-2">
            Generate prescription PDFs from consultation transcripts
          </p>
        </div>

        {warnings.length > 0 && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4 mb-6">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">Warnings</h3>
                <ul className="mt-1 text-sm text-yellow-700 list-disc list-inside">
                  {warnings.map((warning, index) => (
                    <li key={index}>{warning}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white shadow rounded-lg">
          {/* Navigation */}
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 px-6" aria-label="Tabs">
              <button
                className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                  currentStep === 'input'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
                onClick={() => setCurrentStep('input')}
                disabled={isLoading}
              >
                1. Input
              </button>
              <button
                className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                  currentStep === 'edit'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
                onClick={() => setCurrentStep('edit')}
                disabled={isLoading || !prescription}
              >
                2. Edit
              </button>
              <button
                className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                  currentStep === 'preview'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
                onClick={() => setCurrentStep('preview')}
                disabled={isLoading || !prescription}
              >
                3. Preview & Approve
              </button>
            </nav>
          </div>

          <div className="p-6">
            {currentStep === 'input' && (
              <div className="space-y-6">
                <TextInput
                  onTranscriptSubmit={handleTranscriptSubmit}
                  isLoading={isLoading}
                />
              </div>
            )}

            {currentStep === 'edit' && prescription && (
              <div>
                <div className="mb-4 flex justify-between items-center">
                  <h2 className="text-lg font-medium text-gray-900">Edit Prescription Data</h2>
                  <button
                    onClick={resetForm}
                    className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-300"
                  >
                    Start Over
                  </button>
                </div>
                <PrescriptionForm
                  initialData={prescription.structured_data}
                  onSubmit={handleDataUpdate}
                />
              </div>
            )}

            {currentStep === 'preview' && prescription && (
              <div>
                <div className="mb-4 flex justify-between items-center">
                  <h2 className="text-lg font-medium text-gray-900">Preview & Approve</h2>
                  <div className="space-x-3">
                    <button
                      onClick={() => setCurrentStep('edit')}
                      className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-300"
                    >
                      Back to Edit
                    </button>
                    <button
                      onClick={handleApprove}
                      className="bg-green-600 text-white px-6 py-2 rounded-md text-sm hover:bg-green-700"
                    >
                      Approve & Download Final PDF
                    </button>
                  </div>
                </div>
                
                <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
                  <p className="text-red-800 text-sm">
                    <strong>Warning:</strong> Please carefully review all prescription details before approval. 
                    This system is a drafting tool and requires doctor approval before the final PDF can be used.
                  </p>
                </div>

                {prescription.preview_pdf_url && (
                  <PDFViewer pdfUrl={`http://localhost:8000${prescription.preview_pdf_url}`} />
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}