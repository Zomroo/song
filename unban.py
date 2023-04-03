from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

# Add your own API ID and API Hash from the Telegram API website
api_id = 16844842
api_hash = 'f6b0ceec5535804be7a56ac71d08a5d4'

# Add your own bot token obtained from the BotFather
bot_token = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk

# Add your own Telegram user ID as the owner ID
owner_id = 5148561602

# create a Pyrogram client instance
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# define the command "/unbanall" and restrict it to group chats only
@ app.on_message(filters.command("unbanall") & filters.group)
def unban_all_members(client, message):
    # check if the user is the owner of the bot
    if message.from_user.id != owner_id:
        message.reply_text("You do not have permission to unban all members.")
        return

    # retrieve the list of banned users
    banned_members = client.get_chat_members(message.chat.id, filter="banned")

    # unban each member one by one
    for member in banned_members:
        client.unban_chat_member(message.chat.id, member.user.id)

    # notify the user that all members have been unbanned
    message.reply_text("All members have been unbanned.")

# start the bot
app.run()
