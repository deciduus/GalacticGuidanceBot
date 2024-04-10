# main.py
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response, player

# Step 0: LOAD OUR TOKEN AND CHANNEL ID SAFELY
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
MISSION_CONTROL_CHANNEL_ID: Final[int] = int(os.getenv('MISSION_CONTROL_CHANNEL_ID'))

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    is_private = user_message.startswith('?')
    if is_private:
        user_message = user_message[1:]

    try:
        # Check if the message is from the "#mission-control" channel
        if message.channel.id == MISSION_CONTROL_CHANNEL_ID:
            response = get_response(user_message)
            if response:
                if is_private:
                    await message.author.send(response)
                else:
                    await message.channel.send(response)
        else:
            print(f"Ignoring message from channel: {message.channel}")
    except Exception as e:
        print(e)

# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

    # Send the startup message to the #mission-control channel
    mission_control_channel = client.get_channel(MISSION_CONTROL_CHANNEL_ID)
    startup_message = "Greetings, crew. This is Galactic Mission Control, your AI guide through the wonders and challenges of deep space exploration. I'm here to assist you in your quest to uncover the mysteries of the cosmos. Let's embark on this journey together!"
    await mission_control_channel.send(startup_message)

# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()