import os
import tempfile
from pathlib import Path
from faster_whisper import WhisperModel
import re
from typing import Tuple

class TranscriptionService:
    def __init__(self, model_size: str = "base"):
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    def transcribe_audio(self, audio_path: str) -> Tuple[str, str]:
        """
        Transcribe audio file and return (raw_transcript, clean_transcript)
        """
        segments, _ = self.model.transcribe(audio_path, beam_size=5)
        
        raw_segments = []
        for segment in segments:
            raw_segments.append(segment.text)
        
        raw_transcript = " ".join(raw_segments)
        clean_transcript = self._clean_transcript(raw_transcript)
        
        return raw_transcript, clean_transcript
    
    def _clean_transcript(self, text: str) -> str:
        """
        Clean transcript by removing filler words but preserving medical negatives
        """
        # Remove common filler words while preserving important medical negatives
        filler_words = [
            r'\b(um|umm|uh|uhm|er|ah|like|you know)\b',
            r'\b(so|well|actually)\b(?=\s)',  # Only at start of phrases
        ]
        
        cleaned = text
        for pattern in filler_words:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up multiple spaces and normalize
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        return cleaned