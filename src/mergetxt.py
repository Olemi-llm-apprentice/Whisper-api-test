import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

def merge_text_files(folder_path, output_file_name="merged_text.txt"):
    folder_path = Path(folder_path)
    output_path = folder_path.parent / output_file_name
    
    text_files = sorted(folder_path.glob('*.txt'))
    
    merged_content = ""
    for text_file in text_files:
        with open(text_file, 'r', encoding='utf-8') as file:
            merged_content += file.read() + "\n"
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(merged_content)
    
    print(f"Merged text file saved to: {output_path}")

def select_folder_and_merge():
    root = tk.Tk()
    root.withdraw()  # Tkのルートウィンドウを表示しない
    folder_path = filedialog.askdirectory(title="Select Folder Containing Text Files")
    if folder_path:
        merge_text_files(folder_path)
    else:
        print("No folder selected.")

if __name__ == "__main__":
    select_folder_and_merge()