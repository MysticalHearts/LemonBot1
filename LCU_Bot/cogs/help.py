import discord
from discord.ext import tasks, commands
import datetime
from discord.ui import View, Button, Select
from discord import Interaction, app_commands
import time
from datetime import timezone
import math
import asyncio
from cogs.utils.checks import *
import re
import sys
import sqlite3

class help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  intent = discord.Intents.default()
  intent.message_content = True
  intent.members = True
  bot = commands.Bot(command_prefix="t-", intents=intent)
  bot.remove_command("help")
    
  @bot.hybrid_command(description="*This is what you are seeing right now.*", with_app_command = True)
  async def help(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    des = ""
    for command in self.bot.commands:
      commands = ["delete", "get", "reload", "testing", "sync", "devdm"]
      if command.name in commands:
        pass 
      else:
        des += f"**`-{command.name}`** | {command.description}\n\n"


    em = discord.Embed(title=f"{ctx.guild.name} Command List", description=f"{des}", color=discord.Color.from_rgb(16, 124, 233))
    await ctx.send(embed=em)

#`-shutdown` | *This command sends the Server Shut Down message.*\n\n`-session` | *This command sends the Server Start Up message.*\n\n`-svote` | *this commands sends the session vote embed.*\n\n`-staff` | *This command will ping your staff roles provided on setup*\n\n`-manage` | *This will ping your management roles provided on setup*\n\n`-all` | *This will ping both staff and management roles*\n\n`-on` | *This will start your m command reminders*\n\n`-off` | *This will stop your m command reminders*\n\n`-embed message` | *This will make an embed with your provided message*\n\n`-say message` | *This will send a message to the channel with the given message*\n\n`-ad` | *This will send your advertisement to the channel*\n\n`-setup` | *This will allow you to setup the bot*\n\n`-settings` | *This will allow you to change some settings of the bot*
    
#add descriptions to each command


    
async def setup(bot):
  await bot.add_cog(help(bot))