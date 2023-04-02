from pyrogram import Client, filters
import requests
import os

# Replace with your own values
API_ID = your_api_id
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'

# Create a Pyrogram client
bot = Client('my_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define a function to fetch lyrics of a song
def get_lyrics(song_name):
    # Prepare the search query
    query = song_name + ' lyrics'
    
    # Make a Google search to fetch the lyrics page URL
    url = 'https://www.google.com/search?q=' + query
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    link = soup.find('div', {'class': 'BNeawe UPmit AP7Wnd'}).a['href']
    
    # Fetch the lyrics from the lyrics page
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    lyrics = soup.find('div', {'class': 'lyrics'}).get_text()
    
    # Return the lyrics
    return lyrics

# Define a function to handle the /lyc command
@bot.on_message(filters.command(['lyc']))
def send_lyrics(bot, message):
    # Get the song name from the message
    song_name = ' '.join(message.command[1:])
    
    # Fetch the lyrics of the song
    lyrics = get_lyrics(song_name)
    
    # Save the lyrics to a text file
    filename = song_name + '.txt'
    with open(filename, 'w') as f:
        f.write(lyrics)
    
    # Send the text file to the user
    bot.send_document(chat_id=message.chat.id, document=filename)
    
    # Delete the text file
    os.remove(filename)

# Define a function to handle the /start command
@bot.on_message(filters.command(['start']))
def start(bot, message):
    bot.send_message(chat_id=message.chat.id, text='Hello! I am a bot that can fetch lyrics of a song. To use me, just type /lyc followed by the name of the song.')

# Start the bot
bot.run()
