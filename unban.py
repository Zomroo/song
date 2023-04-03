import os
from pyrogram import Client

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get bot token and group ID from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

# Create a Pyrogram client instance
app = Client("my_bot", bot_token=BOT_TOKEN)

# Define function to unban all users in a group
async def unban_all_users():
    chat_id = os.getenv('CHAT_ID')
    async for member in app.iter_chat_members(chat_id, filter='banned'):
        user_id = member.user.id
        try:
            await app.unban_chat_member(chat_id, user_id)
            print(f'Unbanned user {user_id}')
        except:
            print(f'Failed to unban user {user_id}')

# Call the function to unban all users
app.run(unban_all_users())
