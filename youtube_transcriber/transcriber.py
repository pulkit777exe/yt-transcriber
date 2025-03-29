from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter 

url = input("Enter the Youtube watch link: ") 
print("Entered URL:", url)

if "youtube.com/watch?v=" in url:
    video_id = url.split("v=")[1]
    if "&" in video_id:
        video_id = video_id.split("&")[0]
    print("Video ID:", video_id)
else:
    print("Invalid Youtube URL")

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, preserve_formatting=True)

    print("Your transcript has been stored in the file named output.srt")

    output = ''
    for index, x in enumerate(transcript): 
        sentence = x['text']
        startTimestamp = x['start']
        duration = x["duration"]
        output += f'{index + 1}.\n{startTimestamp:.3f} --> {duration + startTimestamp:.3f}\n{sentence}\n\n'

    with open('tmp/output.srt', 'w', encoding='utf-8') as f:
        f.write(output)

    print(output)

except Exception as e:
    print(f"An error occurred: {e}")
