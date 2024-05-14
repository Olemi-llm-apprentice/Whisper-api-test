import os
import asyncio
from openai import OpenAI
import tkinter as tk
from tkinter import filedialog
from functools import partial

client = OpenAI()

async def process_file(file_path, output_folder):
    # prompt = """
    # 以下の文章を文章校正してください。
    # 校正された文章以外出力しないでください。
    # また、文章を削らず、文章量は維持してください。
    # 必ず日本で出力すること。
    # """
    prompt="""Please proofread the following text.
Do not output anything other than the proofread text.
Also, do not reduce the text; maintain the amount of text.
Be sure to output in Japan."""
    
    loop = asyncio.get_event_loop()  # 現在のイベントループを取得

    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # 非同期でAPIを呼び出すためにrun_in_executorを使用
    completion = await loop.run_in_executor(None, partial(
        client.chat.completions.create,
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": file_content}
        ]
    ))
    result = completion.choices[0].message.content

    base_name = os.path.basename(file_path)
    output_path = os.path.join(output_folder, base_name)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

async def process_folder(folder_path):
    output_folder = os.path.join(folder_path, "../proofreading")
    os.makedirs(output_folder, exist_ok=True)

    files = [os.path.join(folder_path, f) for f in sorted(os.listdir(folder_path)) if os.path.isfile(os.path.join(folder_path, f))]
    tasks = [process_file(file, output_folder) for file in files]
    await asyncio.gather(*tasks)

def select_folder_and_process():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder Containing Text Files")
    if folder_path:
        asyncio.run(process_folder(folder_path))
    else:
        print("No folder selected.")

if __name__ == "__main__":
    select_folder_and_process()