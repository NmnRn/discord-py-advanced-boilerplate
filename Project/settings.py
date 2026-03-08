import pathlib
import os

APP_PATH = pathlib.Path(__file__).parent.parent
ENV_PATH = APP_PATH / ".env"
COMMANDS_DIR = APP_PATH / "Commands"
EVENTS_DIR = APP_PATH / "Events"
DATABASE_DIR = APP_PATH / "Database_Processes"
SPECIAL_DIR = APP_PATH / "Special"

PYTHON_FILES = [file for file in os.listdir(path=APP_PATH) if file.endswith(".py")]

PROJECT_FILES = ["libraries.py", "settings.py", "__init__.py"]
PROJECT_FILES_DIR = APP_PATH / "Project"

APP_FILES = ["app.py", "manage.py"]

DATABASE_FILES = ["db_core.py"]

def controlProject():
    if not ENV_PATH.exists():
        ENV_PATH.touch(exist_ok=True)
        write_env()
        print("ENV_PATH created")

    if not COMMANDS_DIR.exists():
        COMMANDS_DIR.mkdir(exist_ok=True)
        print("COMMANDS_DIR created")
        createOneCommand()

    if not EVENTS_DIR.exists():
        EVENTS_DIR.mkdir(exist_ok=True)
        print("EVENTS_DIR created")
        createOneEvent()
        
    if not DATABASE_DIR.exists():
        DATABASE_DIR.mkdir(exist_ok=True)
        print("DATABASE_DIR created")
        database_controll()

    if not SPECIAL_DIR.exists():
        SPECIAL_DIR.mkdir(exist_ok=True)
        print("SPECIAL_DIR created")

    pythonFilesControl()
    strictProjectFolderControl()
    librariesFileControl()
    projectsAppFileControl()
    
    
    try:
        if (APP_PATH / "faststart.py").exists():
            (APP_PATH / "faststart.py").unlink()
    except Exception:
        pass
    finally:
        print("Setup is complete. You can now start the bot using 'python manage.py run'.")

def pythonFilesControl():
    """ Control for python files"""
    for file in PYTHON_FILES:
        if file.lower() in PROJECT_FILES:
            os.replace(src= APP_PATH / file, dst= PROJECT_FILES_DIR / file)

        elif file.lower() in APP_FILES:
            pass

        else:
            os.replace(src=APP_PATH / file, dst=SPECIAL_DIR / file)

def strictProjectFolderControl():
    """ Ensures that no unauthorized files are placed inside the Project folder itself."""
    if not PROJECT_FILES_DIR.exists():
        PROJECT_FILES_DIR.mkdir(exist_ok=True)
        return
        
    for item in os.listdir(PROJECT_FILES_DIR):
        item_path = PROJECT_FILES_DIR / item
        if item.lower() not in PROJECT_FILES and item != "__pycache__":
            print(f"Unauthorized file/folder detected in Project directory: {item}. Moving to Special...")
            try:
                os.replace(src=item_path, dst=SPECIAL_DIR / item)
            except Exception as e:
                print(f"Failed to move {item}: {e}")

def librariesFileControl():
    """ Ensures libraries.py exists to prevent system crashes. """
    lib_file = PROJECT_FILES_DIR / "libraries.py"
    if not lib_file.exists():
        print("libraries.py is missing! Recreating it with default imports...")
        with open(lib_file, "w", encoding="utf-8") as file:
            text = """import discord
from discord.ext import commands
from discord import app_commands
import os
import datetime
from dotenv import load_dotenv
import pathlib

from Database_Processes import db_guilds as dbops
from Database_Processes import db_core
from Database_Processes.log_retention import ModLogRetention
"""
            file.write(text)

def projectsAppFileControl():
    projectMainFile = APP_PATH / "app.py"
    if not projectMainFile.exists():
        with open(projectMainFile, "w", encoding="utf-8") as file:
            text = """
from Project.libraries import *
from Project import settings

settings.pythonFilesControl()
settings.strictProjectFolderControl()

APP_PATH = settings.APP_PATH
ENV_PATH = settings.ENV_PATH
load_dotenv(ENV_PATH)

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set. Add it to your .env file.")

owner_id_raw = os.getenv("OWNER_ID")
OWNER_ID = None

if owner_id_raw:
    try:
        OWNER_ID = int(owner_id_raw)
    except ValueError as exc:
        raise RuntimeError("OWNER_ID must be an integer.") from exc

bot_intents = discord.Intents.all()
bot = commands.AutoShardedBot(
    command_prefix="+",
    help_command=None,
    intents=bot_intents,
    case_insensitive=True,
    owner_id=OWNER_ID)


async def load_extensions():
    command_files = os.listdir(APP_PATH / "Commands")
    for file in command_files:
        if file.endswith(".py"):
            await bot.load_extension(f"Commands.{file[:-3]}")
    print("commands loaded")
    
    event_files = os.listdir(APP_PATH / "Events")
    for file in event_files:
        if file.endswith(".py"):
            await bot.load_extension(f"Events.{file[:-3]}")
    print("events loaded")


@bot.event 
async def setup_hook():
    await load_extensions()
    await bot.tree.sync()

@bot.event
async def on_ready():

    activity = discord.Activity(
        type = discord.ActivityType.playing,
        name = "Bot Cooking"
    )

    await bot.change_presence(activity=activity)
    print(f"{bot.shard_count} shard(s) activated")
    print(f"Logged in as {bot.user.name} ---- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


bot.run(TOKEN)


'Main file of the bot. This file is responsible for starting the bot and loading the extensions.'
"""
            file.write(text)
            file.close()

def write_env():
    with open(ENV_PATH, "w", encoding="utf-8") as file:
        text = """DISCORD_TOKEN=None
OWNER_ID=None

DB_HOST=None
DB_USER=None
DB_PASSWORD=None
DB_NAME=None"""
        file.write(text)
        file.close()

def database_controll():
    db_core = DATABASE_DIR / "db_core.py"
    if not db_core.exists():
        with open(db_core, mode="w", encoding="utf-8") as file:
            text = '''
"""
Core Database Module
Handles async database pooling, context managers, and initialization.
"""

from contextlib import asynccontextmanager
import os
import aiomysql
from aiomysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv()

db_pool = None

async def init_db_pool(pool_size: int = 10) -> None:
    """Initialize async MySQL connection pool."""
    global db_pool
    if db_pool is not None:
        return

    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    if not db_user or not db_password or not db_name:
        raise RuntimeError(
            "DB_USER, DB_PASSWORD and DB_NAME must be set in your .env file."
        )

    db_pool = await aiomysql.create_pool(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_name,
        minsize=1,
        maxsize=pool_size,
        autocommit=False,
    )


async def close_db_pool() -> None:
    """Close async MySQL pool."""
    global db_pool
    if db_pool is None:
        return

    db_pool.close()
    await db_pool.wait_closed()
    db_pool = None


@asynccontextmanager
async def get_db_connection():
    """
    Async context manager to safely get a DB connection from the pool.
    """
    if db_pool is None:
        await init_db_pool()

    async with db_pool.acquire() as connection:
        yield connection


@asynccontextmanager
async def get_db_cursor(dictionary: bool = False):
    """
    Async context manager to safely get a cursor from pooled connection.
    Usage: async with get_db_cursor() as (cursor, conn): ...
    """
    async with get_db_connection() as connection:
        if dictionary:
            async with connection.cursor(DictCursor) as cursor:
                yield cursor, connection
        else:
            async with connection.cursor() as cursor:
                yield cursor, connection
                

async def initialize_database() -> None:
    """Create required tables if they do not exist."""
    queries = [
        """
        CREATE TABLE IF NOT EXISTS guilds (
            guild_id BIGINT PRIMARY KEY,
            welcome_channel_id BIGINT,
            welcome_message VARCHAR(1000) DEFAULT '[user] Joined.',
            goodbye_channel_id BIGINT,
            goodbye_message VARCHAR(1000) DEFAULT '[user] Joined.',
            log_channel_id BIGINT,
            log_state TINYINT(1) NOT NULL DEFAULT 0,
            welcome_state TINYINT(1) NOT NULL DEFAULT 0,
            goodbye_state TINYINT(1) NOT NULL DEFAULT 0,
            mute_role_id BIGINT,
            premium TINYINT(1) DEFAULT NULL,
            ticket_system TINYINT(1) DEFAULT NULL,
            ticket_channel BIGINT,
            ticket_role BIGINT,
            antispam_state BOOL DEFAULT FALSE
        )
        """
    ]

    async with get_db_cursor() as (cursor, conn):
        for query in queries:
            await cursor.execute(query)
        await conn.commit()

# Guilds table columns
GUILD_ID = "guild_id"
WELCOME_CHANNEL_ID = "welcome_channel_id"
WELCOME_MESSAGE = "welcome_message"
GOODBYE_CHANNEL_ID = "goodbye_channel_id"
GOODBYE_MESSAGE = "goodbye_message"
LOG_CHANNEL_ID = "log_channel_id"
LOG_STATE = "log_state"
WELCOME_STATE = "welcome_state"
GOODBYE_STATE = "goodbye_state"
MUTE_ROLE_ID = "mute_role_id"
PREMIUM = "premium"
TICKET_SYSTEM = "ticket_system"
TICKET_CHANNEL = "ticket_channel"
TICKET_ROLE = "ticket_role"
TICKET_STATE = "ticket_state"
CREATED_AT = "created_at"
ANTISPAM_STATE = "antispam_state"
'''
            file.write(text)
            file.close()

def createOneCommand():
    ping_command = COMMANDS_DIR / "ping.py"
    if not ping_command.exists():
        with open(ping_command, mode="w", encoding="utf-8") as file:
            text = '''
from Project.libraries import *
import time

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot\'s connection latency")
    async def ping(self, interaction: discord.Interaction):
        # Calculate Websocket Latency
        ws_latency = round(self.bot.latency * 1000)
        
        # Calculate REST API Latency
        start_time = time.perf_counter()
        await interaction.response.defer(thinking=True)
        end_time = time.perf_counter()
        rest_latency = round((end_time - start_time) * 1000)
        
        # Determine Color based on ping
        embed_color = discord.Color.green() if ws_latency < 100 else (
            discord.Color.yellow() if ws_latency < 250 else discord.Color.red()
        )
        
        embed = discord.Embed(
            title="🏓 Pong!",
            color=embed_color,
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="🌐 WebSocket Ping", value=f"**{ws_latency}** ms", inline=True)
        embed.add_field(name="📡 API Latency", value=f"**{rest_latency}** ms", inline=True)
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PingCommand(bot))
'''
            file.write(text.strip())


def createOneEvent():
    event_file = EVENTS_DIR / "message_events.py"
    if not event_file.exists():
        with open(event_file, mode="w", encoding="utf-8") as file:
            text = '''
from Project.libraries import *

class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from the bot itself
        if message.author.bot:
            return
            
        # Example logic: you can add specific keyword triggers here
        # if "hello" in message.content.lower():
        #     await message.channel.send(f"Hello there, {message.author.mention}!")

async def setup(bot):
    await bot.add_cog(MessageEvents(bot))
'''
            file.write(text.strip())