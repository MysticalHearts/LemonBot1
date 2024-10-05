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

class roles(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  intent = discord.Intents.default()
  intent.message_content = True
  intent.members = True
  bot = commands.Bot(command_prefix="t-", intents=intent)
  bot.remove_command("help")
    
  @bot.hybrid_command(description="*This is what you are seeing right now.*", with_app_command = True)
  async def promote(self, ctx: commands.Context, member: discord.Member, role: discord.Role, *, reason: str = "None Was Specified"):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        if ctx.author == member:
            await ctx.message.delete()
            em = discord.Embed(title="", description="You cant do that, your trying to promote yourself!")
            return await ctx.send(embed=em)
        elif ctx.author.top_role.position <= role.position:
            await ctx.message.delete()
            em = discord.Embed(title="", description="Please make sure your top role is higher than the one your trying to add!")
            return await ctx.send(embed=em)
        elif role in member.roles:
            await ctx.message.delete()
            em = discord.Embed(title="", description=f"{member.mention} already has {role.mention}.")
            return await ctx.send(embed=em)
        else:
            dt = datetime.datetime.now()
            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
            timestamp = math.floor(timestamp)
        
            con = sqlite3.connect("cogs/data/main_db.db")
            cur = con.cursor()
            cur.execute(f"INSERT INTO promos(user_id, promo_reason, moderator, promo_role_id) VALUES ('{member.id}', '{reason}', '{ctx.author.id}', '{role.id}')") 
            con.commit()
            con.close()
            await member.add_roles(role)
            em = discord.Embed(title=f"{guild_info[3]} Staff Promotion", description=f"The HR Team has decided to promote you. Congrats!\n\n> **Username:** {member.name}\n> **Reason:** {reason}\n> **Role:** {role.name} \n > **Submission Date:** <t:{timestamp}:F>", color=discord.Color.from_rgb(255, 255, 254))
            #em.set_footer(text=f"Your Punishment ID is: {warn_id}")
            await ctx.send(embed=em)
            try:
                await member.send(embed=em)
            except:
                await ctx.send("I can't send a message to this user!")
            try:
                await ctx.message.delete()
            except:
                pass
            return
      else:
          em = discord.Embed(title="Missing Permissions.", description="Your highest role is lower than the role you want to assign.", color=discord.Color.from_rgb(255, 255, 254))
          await ctx.send(embed=em)
          return
    else:
        return

  @bot.hybrid_command(description="This command is used to search a users promotions (e.g -search_promos @user)", with_app_command = True)
  async def search_promos(self, ctx: commands.Context, member: discord.Member):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT user_id, promo_reason, moderator, promo_role_id FROM promos WHERE user_id = '{member.id}'")
        result = res.fetchall()
        if not result:
          em = discord.Embed(title=f"", description=f"This member is not in our database", color=discord.Color.from_rgb(255, 255, 254))
          return await ctx.send(embed=em)

        em = discord.Embed(title=f"{member}", description=f"These are the users promotions", color=discord.Color.from_rgb(255, 255, 254))
        for warn in result:
          em.add_field(name=f"{discord.utils.get(ctx.guild.roles, id=int(warn[3]))}", value=f"Reason: {warn[1]}\nModerator: <@{str(warn[2]).replace('[', '').replace(']', '')}>")
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



  @bot.hybrid_command(description="*This is what you are seeing right now.*", with_app_command = True)
  async def demote(self, ctx: commands.Context, member: discord.Member, role: discord.Role, *, reason: str = "None Was Specified"):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        if ctx.author == member:
            await ctx.message.delete()
            em = discord.Embed(title="", description="You cant do that, your trying to promote yourself!")
            return await ctx.send(embed=em)
        elif ctx.author.top_role.position <= role.position:
            await ctx.message.delete()
            em = discord.Embed(title="", description="Please make sure your top role is higher than the one your trying to remove!")
            return await ctx.send(embed=em)
        elif role not in member.roles:
            await ctx.message.delete()
            em = discord.Embed(title="", description=f"{member.mention} does not have {role.mention}.")
            return await ctx.send(embed=em)
        else:
            dt = datetime.datetime.now()
            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
            timestamp = math.floor(timestamp)
        
            con = sqlite3.connect("cogs/data/main_db.db")
            cur = con.cursor()
            cur.execute(f"INSERT INTO demos(user_id, demo_reason, moderator, demo_role_id) VALUES ('{member.id}', '{reason}', '{ctx.author.id}', '{role.id}')") 
            con.commit()
            con.close()
            await member.remove_roles(role)
            em = discord.Embed(title=f"{guild_info[3]} Staff Demotion", description=f"The HR Team has decided to demote you. Please do not start any drama about this. \n\n> **Username:** {member.name}\n> **Reason:** {reason}\n> **Role:** {role.name} \n > **Submission Date:** <t:{timestamp}:F>", color=discord.Color.from_rgb(255, 255, 254))
            #em.set_footer(text=f"Your Punishment ID is: {warn_id}")
            await ctx.send(embed=em)
            try:
                await member.send(embed=em)
            except:
                await ctx.send("I can't send a message to this user!")
            try:
                await ctx.message.delete()
            except:
                pass
            return
      else:
          em = discord.Embed(title="Missing Permissions.", description="Your highest role is lower than the role you want to assign.", color=discord.Color.from_rgb(255, 255, 254))
          await ctx.send(embed=em)
          return
    else:
        return

  @bot.hybrid_command(description="This command is used to search a users demotions (e.g -search_demos @user)", with_app_command = True)
  async def search_demos(self, ctx: commands.Context, member: discord.Member):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT user_id, demo_reason, moderator, demo_role_id FROM demos WHERE user_id = '{member.id}'")
        result = res.fetchall()
        if not result:
          em = discord.Embed(title=f"", description=f"This member is not in our database", color=discord.Color.from_rgb(255, 255, 254))
          return await ctx.send(embed=em)

        em = discord.Embed(title=f"{member}", description=f"These are the users promotions", color=discord.Color.from_rgb(255, 255, 254))
        for warn in result:
          em.add_field(name=f"{discord.utils.get(ctx.guild.roles, id=int(warn[3]))}", value=f"Reason: {warn[1]}\nModerator: <@{str(warn[2]).replace('[', '').replace(']', '')}>")
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
  await bot.add_cog(roles(bot))