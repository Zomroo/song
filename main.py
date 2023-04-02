import os
import pyrogram
import re
import requests
from pytube import YouTube

# Set up the Pyrogram client
api_id = 16844842
api_hash = 'f6b0ceec5535804be7a56ac71d08a5d4'
bot_token = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'
app = pyrogram.Client('my_bot', api_id, api_hash, bot_token=bot_token)

# Define the song command handler
@app.on_message(pyrogram.filters.command(['song']))
def song_command_handler(client, message):
    # Get the song name from the message text
    song_name = message.text.split(' ', 1)[1]
    
    # Search for the song on YouTube and get the URL of the first video in the search results
    search_url = f'https://www.youtube.com/results?search_query={song_name}&sp=EgIQAQ%253D%253D'
    html = requests.get(search_url).text
    video_ids = re.findall(r"watch\?v=(\S{11})", html)
    video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    
    # Download the audio of the video and send it to the user
    try:
        video = YouTube(video_url)
        audio_stream = video.streams.filter(only_audio=True).first()
        audio_stream.download(output_path='downloads/')
        audio_file_path = os.path.join('downloads/', audio_stream.default_filename)
        client.send_audio(
            message.chat.id,
            audio=open(audio_file_path, 'rb'),
            title=video.title,
            performer=video.author
        )
    except Exception as e:
        print(str(e))

# Start the Pyrogram client
app.run()
