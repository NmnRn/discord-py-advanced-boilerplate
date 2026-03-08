import discord
from discord.ext import commands
from discord import app_commands
import os
import datetime
from dotenv import load_dotenv
import pathlib

from Database_Processes import db_guilds as dbops
from Database_Processes import db_core
from Database_Processes.log_retention import ModLogRetention
