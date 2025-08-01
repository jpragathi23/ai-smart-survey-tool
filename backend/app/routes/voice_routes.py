# backend/app/routes/voice_routes.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
import tempfile
import os
from gtts import gTTS
import speech_recognition as sr

router = APIRouter()

@router.post("/speech-to-text")
async def speech_to_text(audio_file: UploadFile = File(...), language: str = Form("en")):
    try:
        # Save uploaded file to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            contents = await audio_file.read()
            tmp.write(contents)
            temp_path = tmp.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=language)
        os.remove(temp_path)
        return {"text": text}
    except sr.UnknownValueError:
        return {"text": "", "error": "Speech unintelligible"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT failed: {str(e)}")

@router.post("/text-to-speech")
def text_to_speech(text: str = Form(...), language: str = Form("en"), slow: bool = Form(False)):
    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.write_to_fp(tmp)
            tmp_path = tmp.name

        def iterfile():
            with open(tmp_path, "rb") as f:
                yield from f
            os.remove(tmp_path)

        return StreamingResponse(iterfile(), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")
