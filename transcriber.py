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

languages = [
    "English", "Mandarin Chinese", "Hindi", "Spanish", "French",
    "Modern Standard Arabic", "Bengali", "Russian", "Portuguese", "Urdu",
    "Indonesian", "German", "Japanese", "Nigerian Pidgin", "Egyptian Arabic",
    "Marathi", "Telugu", "Turkish", "Tamil", "Cantonese",
    "Vietnamese", "Wu Chinese", "Tagalog", "Korean", "Farsi"
]

for index, lang in enumerate(languages):
    print(f"{index + 1}. {lang}")

def language_case(choice):
    switch = {
        1: "You selected English.",
        2: "You selected Mandarin Chinese.",
        3: "You selected Hindi.",
        4: "You selected Spanish.",
        5: "You selected French.",
        6: "You selected Modern Standard Arabic.",
        7: "You selected Bengali.",
        8: "You selected Russian.",
        9: "You selected Portuguese.",
        10: "You selected Urdu.",
        11: "You selected Indonesian.",
        12: "You selected German.",
        13: "You selected Japanese.",
        14: "You selected Nigerian Pidgin.",
        15: "You selected Egyptian Arabic.",
        16: "You selected Marathi.",
        17: "You selected Telugu.",
        18: "You selected Turkish.",
        19: "You selected Tamil.",
        20: "You selected Cantonese.",
        21: "You selected Vietnamese.",
        22: "You selected Wu Chinese.",
        23: "You selected Tagalog.",
        24: "You selected Korean.",
        25: "You selected Farsi."
    }
    return switch.get(choice, "Invalid choice. Please select a number between 1 and 25.")

num = input("Enter the index of the language displayed above: ")

SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes text. "
    "Please summarize the following content. This content can be a transcript of a YouTube video. "
    "Please summarize the content in a concise and informative manner. "
    "You may receive timestamps which you need to ignore and focus on the content and summarize it. "
    f"Please do not include any timestamps in the summary. The summary should be in {language_case(num)} and easy to understand. "
    "Please do not include any personal opinions or comments in the summary. "
    "The summary should be factual, objective, concise, and to the point. "
    "Avoid unnecessary details or filler words."    
)

def summarise_transcript():
    print("This might take a while")
    for chunk in tqdm(texts, desc="Summarizing", unit="chunk"):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{SYSTEM_PROMPT} {chunk}"
            )
            opt = f"{response.text}\n\n"
            time.sleep(3)
            sf.write(opt)

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    output = ""
    for index, x in tqdm(enumerate(transcript), desc="Transcribing", unit=" words"): 
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

    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads", "Transcriber-CLI")
    os.makedirs(downloads_folder, exist_ok=True)
    output_path = os.path.join(downloads_folder, "transcript.srt")
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

    with open(summary_path, 'w', encoding='utf-8') as sf:
        summarise_transcript()

    print("✅Summary saved to:", summary_path)

except Exception as e:
    print(f"🚨An error occurred: {e}")
