import pyrogram

app = pyrogram.Client(
    "my_bot",
    api_id=16844842,
    api_hash="f6b0ceec5535804be7a56ac71d08a5d4",
    bot_token="5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk"
)

# Replace "owner_id" with your Telegram user ID
owner_id = 5148561602

@app.on_message(pyrogram.filters.command("unbanall") & pyrogram.filters.user(owner_id))
def unban_all(client, message):
    chat_id = message.chat.id
    banned_users = client.get_chat_members(chat_id, filter=pyrogram.filters.chat_banned())
    for user in banned_users:
        user_id = user.user.id
        client.unban_chat_member(chat_id, user_id)
    message.reply_text("All banned users have been unbanned.")

app.run()
