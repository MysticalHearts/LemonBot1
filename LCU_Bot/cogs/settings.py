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
from PIL import ImageColor
import re

class SettingsPanel(discord.ui.View):
  def __init__(self, ctx, bot):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.bot = bot
  
#this is the button to start a users shift
  @discord.ui.button(label="Embeds", style=discord.ButtonStyle.grey)
  async def embed_changer(self, ctx: Interaction, button: discord.ui.Button):
    em = discord.Embed(title=f"Embed Changer", description=f"Here you will be able to 100% fully customize the Session, Shutdown, and svote embeds to your liking.")
    select_menu = Select(placeholder="Select An Embed to Change", options=[
    discord.SelectOption(label="Session", value="1", description="Edit the session emebed"),
    discord.SelectOption(label="Shutdown", value="2", description="Edit the shutdown embed"),
    discord.SelectOption(label="SVote", value="3", description="Edit the svote embed"),
    ])

    select_menu2 = Select(placeholder="Select An Embed to Reset", options=[
    discord.SelectOption(label="Session", value="1", description="Reset the session embed"),
    discord.SelectOption(label="Shutdown", value="2", description="Reset the shutdown embed"),
    discord.SelectOption(label="SVote", value="3", description="Reset the SVote embed"),
    ])

    async def callback(ctx: Interaction):
      try:
        if select_menu.values[0] == "1":
          await ctx.message.delete()
          await sessionChange(ctx, self.bot)
        elif select_menu.values[0] == "2":
          await ctx.message.delete()
          await shutdownChange(ctx, self.bot)
        elif select_menu.values[0] == "3":
          await ctx.message.delete()
          await svoteChange(ctx, self.bot)
        else:
          print("Something Went Wrong")
      except Exception as e:
        raise e

    async def callback2(ctx: Interaction):
      try:
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        
        if select_menu2.values[0] == "1":
          #await ctx.message.delete()
          cur.execute(f"UPDATE embeds SET session_description = NULL WHERE guild_id = '{int(ctx.guild.id)}'")
          con.commit()
          con.close()
          await ctx.response.send_message("Your embed is now reset", ephemeral=True)
        elif select_menu2.values[0] == "2":
          #await ctx.message.delete()
          cur.execute(f"UPDATE embeds SET shutdown_description = NULL WHERE guild_id = '{int(ctx.guild.id)}'")
          con.commit()
          con.close()
          await ctx.response.send_message("Your embed is now reset", ephemeral=True)
        elif select_menu2.values[0] == "3":
          #await ctx.message.delete()
          cur.execute(f"UPDATE embeds SET svote_description = NULL WHERE guild_id = '{int(ctx.guild.id)}'")
          con.commit()
          con.close()
          await ctx.response.send_message("Your embed is now reset", ephemeral=True)
        else:
          print("Something Went Wrong")
      except Exception as e:
        raise e
    
    select_menu.callback = callback
    select_menu2.callback = callback2
    view = View()
    view.add_item(select_menu)
    view.add_item(select_menu2)
    msg = await ctx.response.send_message(embed=em, view=view)

  @discord.ui.button(label="Colors", style=discord.ButtonStyle.grey)
  async def color_changer(self, ctx: Interaction, button: discord.ui.Button):
    em = discord.Embed(title=f"Color Changer", description=f"Here you will be able to change the color of embeds.")
    select_menu = Select(placeholder="Select An Embed to Change", options=[
    discord.SelectOption(label="Session", value="1", description="Change the session command color"),
    discord.SelectOption(label="Shutdown", value="2", description="Change the shutdown command color"),
    discord.SelectOption(label="SVote", value="3", description="Change the svote command color"),
    ])

    async def callback(ctx: Interaction):
      await ctx.message.delete()
      em = discord.Embed(title=f"Please provide a color in hex format(ex: `#54FF00`)")
      con = sqlite3.connect("cogs/data/main_db.db")
      cur = con.cursor()
      if select_menu.values[0] == "1":
        embed = await ctx.response.send_message(embed=em)
        msg2 = await self.bot.wait_for('message', timeout=None, check=lambda message: message.author == ctx.user)
        match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', msg2.content)
        if not match:
          em2 = discord.Embed(title=f"That is not a hex value, please provide a color in hex format(ex: `#54FF00`)")
          return await ctx.followup.send(embed=em2)
        else:
          pass
        rgb = ImageColor.getrgb(msg2.content)
        cur.execute(f"UPDATE embeds SET session_color = '{rgb}' WHERE guild_id = '{int(ctx.guild.id)}'")
        await ctx.followup.send("Your embed color is now changed", ephemeral=True)
        await msg2.delete()
      elif select_menu.values[0] == "2":
        embedm = await ctx.response.send_message(embed=em)
        msg2 = await self.bot.wait_for('message', timeout=None, check=lambda message: message.author == ctx.user)
        rgb = ImageColor.getrgb(msg2.content)
        cur.execute(f"UPDATE embeds SET shutdown_color = '{rgb}' WHERE guild_id = '{int(ctx.guild.id)}'")
        await ctx.response.send_message("Your embed color is now changed", ephemeral=True)
        
      elif select_menu.values[0] == "3":
        embedm = await ctx.response.send_message(embed=em)
        msg2 = await self.bot.wait_for('message', timeout=None, check=lambda message: message.author == ctx.user)
        rgb = ImageColor.getrgb(msg2.content)
        cur.execute(f"UPDATE embeds SET svote_color = '{rgb}' WHERE guild_id = '{int(ctx.guild.id)}'")
        await ctx.response.send_message("Your embed color is now changed", ephemeral=True)
      con.commit()
      con.close()
      
    
    select_menu.callback = callback
    view = View()
    view.add_item(select_menu)
    msg = await ctx.response.send_message(embed=em, view=view)
  
class settings(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  intent = discord.Intents.default()
  intent.message_content = True
  intent.members = True
  bot = commands.Bot(command_prefix="t-", intents=intent)

  @bot.hybrid_command(description="*This will allow you to change some settings of the bot.*", with_app_command = True)
  #@commands.has_permissions(administrator=True)
  async def settings(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkManage(ctx)
      if result:
        #await ctx.message.delete()
        em = discord.Embed(title=f"Settings Page", description=f"Each button is setting that can be 100% customized to your liking. The `Embeds` button is used to edit the embeds of the bot to your liking. The `Colors` button is used to edit the color of any embed to your liking", color=discord.Color.blue())
        view = SettingsPanel(ctx, self.bot)
        msg = await ctx.send(embed=em, view=view)
        await self.bot.wait_for('interaction', timeout=None, check=lambda message: message.user == ctx.author)
        await msg.delete()
        return
      else:
        return
    else:
      return
    
async def setup(bot):
  await bot.add_cog(settings(bot))