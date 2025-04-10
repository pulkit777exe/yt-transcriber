import os
import unittest
from unittest.mock import patch, MagicMock
from transcriber import get_transcript, summarise_transcript 
# from 

DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "Transcriber-CLI")

class TestTranscriber(unittest.TestCase):
    def setUp(self):
        self.output_path = os.path.join(DOWNLOAD_FOLDER, "transcript.srt")
        self.summary_path = os.path.join(DOWNLOAD_FOLDER, "summarisedOutput.txt")

    def tearDown(self):
        for file_path in [self.output_path, self.summary_path]:
            if os.path.exists(file_path):
                os.remove(file_path)
    @patch('transcribe_yt.transcriber.YouTubeTranscriptApi')
    @patch('transcribe_yt.transcriber.genai.Client')

    def test_save_transcript(self, mock_transcript):
        mock_transcript.return_value = [
            {"text": "Hello world", "start": 0, "duration": 2.0},
            {"text": "Hello This is a test", "start": 2.0, "duration": 5.0}
        ]

        get_transcript("dummy_video_id", self.output_path)
        self.assertTrue(os.path.exists(self.output_path))
        with open(self.output_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("Hello world", content)
        self.assertIn("This is a test", content)

    @patch("transcribe-yt.client.models.generate_content")
    def test_generate_summary(self, mock_ai_response):
        mock_ai_response.return_value = MagicMock(text = "This is a summary.")

        texts = ["Chunk 1 text","Chunk 2 text"]
        summarise_transcript(texts.self.summary_path)

        self.assertTrue(os.path.exists(self.summary_path))
        with open(self.summary_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assetIn("This is summary.", content)

if __name__ == "__main__":
    unittest.main()