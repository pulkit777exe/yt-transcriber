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
    "English", "Hindi", "Mandarin Chinese", "Spanish", "French",
    "Modern Standard Arabic", "Bengali", "Russian", "Portuguese", "Urdu",
    "Indonesian", "German", "Japanese", "Nigerian Pidgin", "Egyptian Arabic",
    "Marathi", "Telugu", "Turkish", "Tamil", "Cantonese",
    "Vietnamese", "Wu Chinese", "Tagalog", "Korean", "Farsi"
]

for index, lang in enumerate(languages):
    print(f"{index + 1}. {lang}")

langName = ""
langCode = ""

def get_language_info(choice):
    global langName, langCode
    languages = {
        1: ("English", "en"),
        2: ("Hindi", "hi"),
        3: ("Mandarin Chinese", "zh-Hans"),
        4: ("Spanish", "es"),
        5: ("French", "fr"),
        6: ("Modern Standard Arabic", "ar"),
        7: ("Bengali", "bn"),
        8: ("Russian", "ru"),
        9: ("Portuguese", "pt"),
        10: ("Urdu", "ur"),
        11: ("Indonesian", "id"),
        12: ("German", "de"),
        13: ("Japanese", "ja"),
        14: ("Nigerian Pidgin", "kri"),
        15: ("Egyptian Arabic", "ar"), 
        16: ("Marathi", "mr"),
        17: ("Telugu", "te"),
        18: ("Turkish", "tr"),
        19: ("Tamil", "ta"),
        20: ("Cantonese", "zh-Hant"), 
        21: ("Vietnamese", "vi"),
        22: ("Wu Chinese", "zh-Hant"),
        23: ("Tagalog", "fil"),
        24: ("Korean", "ko"),
        25: ("Farsi", "fa"),
    }
    language = languages.get(choice)
    if language:
        langName, langCode = language
        return f"You selected {langName}. Language code: {langCode}"
    else:
        return "Invalid choice. Please select a number between 1 and 25."

user_input = int(input("Enter a number (1-25) to select a language: "))
print(get_language_info(user_input))


SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes content, such as YouTube transcripts. "
    f"Summarize factually and concisely in {langName}, avoiding timestamps, opinions, and filler. "
    "You can be descriptive at times. "
    "Focus on key points and ensure clarity."
)


def summarise_transcript():
    try:
        print("This might take a while")
        for chunk in tqdm(texts, desc="Summarizing", unit="chunk"):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{SYSTEM_PROMPT} {chunk}"
            )
            opt = f"{response.text}\n\n"
            time.sleep(3)
            sf.write(opt)
    except: 
        print("🚨Error in summarising\n Please try after some time.")

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[langCode])
        output = ""
        for index, x in tqdm(enumerate(transcript), desc="Transcribing", unit=" words"): 
            sentence = x['text']
            start_timestamp = x['start']
            duration = x["duration"]
            output += f'{index + 1}.\n{start_timestamp:.3f} --> {duration + start_timestamp:.3f}\n{sentence}\n\n'
        return output
    except:
        print("🚨An error occured\nThe transctipt you were expecting is not available")
        exit(0)

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
        chunk_size=1800,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False
    )
    texts = text_splitter.split_text(transcript_text)

    with open(summary_path, 'w', encoding='utf-8') as sf:
        summarise_transcript()

    print("✅Summary saved to:", summary_path)

except Exception as e:
    print(f"🚨An error occurred: {e}")
