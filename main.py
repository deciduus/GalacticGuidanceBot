# main.py
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, utils
from responses import get_response

# Step 0: LOAD OUR TOKEN AND CHANNEL ID SAFELY
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
MISSION_CONTROL_CHANNEL_ID: Final[int] = int(os.getenv('MISSION_CONTROL_CHANNEL_ID'))
WELCOME_CHANNEL_ID: Final[int] = int(os.getenv('WELCOME_CHANNEL_ID'))
WELCOME_MESSAGE_ID: Final[int] = int(os.getenv('WELCOME_MESSAGE_ID'))
ASTRONAUT_ROLE_ID: Final[int] = int(os.getenv('ASTRONAUT_ROLE_ID'))  # Add this line

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
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

    # Check if the bot's reaction is present on the welcome message
    welcome_channel = client.get_channel(WELCOME_CHANNEL_ID)
    welcome_message = await welcome_channel.fetch_message(WELCOME_MESSAGE_ID)
    reaction = utils.get(welcome_message.reactions, emoji='👍')
    if reaction is None or client.user not in [user async for user in reaction.users()]:
        await welcome_message.add_reaction('👍')
        print("Bot reaction added to the welcome message.")
    else:
        print("Bot reaction already exists on the welcome message.")

# STEP 4: HANDLING REACTION ADD FOR ROLE ASSIGNMENT
@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        print("Reaction added by the bot. Skipping role assignment.")
        return

    if payload.message_id == WELCOME_MESSAGE_ID and str(payload.emoji) == '👍':
        print(f"Reaction added to the welcome message by user with ID: {payload.user_id}")
        guild = client.get_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)
        if user is None:
            print(f"User with ID {payload.user_id} not found in the guild.")
            return

        role = guild.get_role(ASTRONAUT_ROLE_ID)
        if role is not None:
            await user.add_roles(role)
            print(f"Astronaut role assigned to {user.name}")
        else:
            print("Astronaut role not found in the server.")
    else:
        print("Reaction added to a different message or with a different emoji.")

# STEP 5: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# STEP 6: MAIN ENTRY POINT
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()

