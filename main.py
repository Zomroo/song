import logging
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the Telegram client
api_id = 16844842
api_hash = 'f6b0ceec5535804be7a56ac71d08a5d4'
bot_token = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'
client = TelegramClient('client_name', api_id, api_hash).start(bot_token=bot_token)

# Set up the banned rights
rights = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

# Define the SUDO_USERS
SUDO_USERS = [5148561602]

# Define the event handlers
@client.on(events.NewMessage(pattern="^/kickall"))
async def kickall(event):
    if event.sender_id in SUDO_USERS:
        # Get the admins in the chat
        admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        admins_id = [i.id for i in admins]
        # Iterate over the kicked users and kick them
        async for user in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked):
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)

@client.on(events.NewMessage(pattern="^/banall"))
async def banall(event):
    if event.sender_id in SUDO_USERS:
        # Get the admins in the chat
        admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        admins_id = [i.id for i in admins]
        # Iterate over the kicked users and ban them
        async for user in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked):
            if user.id not in admins_id:
                await event.client(EditBannedRequest(event.chat_id, user.id, rights))

@client.on(events.NewMessage(pattern="^/unbanall"))
async def unban(event):
    if event.sender_id in SUDO_USERS:
        # Iterate over the kicked users and unban them
        async for user in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked):
            await event.client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None)))
            await asyncio.sleep(0.1)

# Start the client
client.run_until_disconnected()
