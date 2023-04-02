import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Enter your API ID, API HASH, and BOT TOKEN below
api_id = 16844842	
api_hash = "f6b0ceec5535804be7a56ac71d08a5d4"	
bot_token = "5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk"	

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define a function to handle the /start command
@app.on_message(filters.command("start"))
def start_command_handler(client: Client, message: Message):
    # Send a welcome message to the user
    client.send_message(chat_id=message.chat.id, text="Hello! Send me a /song command followed by the name of a song to get started.")

# Define a function to handle the /song command
@app.on_message(filters.command("song"))
def song_command_handler(client: Client, message: Message):
    # Get the song name from the command arguments
    song_name = " ".join(message.command[1:])

    # Use an API or library of your choice to search for the song and get its audio file
    # For example, you could use the YouTube API and the pytube library to download a song as an mp3 file:
    import pytube
    video_url = pytube.YouTube(f"ytsearch:{song_name}").streams.filter(only_audio=True).first().url
    audio_file = pytube.YouTube(video_url).streams.filter(only_audio=True).first().download()
    
    # Send the audio file to the user
    client.send_audio(chat_id=message.chat.id, audio=audio_file)
    
    # Delete the downloaded file from the server to save storage space
    os.remove(audio_file)

# Start the client
app.run()
