import sys
from pathlib import Path

def save_transcription(transcription, video_file_name):
    """
    Saves the transcription text to a .txt file named after the video file.

    Parameters:
    transcription (str): The transcribed text to be saved.
    video_file_name (str): The name of the video file, used to name the text file.
    """
    try:
        # Define the output text file path based on the video file name
        txt_file_path = Path(video_file_name).with_suffix('.txt')

        # Save the transcription to the text file
        with open(txt_file_path, "w") as txt_file:
            txt_file.write(transcription)
            print(f"Saved transcription to: {txt_file_path}")
    except Exception as e:
        print(f"Error saving transcription for {video_file_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python save_transcription.py <transcription> <video_file_name>")
        sys.exit(1)
    
    # Collect the transcription and video file name from the command line arguments
    transcription = sys.argv[1]
    video_file_name = sys.argv[2]

    save_transcription(transcription, video_file_name)
