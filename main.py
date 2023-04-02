import os
import pyrogram
import re
import requests
from pytube import YouTube
import musixmatch

# Set up the Pyrogram client
api_id = 16844842
api_hash = 'f6b0ceec5535804be7a56ac71d08a5d4'
bot_token = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'
app = pyrogram.Client('my_bot', api_id, api_hash, bot_token=bot_token)

# Set up the Musixmatch API client
musixmatch_api_key = 'e86b5f48a332b3116e500790b650567c'
musixmatch_api = musixmatch.WebService(apikey=musixmatch_api_key)

# Define the song command handler
@app.on_message(pyrogram.filters.command(['start', 'song', 'lyc']))
def song_command_handler(client, message):
    # Define an empty string to hold the message text
    text = ''

    # Get the song name from the message text
    if message.command[0] == 'start':
        text = 'Welcome to my song bot!\nTo download a song, use the /song command followed by the name of the song.\nFor example, /song despacito'
    elif message.command[0] == 'song':
        song_name = message.text.split(' ', 1)[1]
        
        # Search for the song on YouTube and get the URL of the first video in the search results
        search_url = f'https://www.youtube.com/results?search_query={song_name}&sp=EgIQAQ%253D%253D'
        html = requests.get(search_url).text
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        
        # Download the audio and thumbnail of the video and send them to the user
        try:
    if message.command[0] == 'vid':
        video_url = message.command[1]
        video = pafy.new(video_url)
        bestaudio = video.getbestaudio()
        audio_file_path = f"{video.title}.mp3"
        thumbnail_file_path = f"{video.title}.jpg"
        bestaudio.download(audio_file_path, quiet=True)
        video.getbestthumb().download(thumbnail_file_path, quiet=True)
        client.send_audio(
            message.chat.id,
            audio=open(audio_file_path, 'rb'),
            thumb=open(thumbnail_file_path, 'rb'),
            title=video.title,
            performer=video.author
        )
    elif message.command[0] == 'lyc':
        song_name = message.text.split(' ', 1)[1]
        # Get the lyrics of the song using the Musixmatch API
        try:
            response = musixmatch_api.matcher_lyrics_get(song_name, '', 1)
            track_id = response['message']['body']['track']['track_id']
            lyrics = musixmatch_api.track_lyrics_get(track_id)['message']['body']['lyrics']['lyrics_body']
            with open('lyrics.txt', 'w') as f:
                f.write(lyrics)
            client.send_document(
                message.chat.id,
                document=open('lyrics.txt', 'rb'),
                caption=f"Lyrics of {response['message']['body']['artist_name']} - {response['message']['body']['track']['track_name']}"
            )
        except Exception as e:
            print(str(e))
            text = 'Sorry, an error occurred while processing your request.'
    else:
        text = 'Invalid command'
except IndexError:
    text = 'Please provide a valid command'

try:
    # If there is a message to send, send it
    if 'text' in locals():
        client.send_message(message.chat.id, text)
finally:
    # Clean up downloaded files
    if 'audio_file_path' in locals():
        os.remove(audio_file_path)
    if 'thumbnail_file_path' in locals():
        os.remove(thumbnail_file_path)
    if 'lyrics.txt' in os.listdir():
        os.remove('lyrics.txt')

# Run the client
app.run()
