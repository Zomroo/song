from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess

# Replace the placeholders with your own values
api_id = 16844842
api_hash = "f6b0ceec5535804be7a56ac71d08a5d4"
bot_token = "5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command(["start"]))
def start_handler(_, message: Message):
    message.reply_text("Hello! I am a music bot. Use /song to get audio of a song from YouTube, and /lyc to get lyrics.")

@app.on_message(filters.command(["song"]))
def song_handler(_, message: Message):
    if len(message.command) == 1:
        message.reply_text("Please specify a song name.")
        return

    song_name = " ".join(message.command[1:])

    # Download audio from YouTube using youtube-dl
    audio_filename = f"{song_name}.mp3"
    subprocess.run(["youtube-dl", "-x", "--audio-format", "mp3", "-o", audio_filename, f"ytsearch:{song_name}"])

    # Send audio to the user
    message.reply_audio(audio_filename)

    # Remove audio file
    os.remove(audio_filename)

@app.on_message(filters.command(["lyc"]))
def lyc_handler(_, message: Message):
    if len(message.command) == 1:
        message.reply_text("Please specify a song name.")
        return

    song_name = " ".join(message.command[1:])

    # Download lyrics from Genius.com using youtube-dl
    lyrics_filename = f"{song_name}.txt"
    subprocess.run(["youtube-dl", "--write-lyrics", "--skip-download", "-o", lyrics_filename, f"ytsearch:{song_name}"])

    # Send lyrics to the user
    with open(lyrics_filename, "r") as f:
        message.reply_document(f)

    # Remove lyrics file
    os.remove(lyrics_filename)

app.run()
