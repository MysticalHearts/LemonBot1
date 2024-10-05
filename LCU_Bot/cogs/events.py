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
import random

class events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, ctx):
    if self.bot.user.mentioned_in(ctx) and len(ctx.content.split(' ')) == 1 and ctx.content[-1] == ">" and ctx.content[0] == '<':
      await ctx.channel.send("My prefix is `-`\nTry `-help` for help with commands\nTry `-setup` to setup the bot")

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    top_channel = guild.text_channels[0]
    # Send a message to the top channel
    em = discord.Embed(title="Thank You For Adding!", description=f"LCU is a fully customizable Emergency Response : Liberty County. We allow you to do such things as sessions, shutdowns, and session votes\n\nSupport server: https://discord.gg/fwafbXMZrT\nSetup Command: `-setup`\nHelp Command: `-help`", color=discord.Color.blue())
    await top_channel.send(embed=em)
    channel = self.bot.get_channel(1059547913266679889)
    real_member_count = guild.member_count - len(guild.bots)
    em = discord.Embed(title=f"Bot Joining Logs", description=f"Guild Name: **{guild.name}**\nGuild ID: **{guild.id}**\nMember Count: **{real_member_count}**\nBots: **{str(len(guild.bots))}**\nGuild Count: **{str(len(self.bot.guilds))}**")
    await channel.send(embed=em)

  @commands.Cog.listener()
  async def on_ready(self):
    # con = sqlite3.connect("cogs/data/main_db.db")
    # cur = con.cursor()
    # cur.execute("DROP TABLE setup")
    # cur.execute("DROP TABLE embeds")
    # cur.execute("DROP TABLE warns")
    # cur.execute("DROP TABLE strikes")
    # cur.execute("DROP TABLE promos")
    # cur.execute("DROP TABLE demos")

    # cur.execute("CREATE TABLE setup(guild_id INTEGER NOT NULL PRIMARY KEY, session_banner_link NVARCHAR(1000), shutdown_banner_link NVARCHAR(1000), emoji_id NVARCHAR(100), staff_roles_id NVARCHAR(500), management_roles_id NVARCHAR(500), session_role_id INTEGER, m_command_channel INTEGER, ping_channel INTEGER, server_name NVARCHAR(30), server_owner NVARCHAR(20), server_code NVARCHAR(20), vote_number INTEGER, m_command_text NVARCHAR(5000), advertisement NVARCHAR(5000))")
    # cur.execute("CREATE TABLE embeds(guild_id INTEGER NOT NULL PRIMARY KEY, shutdown_description NVARCHAR(10000), session_description NVARCHAR(10000), svote_description NVARCHAR(10000), session_color NVARCHAR(50), shutdown_color NVARCHAR(50), svote_color NVARCHAR(50))")
    # cur.execute("CREATE TABLE warns(id INTEGER NOT NULL PRIMARY KEY, user_id INTEGER NOT NULL, warn_reason NVARCHAR(5000) NOT NULL, warn_id NVARCHAR(40))")
    # cur.execute("CREATE TABLE strikes(id INTEGER NOT NULL PRIMARY KEY, user_id INTEGER NOT NULL, strike_reason NVARCHAR(5000), strike_id NVARCHAR(40))")
    # cur.execute("CREATE TABLE promos(id INTEGER NOT NULL PRIMARY KEY, user_id INTEGER NOT NULL, promo_reason NVARCHAR(5000), moderator INTEGER, promo_role_id INTEGER)")
    # cur.execute("CREATE TABLE demos(id INTEGER NOT NULL PRIMARY KEY, user_id INTEGER NOT NULL, demo_reason NVARCHAR(5000), moderator INTEGER, demo_role_id INTEGER)")

    # con.commit()
    # con.close()
    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.users)} users"))

    print(self.bot.user.name + " is ready.")
    self.bot.loop.create_task(self.presenced())

  async def presenced(self):
    presences = [
        {"name": "-help"},
        {"name": f"{len(self.bot.users)} users"},
        {"name": f"{len(self.bot.guilds)} servers"}
      ]
    while True:
      for item in presences:
        await self.bot.change_presence(activity=discord.Activity(name=item["name"], type=discord.ActivityType.watching))
        await asyncio.sleep(10)

    
async def setup(bot):
  await bot.add_cog(events(bot))