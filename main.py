import os
import requests
import musixmatch
from pyrogram import Client, filters
from pyrogram.types import Message

# Set up the Musixmatch API credentials
musixmatch.api_key = 'e86b5f48a332b3116e500790b650567c'

bot = Client(	
    "bot",	
    api_id=16844842,  # Replace with your API ID	
    api_hash="f6b0ceec5535804be7a56ac71d08a5d4",  # Replace with your API hash	
    bot_token="5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk"  # Replace with your bot token	
)

# Define the command handler for the /start command
@app.on_message(filters.command('start'))
def start_handler(client: Client, message: Message):
    message.reply_text('Hello! To get started, use the /lyc command followed by the name of a song to get its lyrics.')

# Define the command handler for the /lyc command
@app.on_message(filters.command('lyc'))
def lyc_handler(client: Client, message: Message):
    # Get the song name from the message text
    song_name = ' '.join(message.command[1:])

    # Search for the song lyrics using the Musixmatch API
    track = musixmatch.Track.search(song_name, page_size=1, page=1, f_has_lyrics=1)
    lyrics = musixmatch.Track.lyrics(track[0].track_id)

    # Send the lyrics as a text file to the user
    with open(f'{song_name}.txt', 'w') as f:
        f.write(lyrics['lyrics_body'])

    message.reply_document(document=f'{song_name}.txt')

# Start the bot
app.run()
