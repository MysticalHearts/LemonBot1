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
from discord.ext.commands import CommandNotFound

class MSessionBanner(discord.ui.Modal, title='Configuration'):
    answer = discord.ui.TextInput(label="Session Banner", placeholder="Must be from https://cdn.discordapp.com/attachments")

    async def on_submit(self, ctx: Interaction):
      answer = str(self.answer)
      if answer.startswith("https://cdn.discordapp.com/attachments"):
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        cur.execute(f"UPDATE setup SET session_banner_link = '{self.answer}' WHERE guild_id = '{int(ctx.guild.id)}'")
        con.commit()
        con.close()
        await ctx.response.send_message(f"It has now been configured!", ephemeral=True)
      else:
        await ctx.response.send_message(f"Please retry, it must be from https://cdn.discordapp.com/attachments", ephemeral=True)

class MShutdownBanner(discord.ui.Modal, title='Configuration'):
    answer = discord.ui.TextInput(label="Shutdown Banner", placeholder="Must be from https://cdn.discordapp.com/attachments")

    async def on_submit(self, ctx: Interaction):
      answer = str(self.answer)
      if answer.startswith("https://cdn.discordapp.com/attachments"):
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        cur.execute(f"UPDATE setup SET shutdown_banner_link = '{self.answer}' WHERE guild_id = '{int(ctx.guild.id)}'")
        con.commit()
        con.close()
        await ctx.response.send_message(f"It has now been configured!", ephemeral=True)
      else:
        await ctx.response.send_message(f"Please retry, it must be from https://cdn.discordapp.com/attachments", ephemeral=True)

class MEmoji(discord.ui.Modal, title='Configuration'):
    answer = discord.ui.TextInput(label="Emoji", placeholder="Must be a custom emoji.")

    async def on_submit(self, ctx: Interaction):
      answer = str(self.answer)
      if answer.startswith("<") and answer.endswith(">"):
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        cur.execute(f"UPDATE setup SET emoji_id = '{self.answer}' WHERE guild_id = '{int(ctx.guild.id)}'")
        con.commit()
        con.close()
        await ctx.response.send_message(f"It has now been configured!", ephemeral=True)
      else:
        await ctx.response.send_message(f"Please retry, it must start with < and end with >. Example: <emojiname:emojiid>", ephemeral=True)
#-----------------------------------------

class MServerName(discord.ui.Modal, title='Configuration'):
    answer = discord.ui.TextInput(label="Server Name")

    async def on_submit(self, ctx: Interaction):
      answer = str(self.answer)
      
      con = sqlite3.connect("cogs/data/main_db.db")
      cur = con.cursor()
      cur.execute(f"UPDATE setup SET server_name = '{answer}' WHERE guild_id = '{int(ctx.guild.id)}'")
      con.commit()
      con.close()
      await ctx.response.send_message(f"It has now been configured!", ephemeral=True)

class MServerOwner(discord.ui.Modal, title='Configuration'):
    answer = discord.ui.TextInput(label="Server Owner")

    async def on_submit(self, ctx: Interaction):
      answer = str(self.answer)
      
      con = sqlite3.connect("cogs/data/main_db.db")
      cur = con.cursor()
      cur.execute(f"UPDATE setup SET server_owner = '{answer}' WHERE guild_id = '{int(ctx.guild.id)}'")
      con.commit()
      con.close()
      await ctx.response.send_message(f"It has now been configured!", ephemeral=True)

class MCode(discord.ui.Modal, title='Configuration'):
    answer = discord.ui.TextInput(label="ROBLOX Code")

    async def on_submit(self, ctx: Interaction):
      answer = str(self.answer)
      
      con = sqlite3.connect("cogs/data/main_db.db")
      cur = con.cursor()
      cur.execute(f"UPDATE setup SET server_code = '{answer}' WHERE guild_id = '{int(ctx.guild.id)}'")
      con.commit()
      con.close()
      await ctx.response.send_message(f"It has now been configured!", ephemeral=True)

class MReminderText(discord.ui.Modal, title='Configuration'):
    answer = discord.ui.TextInput(label="M Command Text", style=discord.TextStyle.paragraph)

    async def on_submit(self, ctx: Interaction):
      answer = str(self.answer)
      
      con = sqlite3.connect("cogs/data/main_db.db")
      cur = con.cursor()
      cur.execute(f"UPDATE setup SET m_command_text = '{answer}' WHERE guild_id = '{int(ctx.guild.id)}'")
      con.commit()
      con.close()
      await ctx.response.send_message(f"It has now been configured!", ephemeral=True)

class MVotes(discord.ui.Modal, title='Configuration'):
    answer = discord.ui.TextInput(label="Votes", placeholder = "Must be a number")

    async def on_submit(self, ctx: Interaction):
      try:
        print(self.answer)
        answer = str(self.answer)
        answer = int(answer)
      except Exception as e:
        return await ctx.response.send_message(f"Please provide a number(e.g 1, 2, 3)", ephemeral=True)
      
      con = sqlite3.connect("cogs/data/main_db.db")
      cur = con.cursor()
      cur.execute(f"UPDATE setup SET vote_number = '{answer}' WHERE guild_id = '{int(ctx.guild.id)}'")
      con.commit()
      con.close()
      await ctx.response.send_message(f"It has now been configured!", ephemeral=True)
      

class MAdvert(discord.ui.Modal, title='Configuration'):
    answer = discord.ui.TextInput(label="Advertisement", style=discord.TextStyle.paragraph)

    async def on_submit(self, ctx: Interaction):
      answer = str(self.answer)
      
      con = sqlite3.connect("cogs/data/main_db.db")
      cur = con.cursor()
      cur.execute(f"UPDATE setup SET advertisement = '{answer}' WHERE guild_id = '{int(ctx.guild.id)}'")
      con.commit()
      con.close()
      await ctx.response.send_message(f"It has now been configured!", ephemeral=True)
        
class config(commands.Cog):
    def __init__ (self, bot):
      self.bot = bot
      self.staff_roles_returns = []
      
    intent = discord.Intents.default()
    intent.message_content = True
    intent.members = True
    bot = commands.Bot(command_prefix="t-", intents=intent)

    @bot.hybrid_command(description="This will allow you to reconfigure specific features within LCU", with_app_command = True)
    async def config(self, ctx: commands.Context):
      await ctx.defer(ephemeral = False)
      setup = await checkSetUp(ctx)
      if setup:
        result = await checkManage(ctx)
        if result:

          #------------------------------------------------------
          async def callback1(ctx: Interaction):
            if select_menu1.values[0] == "1":
              await ctx.response.send_modal(MSessionBanner())
              return
            elif select_menu1.values[0] == "2":
              await ctx.response.send_modal(MShutdownBanner())
              return
            elif select_menu1.values[0] == "3":
              await ctx.response.send_modal(MEmoji())
              return
          #---------------------------------------------------
              

          async def callback2(ctx: Interaction):
            staff_roles_returns = []
            manage_roles_returns = []
            async def role1callback(ctx: Interaction):
              for role in select_role1.values:
                cstaff_Roles = discord.utils.get(ctx.guild.roles, name=str(role))
                staff_roles_returns.append(cstaff_Roles.id)
              con = sqlite3.connect("cogs/data/main_db.db")
              cur = con.cursor()
              cur.execute(f"UPDATE setup SET staff_roles_id = '{staff_roles_returns}' WHERE guild_id = '{int(ctx.guild.id)}'")
              con.commit()
              con.close()
              await ctx.message.delete()
              await ctx.response.send_message(content = f"Your staff roles has been changed", embed=None, view = None, ephemeral=True)

            async def role2callback(ctx: Interaction):
              
              for role in select_role2.values:
                cmanage_Roles = discord.utils.get(ctx.guild.roles, name=str(role))
                cmanage_Roles = cmanage_Roles.id
                manage_roles_returns.append(cmanage_Roles)
              con = sqlite3.connect("cogs/data/main_db.db")
              cur = con.cursor()
              cur.execute(f"UPDATE setup SET management_roles_id = '{staff_roles_returns}' WHERE guild_id = '{int(ctx.guild.id)}'")
              con.commit()
              con.close()
              await ctx.message.delete()
              await ctx.response.send_message(content = f"Your management roles has been changed", embed=None, view = None, ephemeral=True)

            async def role3callback(ctx: Interaction):
              shift_role = discord.utils.get(ctx.guild.roles, name=str(select_role3.values[0]))
              con = sqlite3.connect("cogs/data/main_db.db")
              cur = con.cursor()
              cur.execute(f"UPDATE setup SET session_role_id = '{shift_role.id}' WHERE guild_id = '{int(ctx.guild.id)}'")
              con.commit()
              con.close()
              await ctx.message.delete()
              await ctx.response.send_message(content = f"Your session role has been changed", embed=None, view = None, ephemeral=True)

            async def channel1callback(ctx: Interaction):
              shift_channel = discord.utils.get(ctx.guild.channels, name=str(select_channel1.values[0]))
              con = sqlite3.connect("cogs/data/main_db.db")
              cur = con.cursor()
              cur.execute(f"UPDATE setup SET m_command_channel = '{shift_channel.id}' WHERE guild_id = '{int(ctx.guild.id)}'")
              con.commit()
              con.close()
              await ctx.message.delete()
              await ctx.response.send_message(content = f"Your m command channel has been changed", embed=None, view = None, ephemeral=True)
              
              
            async def channel2callback(ctx: Interaction):
              shift_channel = discord.utils.get(ctx.guild.channels, name=str(select_channel2.values[0]))
              con = sqlite3.connect("cogs/data/main_db.db")
              cur = con.cursor()
              cur.execute(f"UPDATE setup SET ping_channel = '{shift_channel.id}' WHERE guild_id = '{int(ctx.guild.id)}'")
              con.commit()
              con.close()
              await ctx.message.delete()
              await ctx.response.send_message(content = f"Your staff request channel has been changed", embed=None, view = None, ephemeral=True)
              

            if select_menu2.values[0] == "1":
              em = discord.Embed(title=f"", description=f"What are your staff team role(s) (Please do not select for management roles for this)?", color = discord.Color.green())
              select_role1 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=10)
              select_role1.callback = role1callback
              view=View()
              view.add_item(select_role1)
              await ctx.response.send_message(embed = em, view=view)
              await self.bot.wait_for('interaction', timeout=None, check=lambda message: message.user == ctx.user)
              return
            elif select_menu2.values[0] == "2":
              em = discord.Embed(title=f"", description=f"What are your management team role(s) (Please do not select for staff team roles.)?", color = discord.Color.green())
              select_role2 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=10)
              select_role2.callback = role2callback
              view=View()
              view.add_item(select_role2)
              await ctx.response.send_message(embed = em, view=view)
              await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == ctx.author)
              return
            elif select_menu2.values[0] == "3":
              em = discord.Embed(title=f"", description=f"What is your session/SSU role?", color = discord.Color.green())
              select_role3 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=1)
              select_role3.callback = role3callback
              view=View()
              view.add_item(select_role3)
              await ctx.response.send_message(embed = em, view=view)
              await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == ctx.author)
              return
            elif select_menu2.values[0] == "4":
              em = discord.Embed(title=f"", description=f"Where would you like your :m or :h reminders to be sent?", color = discord.Color.green())
              select_channel1 = discord.ui.ChannelSelect(placeholder="Select A Channel", min_values=1, max_values=1)
              select_channel1.callback = channel1callback
              view=View()
              view.add_item(select_channel1)
              await ctx.response.send_message(embed = em, view=view)
              await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == ctx.author)
              return
            elif select_menu2.values[0] == "5":
              em = discord.Embed(title=f"", description=f"Where would you like your staff request commands to be sent to? (this includes the -all, -staff and -manage commands.)", color = discord.Color.green())
              select_channel2 = discord.ui.ChannelSelect(placeholder="Select A Channel", min_values=1, max_values=1)
              select_channel2.callback = channel2callback
              view=View()
              view.add_item(select_channel2)
              await ctx.response.send_message(embed = em, view=view)
              await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == ctx.author)
              return
          #---------------------------------------------------
          async def callback3(ctx: Interaction):
            if select_menu3.values[0] == "1":
              await ctx.response.send_modal(MServerName())
              return
            elif select_menu3.values[0] == "2":
              await ctx.response.send_modal(MServerOwner())
              return
            elif select_menu3.values[0] == "3":
              await ctx.response.send_modal(MCode())
              return
            elif select_menu3.values[0] == "4":
              await ctx.response.send_modal(MReminderText())
              return
            elif select_menu3.values[0] == "5":
              await ctx.response.send_modal(MVotes())
              return
            elif select_menu3.values[0] == "6":
              await ctx.response.send_modal(MAdvert())
              return
          #-----------------------------------------------------
          em = discord.Embed(title="Reconfiguration", description="Please pick the section you wish to reconfigure below.")
          select_menu1 = Select(placeholder="Select A Feature to Change", options=[
          discord.SelectOption(label="Session Banner", value="1", description="Change the session banner"),
          discord.SelectOption(label="Shutdown Banner", value="2", description="Change the shutdown banner"),
          discord.SelectOption(label="Emoji", value="3", description="Change the emoji"),
          ])

          select_menu2 = Select(placeholder="Select A Feature to Change", options=[
          discord.SelectOption(label="Staff Roles", value="1", description="Change the staff roles"),
          discord.SelectOption(label="Management Roles", value="2", description="Change the management roles"),
          discord.SelectOption(label="Session Role", value="3", description="Change the session role"),
          discord.SelectOption(label="M Reminder Channel", value="4", description="Change the m reminder channel"),
          discord.SelectOption(label="Staff Request Channel", value="5", description="Change the staff request channel"),
          ])

          select_menu3 = Select(placeholder="Select A Feature to Change", options=[
          discord.SelectOption(label="Server Name", value="1", description="Change the server roblox name"),
          discord.SelectOption(label="Server Owner", value="2", description="Change the server roblox owner"),
          discord.SelectOption(label="Code", value="3", description="Change the server roblox code"),
          discord.SelectOption(label="M Reminder Text", value="4", description="Change the m reminder text"),
          discord.SelectOption(label="Votes", value="5", description="Change the number of votes needed for svote"),
          discord.SelectOption(label="Advertisement", value="6", description="Change the advertisement"),
          ])

          select_menu1.callback = callback1
          select_menu2.callback = callback2
          select_menu3.callback = callback3
          view = View()
          view.add_item(select_menu1)
          view.add_item(select_menu2)
          view.add_item(select_menu3)
          await ctx.send(embed=em, view=view)
          return
        else:
          em = discord.Embed(title="Missing Permissions.", description="You are missing the needed permissions to run this command, make sure you have the `staff/management` roles that you setup during the bot setup.", color=discord.Color.red())
          await ctx.send(embed=em)
          return
      else:
        return


  

async def setup(bot):
  await bot.add_cog(config(bot))