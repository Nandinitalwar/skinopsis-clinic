'use client';

import { useState } from 'react';

interface TextInputProps {
  onTranscriptSubmit: (transcript: string) => void;
  isLoading: boolean;
}

export default function TextInput({ onTranscriptSubmit, isLoading }: TextInputProps) {
  const [transcript, setTranscript] = useState('');

  const handleTranscriptSubmit = () => {
    if (transcript.trim()) {
      onTranscriptSubmit(transcript);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      handleTranscriptSubmit();
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-4">Enter Consultation Transcript</h2>
        <p className="text-sm text-gray-600 mb-4">
          Paste or type the medical consultation transcript below. The system will extract structured prescription data from the text.
        </p>
      </div>

      <div>
        <label htmlFor="transcript" className="block text-sm font-medium text-gray-700">
          Medical Transcript
        </label>
        <textarea
          id="transcript"
          rows={10}
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900 placeholder-gray-400"
          placeholder="Enter the consultation transcript here...

Example:
Patient is John Doe, 45 year old male presenting with hypertension. He has been experiencing symptoms for 2 weeks. His presenting symptoms include elevated blood pressure, headaches, and dizziness. He has no known allergies. He is currently taking aspirin. No significant past medical history. I am prescribing Lisinopril 10mg to be taken once daily. Patient should follow up in 2 weeks to monitor blood pressure."
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <p className="mt-2 text-sm text-gray-500">
          Include patient information, symptoms, diagnosis, current medications, and treatment plan for best results. 
          Press Ctrl+Enter (Cmd+Enter on Mac) or click the button to submit.
        </p>
      </div>

      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-600">
          {transcript.trim().length > 0 && (
            <span>{transcript.trim().length} characters entered</span>
          )}
        </div>
        <button
          type="button"
          onClick={handleTranscriptSubmit}
          disabled={!transcript.trim() || isLoading}
          className="bg-blue-600 text-white px-6 py-2 rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Processing...' : 'Generate Prescription'}
        </button>
      </div>

      {isLoading && (
        <div className="text-center py-4">
          <div className="inline-flex items-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span className="text-sm text-gray-600">Processing your transcript...</span>
          </div>
        </div>
      )}
    </div>
  );
}