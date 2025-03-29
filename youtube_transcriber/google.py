from google import genai
from dotenv import load_dotenv, dotenv_values
load_dotenv()
client = genai.Client(api_key = dotenv_values(".env.GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)

print(response.text)