import os
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
import asyncio
from functools import partial

async def split_mp3(mp3_file_path, target_size_mb=8):
    loop = asyncio.get_event_loop()
    audio = await loop.run_in_executor(None, partial(AudioSegment.from_mp3, mp3_file_path))
    total_length_ms = len(audio)
    file_size_mb = os.path.getsize(mp3_file_path) / (1024 * 1024)
    target_length_ms = (target_size_mb / file_size_mb) * total_length_ms
    chunk_paths = []

    base_name = os.path.basename(mp3_file_path).rsplit('.', 1)[0]
    new_folder_path = os.path.join('resource', 'result', base_name)
    os.makedirs(new_folder_path, exist_ok=True)

    tasks = []
    for i in range(0, len(audio), int(target_length_ms)):
        chunk = audio[i:i + int(target_length_ms)]
        chunk_name = f"chunk{i}.mp3"
        chunk_path = os.path.join(new_folder_path, chunk_name)
        # 非同期タスクとしてエクスポート処理をスケジュール
        task = loop.run_in_executor(None, partial(chunk.export, chunk_path, format="mp3"))
        tasks.append(task)
        chunk_paths.append(chunk_path)
    
    # すべての非同期タスクが完了するのを待つ
    await asyncio.gather(*tasks)
    
    for chunk_path in chunk_paths:
        print(f"Created chunk: {chunk_path}")
    
    return chunk_paths

async def main():
    root = tk.Tk()
    root.withdraw()
    mp3_file_path = filedialog.askopenfilename(
        title="Select MP3 File",
        filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*"))
    )
    
    if mp3_file_path:
        await split_mp3(mp3_file_path)
    else:
        print("No file selected.")

if __name__ == "__main__":
    asyncio.run(main())