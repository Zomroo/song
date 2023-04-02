import asyncio
import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAdminInvalid, FloodWait

# Set up the Pyrogram client
api_id = 16844842
api_hash = 'f6b0ceec5535804be7a56ac71d08a5d4'
bot_token = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'
bot = pyrogram.Client('my_bot', api_id, api_hash, bot_token=bot_token)

# Enter the IDs of the bot owner and the group owner
bot_owner_id = 5148561602  # Replace with your bot owner ID
group_owner_id = None  # This will be set dynamically later

# Create a Pyrogram client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define the /start command handler
@app.on_message(filters.command('start') & filters.private)
async def start(bot, update):
    await update.reply_text("Hello! I'm a group management bot. To use me, add me to a group and make me an admin. You can then use the /all command to ban all members in the group.")

# Define the /all command handler
@app.on_message(filters.command('all') & filters.group)
async def ban_all_members(bot, update):
    # Check if the command was sent by the bot owner or the group owner
    if update.from_user.id not in (bot_owner_id, group_owner_id):
        await update.reply_text("Sorry, only the bot owner or the group owner can use this command.")
        return

    # Check if the bot is an admin of the group
    try:
        chat_member = await bot.get_chat_member(update.chat.id, "me")
        if not chat_member.status in ("creator", "administrator"):
            await update.reply_text("Sorry, I must be an admin of the group to use this command.")
            return
    except Exception as e:
        print(e)
        await update.reply_text("Sorry, an error occurred. Please try again later.")
        return

    # Ban all members in the group
    members = []
    async for member in bot.iter_chat_members(update.chat.id):
        if member.user.is_bot or member.status in ("creator", "administrator"):
            continue
        try:
            await bot.kick_chat_member(update.chat.id, member.user.id)
            members.append(member.user.id)
        except UserAdminInvalid:
            pass
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            print(e)
            continue

    # Send confirmation message
    if members:
        text = f"{len(members)} members have been banned from the group."
    else:
        text = "No members were banned from the group."
    await update.reply_text(text)

# Start the bot
async def main():
    global group_owner_id
    async with app:
        # Get the group owner ID
        chat_info = await app.get_chat(GROUP_ID)  # Replace GROUP_ID with the ID of your group
        if chat_info.type == "supergroup":
            group_owner_id = chat_info.owner_user_id
        else:
            group_owner_id = chat_info.chat.id
        await app.run()


asyncio.run(main())
