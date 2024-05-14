import moviepy.editor as mp
import sys
import tkinter as tk
from tkinter import filedialog

def convert_mp4_to_mp3(mp4_file_path):
    """
    Converts an MP4 video file to an MP3 audio file.

    Parameters:
    mp4_file_path (str): The path to the MP4 file to be converted.

    Returns:
    str: The path to the converted MP3 file.
    """
    try:
        # Load the video file
        video_clip = mp.VideoFileClip(mp4_file_path)
        
        # Extract the audio from the video
        audio_clip = video_clip.audio
        
        # Define the output MP3 file path
        mp3_file_path = mp4_file_path.rsplit('.', 1)[0] + '.mp3'
        
        # Write the audio to an MP3 file
        audio_clip.write_audiofile(mp3_file_path)
        
        # Close the clips to free up resources
        video_clip.close()
        audio_clip.close()
        
        print(f"Conversion successful: {mp3_file_path}")
        return mp3_file_path
    except Exception as e:
        print(f"Error converting {mp4_file_path} to MP3: {e}")
        return None

if __name__ == "__main__":
    # GUIを使用してファイル選択ダイヤログを表示
    root = tk.Tk()
    root.withdraw()  # Tkのメインウィンドウを表示しない
    mp4_file_path = filedialog.askopenfilename(
        title="Select MP4 File",
        filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*"))
    )
    
    if mp4_file_path:
        convert_mp4_to_mp3(mp4_file_path)
    else:
        print("No file selected.")
