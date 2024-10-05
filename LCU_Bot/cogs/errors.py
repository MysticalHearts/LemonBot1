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

class errors(commands.Cog):
  def __init__ (self, bot):
      self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(title="Please state all requirements!", description="You can join our [Support Server](https://discord.gg/fwafbXMZrT).")
      await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(title="You do not have the permission to run this command!", description="You can join our [Support Server](https://discord.gg/fwafbXMZrT).")
      await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
      embed = discord.Embed(title="Command not found!", description="You can join our [Support Server](https://discord.gg/fwafbXMZrT).")
      await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
      embed = discord.Embed(title="Cooldown!", description=f"This command is on cooldown, please try again in `{round(error.retry_after)}` seconds.\n\nYou can join our [Support Server](https://discord.gg/fwafbXMZrT).")
      await ctx.send(embed=embed)
    elif isinstance(error, commands.NotOwner):
      embed = discord.Embed(title="This command is an owner only command for the bot owner!", description=f"You can join our [Support Server](https://discord.gg/fwafbXMZrT).")
      await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
      em = discord.Embed(title="Bad Argument", description="You inputted something wrong, please try again!\n\nYou can join our [Support Server](https://discord.gg/fwafbXMZrT).")
      await ctx.send(embed=em)
    elif isinstance(error, commands.CheckFailure):
      pass
    elif discord.Forbidden:
      em = discord.Embed(title="Missing Permissions", description="Please make sure I can send messages and have all permissions to interact in the channels.\n\nYou can join our [Support Server](https://discord.gg/fwafbXMZrT).")
      await ctx.send(embed=em)
    else:
      channel = self.bot.get_channel(1059547910175477872)
      embed = discord.Embed(title="ERROR!", description=":x: Something went wrong!\n\nPlease join our [Support Server](https://discord.gg/fwafbXMZrT).", color=discord.Color.red())
      embed.add_field(name="Error", value=f"||{error}||")
      await ctx.send(embed=embed)
      embed2 = discord.Embed(title="Something went wrong!", description=f"Error: `{error}` in command **{ctx.command}**", color=discord.Color.blue())
      embed2.set_footer(text=f"Done by: {ctx.author.name}#{ctx.author.discriminator} in {ctx.guild.name}")
      await channel.send(embed=embed2)

async def setup(bot):
  await bot.add_cog(errors(bot))