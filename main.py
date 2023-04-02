from pyrogram import Client, filters
from pyrogram.types import Message

app = Client("my_bot", api_id=16844842, api_hash="f6b0ceec5535804be7a56ac71d08a5d4", bot_token="5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk")

# define the /start command
@app.on_message(filters.command("start"))
def start_command(client: Client, message: Message):
    message.reply_text("Hello! I'm ready to ban all members in your group. Use the /all command to begin.")

# define the /all command
@app.on_message(filters.command("all") & filters.group)
def all_command(client: Client, message: Message):
    # check if user is the bot owner
    if message.from_user.id != 5148561602:
        message.reply_text("You are not authorized to use this command.")
        return

    # get the chat ID where the command was sent
    chat_id = message.chat.id

    # check if bot is an admin in the chat
    bot_member = client.get_chat_member(chat_id, "me")
if bot_member.status not in ["administrator", "creator"]:
    message.reply_text("I'm not an admin in this chat.")
    return


    # check if bot has permission to ban members
    if not bot_member.can_restrict_members:
        message.reply_text("I don't have permission to ban members in this chat.")
        return

    # get list of members in the chat and ban them
    members = client.get_chat_members(chat_id)
    for member in members:
        try:
            client.kick_chat_member(chat_id, member.user.id)
        except Exception as e:
            print(e) # handle any exceptions that may occur during the banning process

    message.reply_text("All members have been banned from the chat.")

app.run()
