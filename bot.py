import discord
from discord.ext import commands
import os
import json
import tracemalloc
import logging
import os

#pip install mysql-connector-python
#pip install discord.py
#pip install requests

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.INFO, handlers=[handler])

def load_config():
    config_file = "datastores/config.json"
    config = None
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            print(f"Loaded configuration from {config_file}.")
    except FileNotFoundError:
        print(f"{config_file} not found...")
    return config

config = load_config()

# Define the intents you want your bot to have
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True  # Required to receive member update events
intents.guilds = True   # Required to receive guild events


# Prefix and bot initialization
PREFIX = "!"
# Load application_id as an integer
application_id = int(config['application_id'])
bot = commands.AutoShardedBot(command_prefix=PREFIX, intents=intents, application_id=application_id, help_command=None)

# Start memory tracking
tracemalloc.start()

# Function to load all Python files from a directory as extensions
async def load_extensions_from_folder(folder):
    for filename in os.listdir(folder):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module_path = f'{folder}.{module_name}'
            try:
                await bot.load_extension(module_path)
                print(f'Loaded extension: {module_path}')
            except Exception as e:
                print(f'Failed to load extension {module_path}. Reason: {e}')

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="Backup")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print(f"Shard ID: {bot.shard_id}")
    print(f"Total Shards: {bot.shard_count}")
    
    for shard_id, latency in bot.latencies:
        print(f"Shard ID: {shard_id} | Latency: {latency*1000:.2f}ms")

# Event: Sync commands when bot joins a new guild
@bot.event
async def on_guild_join(guild):
    await bot.tree.sync(guild=guild)

# Setup hook to load extensions
async def setup_hook():
    await load_extensions_from_folder('functions')
    await bot.tree.sync()

# Assign setup_hook to the bot
bot.setup_hook = setup_hook

# Run the bot with your token
if __name__ == '__main__':
    token = config['token']
    bot.run(token, log_handler=handler, log_level=logging.INFO)
