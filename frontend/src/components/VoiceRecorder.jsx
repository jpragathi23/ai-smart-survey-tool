import React, { useState, useRef } from 'react';

const VoiceRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunks = useRef([]);

  const startRecording = async () => {
    setIsRecording(true);
    audioChunks.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = event => {
        if (event.data.size > 0) {
          audioChunks.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(audioChunks.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(blob);
        setAudioURL(url);
      };

      mediaRecorderRef.current.start();
    } catch (err) {
      console.error("Microphone access denied or error:", err);
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  return (
    <div className="p-6 bg-white rounded-2xl shadow-md text-center">
      <h2 className="text-2xl font-semibold mb-4">🎙️ Voice Recorder</h2>
      {!isRecording ? (
        <button
          onClick={startRecording}
          className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition"
        >
          Start Recording
        </button>
      ) : (
        <button
          onClick={stopRecording}
          className="px-6 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 transition"
        >
          Stop Recording
        </button>
      )}
      {audioURL && (
        <div className="mt-4">
          <audio controls src={audioURL}></audio>
          <p className="text-sm text-gray-600 mt-2">Recording ready for submission</p>
        </div>
      )}
    </div>
  );
};

export default VoiceRecorder;
