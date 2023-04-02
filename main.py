from pyrogram import Client, filters
import lyricsgenius
import pyrogram

# Set up the Pyrogram client
api_id = 16844842
api_hash = 'f6b0ceec5535804be7a56ac71d08a5d4'
bot_token = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'
app = pyrogram.Client('my_bot', api_id, api_hash, bot_token=bot_token)


def fetch_lyrics(song_name):
    genius = lyricsgenius.Genius("bwQCIfxQqXqkuEFiXt6xY387J-L9b9GgfnHph85YcP0EQvC9ZpWG-js7okipBsFe")
    song = genius.search_song(song_name)
    if song:
        return song.lyrics
    else:
        return "Sorry, I couldn't find the lyrics for that song."


@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text(
        "Hello! I can fetch the lyrics of a song for you. To get started, send me a message in the format /lyc song name."
    )


@app.on_message(filters.command("lyc"))
def fetch_lyrics_command(client, message):
    song_name = " ".join(message.command[1:])
    lyrics = fetch_lyrics(song_name)
    if lyrics == "Sorry, I couldn't find the lyrics for that song.":
        message.reply_text(lyrics)
    else:
        with open(f"{song_name}.txt", "w") as file:
            file.write(lyrics)
        client.send_document(
            message.chat.id,
            document=f"{song_name}.txt",
            caption=f"Lyrics of {song_name}"
        )


app.run()
