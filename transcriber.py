from dotenv import load_dotenv
import os
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from tqdm import tqdm
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("🚨API key not found. Check your .env file.")

client = genai.Client(api_key=api_key)

def summarise_transcript():
    for chunk in tqdm(texts, desc="Summarizing", unit="chunk"):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{SYSTEM_PROMPT} {chunk}"
            )
            opt = f"{response.text}\n\n"
            time.sleep(3)
            sf.write(opt)

def get_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    output = ""
    for index, x in tqdm(enumerate(transcript), desc="Transcribing", unit="words"): 
        sentence = x['text']
        start_timestamp = x['start']
        duration = x["duration"]
        output += f'{index + 1}.\n{start_timestamp:.3f} --> {duration + start_timestamp:.3f}\n{sentence}\n\n'
    return output

url = input("Enter the YouTube watch link: ") 
print("Entered URL:", url)

if "youtube.com/watch?v=" in url:
    video_id = url.split("v=")[1].split("&")[0]
    print('Searching for video...')
else:
    raise ValueError("🚨Invalid YouTube URL")

try:
    output = get_transcript(video_id)

    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads", "Transcriber")
    os.makedirs(downloads_folder, exist_ok=True)
    output_path = os.path.join(downloads_folder, "output.srt")
    summary_path = os.path.join(downloads_folder, "summarisedOutput.txt")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print("Transcript saved to:", output_path)

    if not os.path.exists(output_path):
        raise FileNotFoundError("🚨Transcript file was not created!")

    with open(output_path, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    if not transcript_text.strip():
        raise ValueError("🚨Transcript file is empty!")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False
    )
    texts = text_splitter.split_text(transcript_text)

    SYSTEM_PROMPT = (
        "You are a helpful assistant that summarizes text. "
        "Please summarize the following content. This content can be a transcript of a YouTube video. "
        "Please summarize the content in a concise and informative manner. "
        "You may receive timestamps which you need to ignore and focus on the content and summarize it. "
        "Please do not include any timestamps in the summary. The summary should be in English and easy to understand. "
        "Please do not include any personal opinions or comments in the summary. "
        "The summary should be factual, objective, concise, and to the point. "
        "Avoid unnecessary details or filler words."
    )

    with open(summary_path, 'w', encoding='utf-8') as sf:
        summarise_transcript()

    print("✅Summary saved to:", summary_path)

except Exception as e:
    print(f"🚨An error occurred: {e}")
