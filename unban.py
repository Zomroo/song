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
    # Get list of banned users in the group
    banned_users = app.iter_chat_members(
        chat_id=GROUP_ID,
        filter="kicked"
    )
    # Unban each user
    async for user in banned_users:
        await app.unban_chat_member(
            chat_id=GROUP_ID,
            user_id=user.user.id
        )

# Start the client and call the function to unban all users
app.start()
app.run(unban_all_users())
