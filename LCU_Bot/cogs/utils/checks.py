import discord
from discord.ext import tasks, commands
import datetime
from discord.ui import View, Button
from discord import Interaction, app_commands
import time
from datetime import timezone
import math
import asyncio
from cogs.utils.checks import *
import re
import sys
import sqlite3

async def create_id(ctx: Interaction, type):
  unique_id = 0
  strikeSTR = ""
  warnSTR = ""
  strikeNUM = 0
  warnNUM = 0

  con = sqlite3.connect("cogs/data/main_db.db")
  cur = con.cursor()

  try:

    if type == "warn":
      warnLOG = cur.execute(f"SELECT warn_id FROM warns")
      warns = warnLOG.fetchall()
      if not warns:
        return f"{type}-1"
      else:
        warns = warns[-1]
        for letter in warns:
            warnSTR += letter

        length = len(warnSTR) + 1
        warnNUM = warnSTR[5:length]
          
        warnNUM = int(warnNUM)
        
        unique_id = warnNUM + 1
        unique_id = f"{type}-{unique_id}"
        return unique_id

    if type == "strike":
      strikeLOG = cur.execute(f"SELECT strike_id FROM strikes")
      strikes = strikeLOG.fetchall()
      if not strikes:
        return f"{type}-1"
      else:
        strikes = strikes[-1]
        for letter in strikes:
            strikeSTR += letter

        length = len(strikeSTR) + 1
        strikeNUM = strikeSTR[9:length]
          
        strikeNUM = int(strikeNUM)
        
        unique_id = strikeNUM + 1
        unique_id = f"{type}-{unique_id}"
        return unique_id

  except Exception as e:
    print(e)
    return "Something went wrong"


async def insertData(ctx, session_banner_link, shutdown_banner_link, emoji_id, staff_roles_id, management_roles_id, session_role_id, m_command_channel, ping_channel, server_name, server_owner, server_code, vote_number, m_command_text, advertisement):
  con = sqlite3.connect("cogs/data/main_db.db")
  cur = con.cursor()
  res = cur.execute(f"SELECT guild_id FROM setup WHERE guild_id = '{int(ctx.guild.id)}'")
  result = res.fetchone()

  try:
    if result == None:
      cur.execute("INSERT INTO setup VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (int(ctx.guild.id), str(session_banner_link), str(shutdown_banner_link), str(emoji_id), str(staff_roles_id), str(management_roles_id), str(session_role_id), str(m_command_channel), str(ping_channel), str(server_name), str(server_owner), str(server_code), int(vote_number), str(m_command_text), str(advertisement)))
      cur.execute(f"INSERT INTO embeds(guild_id) VALUES ('{int(ctx.guild.id)}')")

    else:
      cur.execute(f"UPDATE setup SET session_banner_link = ?, shutdown_banner_link = ?, emoji_id = ?, staff_roles_id = ?, management_roles_id = ?, session_role_id = ?, m_command_channel = ?, ping_channel = ?, server_name = ?, server_owner = ?, server_code = ?, vote_number = ?, m_command_text = ?, advertisement = ? WHERE guild_id = '{int(ctx.guild.id)}'", (str(session_banner_link), str(shutdown_banner_link), str(emoji_id), str(staff_roles_id), str(management_roles_id), str(session_role_id), str(m_command_channel), str(ping_channel), str(server_name), str(server_owner), str(server_code), int(vote_number), str(m_command_text), str(advertisement)))
  except Exception as e:
    raise e

  con.commit()
  con.close()  

async def getInfo(ctx):
  guild_info = []
  con = sqlite3.connect("cogs/data/main_db.db")
  cur = con.cursor()
  #cur.execute(f"INSERT INTO setup(guild_id) VALUES (1234)")
  res = cur.execute(f"SELECT * FROM setup WHERE guild_id = '{int(ctx.guild.id)}'")
  result = res.fetchone()
  con.close()
  for item in result:
    if item == "None":
      guild_info.append("")
    else:
      guild_info.append(item)
  
  return guild_info

async def checkStaff(ctx):
  guild_info = await getInfo(ctx)
  var = False
  member = guild_info[4]
  member = member[1:-1]
  member_list = re.split(r',\s?', member)
  for member in member_list:
    staff = discord.utils.get(ctx.guild.roles, id=int(member))
    if staff in ctx.author.roles:
      var = True
      break
    else:
      var = False
      pass
  if var:
    return True
  else:
    return False
  
async def checkManage(ctx):
  guild_info = await getInfo(ctx)
  var = False
  member = guild_info[5]
  member = member[1:-1]
  member_list = re.split(r',\s?', member)
  for member in member_list:
    staff = discord.utils.get(ctx.guild.roles, id=int(member))
    if staff in ctx.author.roles:
      var = True
      break
    else:
      var = False
      pass
  if var:
    return True
  else:
    return False

async def checkSetUp(ctx):
  con = sqlite3.connect("cogs/data/main_db.db")
  cur = con.cursor()

  res = cur.execute(f"SELECT guild_id FROM setup WHERE guild_id = '{int(ctx.guild.id)}'")
  result = res.fetchone()
  if result == None:
    em = discord.Embed(title="Setup", description="Please setup the bot!", color=discord.Color.blue())
    await ctx.send(embed = em)
    return False
  else:
    return True


async def sessionChange(ctx: Interaction, bot):
  em = discord.Embed(title=f"Session Embed Changer", description=f"The following are options to include in your description.")
  em.add_field(name=f"ROBLOX server name", value="{ro_name}", inline=True)
  em.add_field(name=f"ROBLOX server owner", value="{ro_owner}", inline=True)
  em.add_field(name=f"ROBLOX server code", value="{ro_code}", inline=True)
  em.add_field(name=f"Server Emoji", value="{emoji}", inline=True)
  em.add_field(name=f"Timestamp", value="{timestamp}", inline=True)
  await ctx.response.send_message(embed=em)
  shutdown_msg = await bot.wait_for('message', timeout=None, check=lambda message: message.author == ctx.user)
  await shutdown_msg.delete()
  con = sqlite3.connect("cogs/data/main_db.db")
  cur = con.cursor()
  cur.execute(f"UPDATE embeds SET session_description = '{shutdown_msg.content}' WHERE guild_id = '{int(ctx.guild.id)}'")
  con.commit()
  con.close()
  await ctx.followup.send("Your embed is now changed", ephemeral=True)

async def shutdownChange(ctx: Interaction, bot):
  em = discord.Embed(title=f"Shutdown Embed Changer", description=f"The following are options to include in your description.")
  em.add_field(name=f"ROBLOX server name", value="{ro_name}", inline=True)
  em.add_field(name=f"ROBLOX server owner", value="{ro_owner}", inline=True)
  em.add_field(name=f"ROBLOX server code", value="{ro_code}", inline=True)
  em.add_field(name=f"Server Emoji", value="{emoji}", inline=True)
  em.add_field(name=f"Timestamp", value="{timestamp}", inline=True)
  await ctx.response.send_message(embed=em)
  shutdown_msg = await bot.wait_for('message', timeout=None, check=lambda message: message.author == ctx.user)
  await shutdown_msg.delete()
  con = sqlite3.connect("cogs/data/main_db.db")
  cur = con.cursor()
  cur.execute(f"UPDATE embeds SET shutdown_description = '{shutdown_msg.content}' WHERE guild_id = '{int(ctx.guild.id)}'")
  con.commit()
  con.close()
  await ctx.followup.send("Your embed is now changed", ephemeral=True)

async def svoteChange(ctx: Interaction, bot):
  em = discord.Embed(title=f"SVote Embed Changer", description=f"The following are options to include in your description.")
  em.add_field(name=f"ROBLOX server name", value="{ro_name}", inline=True)
  em.add_field(name=f"ROBLOX server owner", value="{ro_owner}", inline=True)
  em.add_field(name=f"ROBLOX server code", value="{ro_code}", inline=True)
  em.add_field(name=f"Server Emoji", value="{emoji}", inline=True)
  em.add_field(name=f"Timestamp", value="{timestamp}", inline=True)
  await ctx.response.send_message(embed=em)
  shutdown_msg = await bot.wait_for('message', timeout=None, check=lambda message: message.author == ctx.user)
  await shutdown_msg.delete()
  con = sqlite3.connect("cogs/data/main_db.db")
  cur = con.cursor()
  cur.execute(f"UPDATE embeds SET svote_description = '{shutdown_msg.content}' WHERE guild_id = '{int(ctx.guild.id)}'")
  con.commit()
  con.close()
  await ctx.followup.send("Your embed is now changed", ephemeral=True)

# async def logCommand(ctx, command, bot):
#   em = discord.Embed(title=f"Command logging", description=f"Command: **{command}**\nUsername: **{ctx.author}**\nUser ID: **{ctx.author.id}**\nGuild Name: **{ctx.guild.name}**")
#   em.timestamp = datetime.datetime.utcnow()
#   channel = bot.get_channel(1059547911454736505)

#   await channel.send(embed=em)

async def convertInto(ctx: Interaction, bot, member_list):
  msg = ""
  member_list = member_list[1:-1]
  member_list = re.split(r',\s?', member_list)
  for member in member_list:
      staff = discord.utils.get(ctx.guild.roles, id=int(member))
      msg += f"{staff.mention}"

  return msg