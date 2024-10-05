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

class infract(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  intent = discord.Intents.default()
  intent.message_content = True
  intent.members = True
  bot = commands.Bot(command_prefix="t-", intents=intent)
  

  @bot.hybrid_command(description="This command is used to punish any staff members who require a punishment.", with_app_command = True)
  async def warn(self, ctx: commands.Context, member: discord.Member, *, reason: str = "None Was Specified"):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
          dt = datetime.datetime.now()
          timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
          timestamp = math.floor(timestamp)
      
          warn_id = await create_id(ctx, "warn")
          con = sqlite3.connect("cogs/data/main_db.db")
          cur = con.cursor()
          cur.execute(f"INSERT INTO warns(user_id, warn_reason, warn_id) VALUES ('{member.id}', '{reason}', '{warn_id}')")
          con.commit()
          con.close()
          
          em = discord.Embed(title=f"{guild_info[3]} Staff Warning", description=f"The HR Team has decided to take the following actions upon you. Please do not start any drama about this.\n\n> **Username:** {member.name}\n> **Reason:** {reason}\n> **Submission Date:** <t:{timestamp}:F>", color=discord.Color.from_rgb(255, 255, 254))
          em.set_footer(text=f"Your Punishment ID is: {warn_id}")
          await ctx.send(embed=em)
          try:
            await member.send(embed=em)
          except:
            await ctx.send("I cant send a message to this user!")
          try:
            await ctx.message.delete()
          except:
            pass
          return
      else:
          em = discord.Embed(title="Missing Permissions.", description="You are missing the needed permissions to run this command, make sure you have the `staff/management` roles that you setup during the bot setup.", color=discord.Color.red())
          await ctx.send(embed=em)
          return
    else:
      return

  @bot.hybrid_command(description="This command is used to search a users warnings (e.g -search_warns @user)", with_app_command = True)
  async def search_warns(self, ctx: commands.Context, member: discord.Member):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT user_id, warn_reason, warn_id FROM warns WHERE user_id = '{member.id}'")
        result = res.fetchall()
        if not result:
          em = discord.Embed(title=f"", description=f"This member is not in our database", color=discord.Color.from_rgb(255, 255, 254))
          return await ctx.send(embed=em)

        em = discord.Embed(title=f"{member}", description=f"These are the users warns", color=discord.Color.from_rgb(255, 255, 254))
        for warn in result:
          em.add_field(name=f"{warn[1]}", value=f"`{warn[2]}`")
        await ctx.send(embed=em)
        con.commit()
        con.close()

        try:
          await ctx.message.delete()
        except:
          pass
        return
      else:
            em = discord.Embed(title="Missing Permissions.", description="You are missing the needed permissions to run this command, make sure you have the `staff/management` roles that you setup during the bot setup.", color=discord.Color.red())
            await ctx.send(embed=em)
            return
    else:
      return

  @bot.hybrid_command(description="This command is used to punish any staff members who require a punishment.", with_app_command = True) 
  async def strike(self, ctx: commands.Context, member: discord.Member, *, reason: str = "None Was Specified"):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        dt = datetime.datetime.now()
        timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
        timestamp = math.floor(timestamp)
    
        strike_id = await create_id(ctx, "strike")
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO strikes(user_id, strike_reason, strike_id) VALUES ('{member.id}', '{reason}', '{strike_id}')")
        con.commit()
        con.close()
        
        em = discord.Embed(title=f"{guild_info[3]} Staff Strike", description=f"The HR Team has decided to take the following actions upon you. Please do not start any drama about this.\n\n> **Username:** {member.name}\n> **Reason:** {reason}\n> **Submission Date:** <t:{timestamp}:F>", color=discord.Color.from_rgb(255, 255, 254))
        em.set_footer(text=f"Your Punishment ID is: {strike_id}")
        await ctx.send(embed=em)
        await member.send(embed=em)
        try:
          await ctx.message.delete()
        except:
          pass
        return
      else:
            em = discord.Embed(title="Missing Permissions.", description="You are missing the needed permissions to run this command, make sure you have the `staff/management` roles that you setup during the bot setup.", color=discord.Color.red())
            await ctx.send(embed=em)
            return
    else:
      return

  @bot.hybrid_command(description="This command is used to search a users strikes (e.g -search_strikes @user)", with_app_command = True)
  async def search_strikes(self, ctx: commands.Context, member: discord.Member):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:

        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT user_id, strike_reason, strike_id FROM strikes WHERE user_id = '{member.id}'")
        result = res.fetchall()
        if not result:
          em = discord.Embed(title=f"", description=f"This member is not in our database", color=discord.Color.from_rgb(255, 255, 254))
          return await ctx.send(embed=em)

        em = discord.Embed(title=f"{member}", description=f"These are the users warns", color=discord.Color.from_rgb(255, 255, 254))
        for warn in result:
          em.add_field(name=f"{warn[1]}", value=f"`{warn[2]}`")
        await ctx.send(embed=em)
        con.commit()
        con.close()

        try:
          await ctx.message.delete()
        except:
          pass
        return
      else:
            em = discord.Embed(title="Missing Permissions.", description="You are missing the needed permissions to run this command, make sure you have the `staff/management` roles that you setup during the bot setup.", color=discord.Color.red())
            await ctx.send(embed=em)
            return
    else:
      return

  @bot.hybrid_command(description="This command is used to delete a users warn (e.g -delete_warn @user)", with_app_command = True)
  async def delete_warn(self, ctx: commands.Context, member: discord.Member, *, id: str):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:

        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT warn_id FROM warns WHERE user_id = '{member.id}'")
        result = res.fetchall()
        
        if not result:
          em = discord.Embed(title=f"", description=f"This warn is not in our database", color=discord.Color.from_rgb(255, 255, 254))
          return await ctx.send(embed=em)
        else:
          cur.execute(f"DELETE FROM warns WHERE warn_id = '{id}'")

        em = discord.Embed(title=f"Success!", description=f"Warn id `{id}` has been deleted.", color=discord.Color.green())
        await ctx.send(embed=em)
        con.commit()
        con.close()

        try:
          await ctx.message.delete()
        except:
          pass
        return
      else:
            em = discord.Embed(title="Missing Permissions.", description="You are missing the needed permissions to run this command, make sure you have the `staff/management` roles that you setup during the bot setup.", color=discord.Color.red())
            await ctx.send(embed=em)
            return
    else:
      return

  @bot.hybrid_command(description="This command is used to delete a users strike (e.g -delete_strike @user)", with_app_command = True)
  async def delete_strike(self, ctx: commands.Context, member: discord.Member, *, id: str):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:

        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT strike_id FROM strikes WHERE user_id = '{member.id}'")
        result = res.fetchall()
        if not result:
          em = discord.Embed(title=f"", description=f"This strike is not in our database", color=discord.Color.from_rgb(255, 255, 254))
          return await ctx.send(embed=em)
        else:
          cur.execute(f"DELETE FROM strikes WHERE strike_id = '{id}'")

        em = discord.Embed(title=f"Success!", description=f"Warn id `{id}` has been deleted.", color=discord.Color.green())
        await ctx.send(embed=em)
        con.commit()
        con.close()

        try:
          await ctx.message.delete()
        except:
          pass
        return
      else:
            em = discord.Embed(title="Missing Permissions.", description="You are missing the needed permissions to run this command, make sure you have the `staff/management` roles that you setup during the bot setup.", color=discord.Color.red())
            await ctx.send(embed=em)
            return
    else:
      return
    
    
async def setup(bot):
  await bot.add_cog(infract(bot))