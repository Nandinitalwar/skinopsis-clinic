'use client';

import { useState } from 'react';

interface PDFViewerProps {
  pdfUrl: string;
}

export default function PDFViewer({ pdfUrl }: PDFViewerProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const handleLoad = () => {
    setIsLoading(false);
    setError(null);
  };

  const handleError = () => {
    setIsLoading(false);
    setError('Failed to load PDF preview');
  };

  const openInNewTab = () => {
    window.open(pdfUrl, '_blank');
  };

  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium text-gray-900">PDF Preview</h3>
        <button
          onClick={openInNewTab}
          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700"
        >
          Open in New Tab
        </button>
      </div>
      
      <div className="relative" style={{ height: '600px' }}>
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-100 rounded">
            <div className="text-center">
              <svg className="animate-spin -ml-1 mr-3 h-8 w-8 text-blue-600 mx-auto" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p className="mt-2 text-sm text-gray-600">Loading PDF...</p>
            </div>
          </div>
        )}
        
        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-red-50 rounded border border-red-200">
            <div className="text-center">
              <svg className="mx-auto h-8 w-8 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="mt-2 text-sm text-red-600">{error}</p>
              <button
                onClick={openInNewTab}
                className="mt-2 text-sm text-blue-600 hover:text-blue-500"
              >
                Try opening in new tab
              </button>
            </div>
          </div>
        )}
        
        <iframe
          src={pdfUrl}
          className="w-full h-full border border-gray-300 rounded"
          onLoad={handleLoad}
          onError={handleError}
          title="Prescription PDF Preview"
        />
      </div>
      
      <div className="mt-4 text-sm text-gray-600">
        <p>
          <strong>Note:</strong> This is a preview of your prescription. Please review all details carefully 
          before approving. The final approved PDF will be signed and ready for use.
        </p>
      </div>
    </div>
  );
}