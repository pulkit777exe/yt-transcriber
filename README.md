# 🎥 YouTube Transcript & AI Summarizer CLI

A command-line Python tool that extracts the transcript from a YouTube video and generates an AI-powered summary using **Google GenAI**. Outputs are saved directly to your **Downloads** folder for easy access.

---

## 🚀 What It Does

Given a YouTube watch link, this CLI tool will:

1. 📝 **Extract Transcript**: Uses `youtube-transcript-api` to fetch subtitles and stores them in `transcript.srt`.
2. 🤖 **Generate AI Summary**: Uses Google GenAI via `langchain` to produce a meaningful summary of the video.
3. 💾 **Save Files**: Automatically saves:
   - `transcript.srt` – Full transcript in subtitle format.
   - `summarisedOutput.txt` – AI-generated summary.
   Both are placed inside your system's **Downloads** folder.

---

## 📦 Tech Stack / Dependencies

This project leverages the power of the following libraries:

- [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/) – Extracts subtitles directly from YouTube.
- [`google-generativeai`](https://pypi.org/project/google-generativeai/) – Access to Google's Gemini (GenAI) models.
- [`langchain`](https://github.com/langchain-ai/langchain) – Framework to interface with LLMs.
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) – Load API keys and configuration from `.env` file.
- `tqdm` – Shows progress bars for longer operations.
- `time` – For handling delays and logging.
- `dotenv` – Alternate environment loader if needed.

Install all required packages:

```bash
pip install youtube-transcript-api google-generativeai langchain python-dotenv tqdm
```

---

## ⚙️ Setup

1. **Clone the repo**:
   ```bash
   git clone https://github.com/pulkit777exe/yt-transcriber.git
   cd transcribe-yt
   ```

2. **Create a `.env` file**:
   Add your Google API Key:
   ```
   GOOGLE_API_KEY=your-google-api-key-here
   ```

3. **Run the CLI**:
   ```bash
   ##In Linux
   python3 transciber.py "https://www.youtube.com/watch?v=xyz"

   ##In Windows
   python transcriber.py "https://www.youtube.com/watch?v=xyz"
   ```

---

## 📁 Output Files

| File                    | Description                         | Location                 |
|-------------------------|-------------------------------------|--------------------------|
| `transcript.srt`        | Full transcript of the video        | Downloads folder         |
| `summarisedOutput.txt`  | AI-generated concise summary        | Downloads folder         |

---

## 💡 Example

```bash
$ python main.py "https://www.youtube.com/watch?v=xyz"
✅ Transcript saved to ~/Downloads/transcript.srt
✅ Summary saved to ~/Downloads/summarisedOutput.txt
```

---

## ❗ Important Notes

- Transcript must be available for the video (auto-generated or uploaded).
- Make sure your Google API key has access to GenAI models (e.g., Gemini 1.5).
- Supports only English transcripts at the moment.
- Handles errors gracefully and provides helpful messages.

---

## 🛠 Project Structure

```
transcribe-yt/
│
├── main.py
├── transcript_handler.py
├── summarizer.py
├── utils.py
├── .env
├── requirements.txt
└── README.md
```

---
---
Thanks to the open-source tools and the incredible GenAI platform by Google for free!

---
---
