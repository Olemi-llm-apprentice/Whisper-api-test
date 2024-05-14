import os
import streamlit as st
import pyaudio
import wave
import io
import asyncio
from openai import OpenAI

# OpenAIクライアントの初期化
client = OpenAI()

# PyAudioの設定
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

# 音声録音の関数
def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(io.BytesIO(b"".join(frames)), "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    return io.BytesIO(b"".join(frames))

# 音声翻訳の関数
async def translate_audio(audio_file):
    loop = asyncio.get_event_loop()
    try:
        # Whisper APIによる翻訳を非同期で実行
        response = await loop.run_in_executor(None, lambda: client.audio.translations.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
            language="en"
        ))
        # 翻訳されたテキストを抽出
        translated_text = response
        
        return translated_text
    except Exception as e:
        print(f"翻訳エラー: {e}")
        return None

# Streamlitアプリケーションの設定
st.title("リアルタイム英語→日本語翻訳")

if st.button("Start"):
    while True:
        # 音声の録音
        audio_file = record_audio()
        
        # 音声の翻訳
        translation = asyncio.run(translate_audio(audio_file))
        
        # 翻訳結果の表示
        if translation:
            st.write(translation)