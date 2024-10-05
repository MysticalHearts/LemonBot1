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

reg = r'<:\w*:\d*>'

#these are the setup options
class setUpOptions():
  def __init__(self, bot):
    super().__init__(timeout=None)
    self.bot = bot

    #this is the shift setup options
  async def all(self, ctx):
    session = []
    channel_returns = []
    staff_roles_returns = []
    manage_roles_returns = []
    async def role1callback(ctx):
      await ctx.response.defer(ephemeral=False)
      for role in select_role1.values:
        cstaff_Roles = discord.utils.get(ctx.guild.roles, name=str(role))
        cstaff_Roles = cstaff_Roles.id
        staff_roles_returns.append(cstaff_Roles)
    async def role2callback(ctx):
      await ctx.response.defer(ephemeral=False)
      for role in select_role2.values:
        cmanage_Roles = discord.utils.get(ctx.guild.roles, name=str(role))
        cmanage_Roles = cmanage_Roles.id
        manage_roles_returns.append(cmanage_Roles)
    async def role3callback(ctx):
      await ctx.response.defer(ephemeral=False)
      shift_role = discord.utils.get(ctx.guild.roles, name=str(select_role3.values[0]))
      shift_role_id = shift_role.id
      session.append(shift_role_id)
    async def channel1callback(ctx):
      await ctx.response.defer(ephemeral=False)
      shift_channel = discord.utils.get(ctx.guild.channels, name=str(select_channel1.values[0]))
      shift_channel_id = shift_channel.id
      channel_returns.append(shift_channel_id)
    async def channel2callback(ctx):
      await ctx.response.defer(ephemeral=False)
      shift_channel = discord.utils.get(ctx.guild.channels, name=str(select_channel2.values[0]))
      shift_channel_id = shift_channel.id
      channel_returns.append(shift_channel_id)
    try:
      em = discord.Embed(title=f"", description=f"What would you like your Session banner to be?(Has to be in the form of a `cdn.discordapp.com/attachments` link) Type `skip` to skip, type `cancel` to cancel setup.", color = discord.Color.green())
      em1 = await ctx.send(embed = em)
      session_banner_link = await self.bot.wait_for('message', timeout=600.0, check=lambda message: message.author == ctx.author)
      if session_banner_link.content == "skip":
        await session_banner_link.delete()
        session_banner_link = "None"
      elif session_banner_link.content == "cancel":
        return False
      elif session_banner_link.content.startswith("https://cdn.discordapp.com/attachments"):
        await session_banner_link.delete()
        session_banner_link = session_banner_link.content
      else:
        await session_banner_link.delete()
        await ctx.send("Please Provide a valid link", delete_after=2)
        while True:
          session_banner_link = await self.bot.wait_for('message', timeout=600.0, check=lambda message: message.author == ctx.author)
          if session_banner_link.content == "skip":
            await session_banner_link.delete()
            session_banner_link = "None"
            break
          elif session_banner_link.content == "cancel":
            return False
          elif session_banner_link.content.startswith("https://cdn.discordapp.com/attachments"):
            await session_banner_link.delete()
            session_banner_link = session_banner_link.content
            break
          else:
            await session_banner_link.delete()
            await ctx.send("Please Provide a valid link!", delete_after=2)
      await em1.delete()
      try:
        await session_banner_link.delete()
      except:
        pass
  
      em = discord.Embed(title=f"", description=f"What would you like your Server Shutdown banner to be? (Has to be in the form of a `cdn.discordapp.com/attachments` link)? Type `skip` to skip, type `cancel` to cancel setup.", color = discord.Color.green())
      em2 = await ctx.send(embed = em)
      shutdown_banner_link = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
      if shutdown_banner_link.content == "skip":
        await shutdown_banner_link.delete()
        shutdown_banner_link = "None"
      elif shutdown_banner_link.content == "cancel":
        return False
      elif shutdown_banner_link.content.startswith("https://cdn.discordapp.com/attachments"):
        await shutdown_banner_link.delete()
        shutdown_banner_link = shutdown_banner_link.content
      else:
        await shutdown_banner_link.delete()
        await ctx.send("Please Provide a valid link", delete_after=2)
        while True:
          shutdown_banner_link = await self.bot.wait_for('message', timeout=600.0, check=lambda message: message.author == ctx.author)
          if shutdown_banner_link.content == "skip":
            await shutdown_banner_link.delete()
            shutdown_banner_link = "None"
            break
          elif shutdown_banner_link.content == "cancel":
            return False
          elif shutdown_banner_link.content.startswith("https://cdn.discordapp.com/attachments"):
            await shutdown_banner_link.delete()
            shutdown_banner_link = shutdown_banner_link.content
            break
          else:
            await shutdown_banner_link.delete()
            await ctx.send("Please Provide a valid link", delete_after=2)
      await em2.delete()
      try:
        await shutdown_banner_link.delete()
      except:
        pass
        
      em = discord.Embed(title=f"", description=f"What is your discord server logo Emoji (Must be a custom emoji)? Type `skip` to skip, type `cancel` to cancel setup.", color = discord.Color.green())
      em2 = await ctx.send(embed = em)
      emoji_id = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
      if emoji_id.content == "skip":
        await emoji_id.delete()
        emoji_id = "None"
      elif emoji_id.content == "cancel":
            return False
      elif re.search(r'<:\w*:\d*>', emoji_id.content) != None:
        await emoji_id.delete()
        emoji_id = emoji_id.content
      else:
        await emoji_id.delete()
        await ctx.send("Please Provide a valid emoji!", delete_after=2)
        while True:
          emoji_id = await self.bot.wait_for('message', timeout=600.0, check=lambda message: message.author == ctx.author)
          if emoji_id.content == "skip":
            emoji_id = "None"
            break
          elif emoji_id.content == "cancel":
            return False
          elif re.search(r'<:\w*:\d*>', emoji_id.content) != None:
            emoji_id = emoji_id.content
            break
          else:
            await ctx.send("Please Provide a valid emoji", delete_after=2)
            await emoji_id.delete()
      await em2.delete()
      try:
        await emoji_id.delete()
      except:
        pass

      em = discord.Embed(title=f"", description=f"What are your staff team role(s) (Please do not select for management roles for this)?", color = discord.Color.green())
      select_role1 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=20)
      select_role1.callback = role1callback
      view=View()
      view.add_item(select_role1)
      em2 = await ctx.send(embed = em, view=view)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == ctx.author)
      await em2.delete()

      em = discord.Embed(title=f"", description=f"What are your management team role(s) (Please do not select for staff team roles.)?", color = discord.Color.green())
      select_role2 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=20)
      select_role2.callback = role2callback
      view=View()
      view.add_item(select_role2)
      em2 = await ctx.send(embed = em, view=view)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == ctx.author)
      await em2.delete()

      em = discord.Embed(title=f"", description=f"What is your session/SSU role?", color = discord.Color.green())
      select_role3 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=1)
      select_role3.callback = role3callback
      view=View()
      view.add_item(select_role3)
      em2 = await ctx.send(embed = em, view=view)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == ctx.author)
      await em2.delete()

      em = discord.Embed(title=f"", description=f"Where would you like your :m or :h reminders to be sent?", color = discord.Color.green())
      select_channel1 = discord.ui.ChannelSelect(placeholder="Select A Channel", min_values=1, max_values=1)
      select_channel1.callback = channel1callback
      view=View()
      view.add_item(select_channel1)
      em2 = await ctx.send(embed = em, view=view)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == ctx.author)
      await em2.delete()

      em = discord.Embed(title=f"", description=f"Where would you like your staff request commands to be sent to? (this includes the -all, -staff and -manage commands.)", color = discord.Color.green())
      select_channel2 = discord.ui.ChannelSelect(placeholder="Select A Channel", min_values=1, max_values=1)
      select_channel2.callback = channel2callback
      view=View()
      view.add_item(select_channel2)
      em2 = await ctx.send(embed = em, view=view)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == ctx.author)
      await em2.delete()

      em = discord.Embed(title=f"", description=f"What would you like the bot to be called? (`cancel` to cancel setup)?", color = discord.Color.green())
      em3 = await ctx.send(embed = em)
      name = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
      if name.content == "cancel":
        return False
      await em3.delete()
      try:
        await name.delete()
      except:
        pass

      em = discord.Embed(title=f"", description=f"What is your in-game server called(type `cancel` to cancel setup)?", color = discord.Color.green())
      em4 = await ctx.send(embed = em)
      server_name = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
      if server_name.content == "cancel":
        return False
      await em4.delete()
      try:
        await server_name.delete()
      except:
        pass

      em = discord.Embed(title=f"", description=f"Who is the owner of your in-game server(`cancel` to cancel setup)?", color = discord.Color.green())
      em2 = await ctx.send(embed = em)
      server_owner = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
      if server_owner.content == "cancel":
        return False
      await em2.delete()
      try:
        await server_owner.delete()
      except:
        pass

      em = discord.Embed(title=f"", description=f"What is your in-game server code(`cancel` to cancel setup)?", color = discord.Color.green())
      em2 = await ctx.send(embed = em)
      code = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
      if code.content == "cancel":
        return False
      await em2.delete()
      try:
        await code.delete()
      except:
        pass

      em = discord.Embed(title=f"", description=f"How many votes do you want to have for your session/ssu vote command? (e.g 4 votes.) (`cancel` to cancel setup)?", color = discord.Color.green())
      em2 = await ctx.send(embed = em)
      vote_number = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
      if vote_number.content == "cancel":
        return False
      elif vote_number.content.isdigit():
        await vote_number.delete()
        vote_number = vote_number.content
        pass
      elif vote_number.content.isdigit() == False:
        await vote_number.delete()
        await ctx.send("Please Provide a number!", delete_after=2)
        while True:
          vote_number = await self.bot.wait_for('message', timeout=600.0, check=lambda message: message.author == ctx.author)
          if vote_number.content == "cancel":
            return False
          elif vote_number.content.isdigit():
            await vote_number.delete()
            vote_number = vote_number.content
            break
          elif vote_number.content.isdigit() == False:
            await ctx.send("Please Provide a number!", delete_after=2)
      await em2.delete()
      try:
        await vote_number.delete()
      except:
        pass

      em = discord.Embed(title=f"", description=f"What is your :m/:h command reminder text (e.g :m Thanks for playing join our discord the code is discord.gg/123)(`cancel` to cancel setup)?", color = discord.Color.green())
      em2 = await ctx.send(embed = em)
      m_command_text = await self.bot.wait_for('message', timeout=None, check=lambda message: message.author == ctx.author)
      if m_command_text.content == "cancel":
        return False
      await em2.delete()
      try:
        await m_command_text.delete()
      except:
        pass

      em = discord.Embed(title=f"", description=f"What is your server advertisement(`cancel` to cancel setup)?", color = discord.Color.green())
      em3 = await ctx.send(embed = em)
      advertisement = await self.bot.wait_for('message', timeout=None, check=lambda message: message.author == ctx.author)
      if advertisement.content == "cancel":
        return False
      await em3.delete()
      try:
        await advertisement.delete()
      except:
        pass

      await insertData(ctx, session_banner_link, shutdown_banner_link, emoji_id, staff_roles_returns, manage_roles_returns, session, channel_returns[0], channel_returns[1], server_name.content, server_owner.content, code.content, vote_number, m_command_text.content, advertisement.content)
      await ctx.guild.me.edit(nick=name.content)
      return True
    except asyncio.TimeoutError:
      em = discord.Embed(title="Timeout", description="You took to long to respond! Please reset-up the bot by doing `-setup`.", color=discord.Color.red())
      return await ctx.send(embed=em)
      
class setup_bot(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  intent = discord.Intents.default()
  intent.message_content = True
  intent.members = True
  bot = commands.Bot(command_prefix="t-", intents=intent)

  @bot.hybrid_command(description="*This will allow you to setup the bot to your liking.*", with_app_command = True)
  #@commands.has_permissions(administrator=True)
  async def setup(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    em = discord.Embed(title="", description="Please make sure that you have given the appropriate permissions to LCU or else it will not work properly.", color=discord.Color.green())
    em.timestamp = datetime.datetime.utcnow()
    em.set_footer(text='LCU - Setup \u200b')
    continueB = discord.ui.Button(label="Continue", style=discord.ButtonStyle.green)
    view=View()
    view.add_item(continueB)
    msg = await ctx.send(embed=em, view=view)
    inter = await self.bot.wait_for('interaction', timeout=None, check=lambda message: message.user == ctx.author)
    await msg.delete()
    is_setup = await setUpOptions.all(self, ctx)
    if is_setup == True:
      guild_info = await getInfo(ctx)
      em = discord.Embed(title="Success", description="Everything is set-up, these are your options you provided.", color=discord.Color.green())
      
      em.add_field(name="Session Link", value=f"> {guild_info[1]}", inline=False)
      em.add_field(name="Shutdown Link", value=f"> {guild_info[2]}", inline=False)
      em.add_field(name="Server Emoji", value=f"> {guild_info[3]}", inline=False)
      msg = await convertInto(ctx, self.bot, guild_info[4])
      em.add_field(name="Staff Roles", value=f"> {msg}", inline=False)
      msg = await convertInto(ctx, self.bot, guild_info[5])
      em.add_field(name="Management Roles", value=f"> {msg}", inline=False)
      msg = await convertInto(ctx, self.bot, guild_info[6])
      em.add_field(name="Session Role", value=f"> {msg}", inline=False)
      em.add_field(name="M Command Channel", value=f"> <#{str(guild_info[7]).replace('[', '').replace(']', '')}>", inline=False)
      em.add_field(name="Staff Ping Channel", value=f"> <#{str(guild_info[8]).replace('[', '').replace(']', '')}>", inline=False)
      em.add_field(name="ROBLOX Server Name", value=f"> `{guild_info[9]}`", inline=False)
      em.add_field(name="ROBLOX Server Owner", value=f"> `{guild_info[10]}`", inline=False)
      em.add_field(name="ROBLOX Code", value=f"> `{guild_info[11]}`", inline=False)
      em.add_field(name="Number of Votes", value=f"> `{guild_info[12]}`", inline=False)
      em.add_field(name="M Command Text", value=f"> `{guild_info[13]}`", inline=False)

      await ctx.send(embed=em)
    if is_setup == False:
      em = discord.Embed(title="Canceled", description="Setup has been canceled!", color=discord.Color.red())
      await ctx.send(embed=em)
      
    
    
    
async def setup(bot):
  await bot.add_cog(setup_bot(bot))