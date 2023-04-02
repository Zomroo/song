import os
import pyrogram
import re
import requests
from pytube import YouTube
from lyricsgenius import Genius

# Set up the Pyrogram client
api_id = 16844842
api_hash = 'f6b0ceec5535804be7a56ac71d08a5d4'
bot_token = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'
app = pyrogram.Client('my_bot', api_id, api_hash, bot_token=bot_token)

# Set up the Genius API client
genius = Genius('B29hcfPEjeuWcYJ1ifG5agCZtZdgqXpQmDIHU5q5oeY0coa6rYsFEpyfYOoUtush')

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
            video = YouTube(video_url)
            audio_stream = video.streams.filter(only_audio=True).first()
            audio_stream.download(output_path='downloads/')
            audio_file_path = os.path.join('downloads/', audio_stream.default_filename)
            thumbnail_url = video.thumbnail_url
            thumbnail_file_path = os.path.join('downloads/', f'{video.video_id}.jpg')
            with open(thumbnail_file_path, 'wb') as f:
                f.write(requests.get(thumbnail_url).content)
            client.send_audio(
                message.chat.id,
                audio=open(audio_file_path, 'rb'),
                thumb=open(thumbnail_file_path, 'rb'),
                title=video.title,
                performer=video.author
            )
        except Exception as e:
            print(str(e))
            text = 'Sorry, an error occurred while processing your request.'
    elif message.command[0] == 'lyc':
        song_name = message.text.split(' ', 1)[1]
        
        # Get the lyrics of the song using the Genius API
        try:
            song = genius.search_song(song_name)
            lyrics = song.lyrics
            with open('lyrics.txt', 'w') as f:
                f.write(lyrics)
            client.send_document(
                message.chat.id,
                document=open('lyrics.txt', 'rb'),
                caption=f"Lyrics of {song.title} by {song.artist}"
            )
            os.remove('lyrics.txt')
        except Exception as e:
            print(str(e))
            text = 'Sorry, an error occurred while processing your request.'
    
    client.send_message(message.chat.id, text)

# Start the Pyrogram client
app.run()
