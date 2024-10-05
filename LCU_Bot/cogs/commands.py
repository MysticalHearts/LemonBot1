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

reg = r'https\:\/\/media\.discordapp\.net\/attachments\/(A-Za-z0-9\/\-\.\?\=\&)+'
dt = datetime.datetime.now()
timestamp1 = dt.replace(tzinfo=timezone.utc).timestamp()
timestamp = math.floor(timestamp1)


class voteButtons(discord.ui.View):
  def __init__(self, guild_info, bot):
    super().__init__(timeout=None)
    self.votes = 0
    self.votedUsers = []
    self.guild_info = guild_info
    self.bot = bot
    

  @discord.ui.button(label="Vote", style=discord.ButtonStyle.grey)
  async def vote(self, interaction: discord.Interaction, button: discord.ui.Button):
    try:
      #checks to see if user has already voted
      if interaction.user.id in self.votedUsers:
        return await interaction.response.send_message("You cannot unreact to this vote or vote again!", ephemeral=True)
      else:#if user has not votes, append name to list
        self.votedUsers.append(interaction.user.id)
        await interaction.response.send_message("You have just voted to start a SSU!", ephemeral=True)
      
      #adds a vote and opens db to get data
      self.votes += 1
      #vote = int(self.votes)
      con = sqlite3.connect("cogs/data/main_db.db")
      cur = con.cursor()
      res = cur.execute(f"SELECT svote_description, svote_color FROM embeds WHERE guild_id = '{int(interaction.guild.id)}'")
      des = res.fetchone()

      #if theres no color picked for embed, provide this one
      if des[1] == None:
          color = discord.Color.from_rgb(43, 112, 182)
      else:#if color picked than use it
        des1 = des[1]
        des1 = des1[1:-1]
        list = re.split(r',\s?', des1)
        color = discord.Color.from_rgb(int(list[0]), int(list[1]), int(list[2]))

      #check to see if no description was privided, if so use this
      if des[0] == None:
        em = discord.Embed(title=f"{interaction.guild.name} Session Poll", description=f"{self.guild_info[3]} **Management Team** *have decided to start a session poll, vote below if you are willing to attend this session!*\n\nRequired Votes: **{self.guild_info[12]}**", color=color)
      else:#else grab description from db and replace the needed things
        new_des = des[0].replace("{timestamp}", f"<t:{timestamp}:F>")
        new_string1 = new_des.replace("{ro_name}", self.guild_info[9])
        new_string2 = new_string1.replace("{ro_owner}", self.guild_info[10])
        new_string3 = new_string2.replace("{ro_code}", self.guild_info[11])
        new_string4 = new_string3.replace("{emoji}", self.guild_info[3])
        em = discord.Embed(title=f"{interaction.guild.name} Session Poll", description=new_string4, color=color)
      
      #if there was a banner provided, use it
      if self.guild_info[1] != "None":
        em.set_image(url=f"{self.guild_info[1]}")
      else:
        pass

      em.add_field(name="Votes", value=f"{self.votes}")
      

      #edit the message with the new embed or the new amount of voters
      await interaction.message.edit(embed=em)
      
      #checks to see if the number of people voted is same as the required amt to start
      if self.votes == int(self.guild_info[12]):
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT session_description, session_color FROM embeds WHERE guild_id = '{int(interaction.guild.id)}'")
        des = res.fetchone()
        if des[1] == None:
          color = discord.Color.from_rgb(247, 200, 137)
        else:
          des1 = des[1]
          des1 = des1[1:-1]
          list = re.split(r',\s?', des1)
          color = discord.Color.from_rgb(int(list[0]), int(list[1]), int(list[2]))
        if des[0] == None:
          em = discord.Embed(title=f"{interaction.guild.name} Session Startup", description=f"Our ingame server has been started up! If you voted, you must join the server, failure to do so will result in a infraction.\n\nServer Name: **{self.guild_info[9]}**\nServer Owner: **{self.guild_info[10]}**\nServer Code: **{self.guild_info[11]}** (Case Sensitive)\n\n**Issued on:** <t:{timestamp}:F>", color=color)
        else:
          new_des = des[0].replace("{timestamp}", f"<t:{timestamp}:F>")
          new_string1 = new_des.replace("{ro_name}", self.guild_info[9])
          new_string2 = new_string1.replace("{ro_owner}", self.guild_info[10])
          new_string3 = new_string2.replace("{ro_code}", self.guild_info[11])
          new_string4 = new_string3.replace("{emoji}", self.guild_info[3])
          em = discord.Embed(title=f"{interaction.guild.name} Session Startup", description=new_string4, color=color)
        if self.guild_info[1] != "None":
          em.set_image(url=f"{self.guild_info[1]}")
        else:
          pass
        button = Button(style=discord.ButtonStyle.url, label="Click to Join", url=f"https://policeroleplay.community/join/{self.guild_info[11]}")
        view = View()
        view.add_item(button)
        
        
        await interaction.message.edit(embed=em, view=view)
        msg = ""
        for x in self.votedUsers:
          user = interaction.guild.get_member(int(x))
          msg += user.mention
        await interaction.followup.send(f"{self.guild_info[3]} *The following people are required to join the session, failure to join will result in a infraction:*\n{msg}")
      else:
        pass
        
    except Exception as e:
      raise e


class commands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.index = 0
    
  intent = discord.Intents.default()
  intent.message_content = True
  intent.members = True
  bot = commands.Bot(command_prefix="t-", intents=intent)

  @tasks.loop(seconds=480.0)
  async def mreminder(self, ctx: Interaction):
    con = sqlite3.connect("cogs/data/main_db.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM setup WHERE guild_id = '{int(ctx.guild.id)}'")
    result = res.fetchone()
    con.close()
    members = result[4]
    members = members[1:-1]
    members = members.split(f', ')
    msg = ""
    for i in members:
      staff = discord.utils.get(ctx.guild.roles, id=int(i))
      msg += f"{staff.mention}"
    channel = discord.utils.get(ctx.guild.channels, id=result[7])
    em = discord.Embed(title="This is an M Command Reminder", description=f"```{result[13]}```", color=discord.Color.from_rgb(255, 255, 254))
    await channel.send(embed=em, content=f"{msg}")

  @bot.hybrid_command(description="This command will provide all important information about LCU.", with_app_command = True)
  async def info(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    em = discord.Embed(title=f"LCU Information", description=f"LCU is an up and coming utilities bot for roleplay servers, our main focus is for servers in the ER:LC community. LCU allows users to set up custom embeds for things like Server Start Ups, Server Shut Downs, Server Start Up Votes and more! We plan on adding more things to LCU in the near future, somethings you can expect are, a dashboard to have full control over the embed looks and commands, and more!\n\n", color=discord.Color.blue())
    em.add_field(name="Links", value="[Support Server](https://discord.gg/fwafbXMZrT)\n[Bot Invite](https://discord.com/api/oauth2/authorize?client_id=1057325266097156106&permissions=1634705337456&scope=bot)")
    em.add_field(name="Users", value=len(self.bot.users))
    em.add_field(name="Guilds", value=len(self.bot.guilds))
    await ctx.send(embed=em)
    try:
      await ctx.message.delete()
    except:
      pass

  @bot.hybrid_command(description="This command sends the Server Start Up message", with_app_command = True)
  async def session(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      dt = datetime.datetime.now()
      timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
      timestamp = math.floor(timestamp)
      result = await checkManage(ctx)
      guild_info = await getInfo(ctx)
      if result:
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT session_description, session_color FROM embeds WHERE guild_id = '{int(ctx.guild.id)}'")
        des = res.fetchone()
        if des[1] == None:
          color = discord.Color.from_rgb(176, 207, 251)
        else:
          des1 = des[1]
          des1 = des1[1:-1]
          list = re.split(r',\s?', des1)
          color = discord.Color.from_rgb(int(list[0]), int(list[1]), int(list[2]))
        if des[0] == None:
          em = discord.Embed(title=f"{ctx.guild.name} Session Startup", description=f"Our ingame server has been started up! If you voted, you must join the server, failure to do so will result in a infraction.\n\nServer Name: **{guild_info[9]}**\nServer Owner: **{guild_info[10]}**\nServer Code: **{guild_info[11]}** (Case Sensitive)\n\n**Issued on:** <t:{timestamp}:F>", color=color)
        else:
          new_des = des[0].replace("{timestamp}", f"<t:{timestamp}:F>")
          new_string1 = new_des.replace("{ro_name}", guild_info[9])
          new_string2 = new_string1.replace("{ro_owner}", guild_info[10])
          new_string3 = new_string2.replace("{ro_code}", guild_info[11])
          new_string4 = new_string3.replace("{emoji}", guild_info[3])
          em = discord.Embed(title=f"{ctx.guild.name} Session Startup", description=new_string4, color=color)
        if guild_info[1] != "None":
          em.set_image(url=f"{guild_info[1]}")
        else:
          pass
          
        button = Button(style=discord.ButtonStyle.url, label="Click to Join", url=f"https://policeroleplay.community/join/{guild_info[11]}")
        view = View()
        view.add_item(button)

        member = guild_info[6]
        member = member[1:-1]
        role = discord.utils.get(ctx.guild.roles, id=int(member))
        await ctx.reply('Sent!', delete_after = 0, allowed_mentions=discord.AllowedMentions(roles=False, users = False, replied_user=False))
        await ctx.channel.send(content=f"{role.mention}", embed=em, view=view)
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
      

  @bot.hybrid_command(description="*This command sends the Server Shut Down message.*", with_app_command = True)
  async def shutdown(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      dt = datetime.datetime.now()
      timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
      timestamp = math.floor(timestamp)
      
      guild_info = await getInfo(ctx)
      result = await checkManage(ctx)
      if result:
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT shutdown_description, shutdown_color FROM embeds WHERE guild_id = '{int(ctx.guild.id)}'")
        des = res.fetchone()
        if des[1] == None:
          color = discord.Color.from_rgb(247, 200, 137)
        else:
          des1 = des[1]
          des1 = des1[1:-1]
          list = re.split(r',\s?', des1)
          color = discord.Color.from_rgb(int(list[0]), int(list[1]), int(list[2]))
        if des[0] == None:
          em = discord.Embed(title=f"{ctx.guild.name} Session Shutdown", description=f"{guild_info[3]} *Our ingame server has been shutdown. Do not join our server until we start up the server again.*\n\n**Issued on:** <t:{timestamp}:F>", color=color)
        else:
          new_des = des[0].replace("{timestamp}", f"<t:{timestamp}:F>")
          new_string1 = new_des.replace("{ro_name}", guild_info[9])
          new_string2 = new_string1.replace("{ro_owner}", guild_info[10])
          new_string3 = new_string2.replace("{ro_code}", guild_info[11])
          new_string4 = new_string3.replace("{emoji}", guild_info[3])
          em = discord.Embed(title=f"{ctx.guild.name} Session Shutdown", description=new_string4, color=color)
        if guild_info[2] != "None":
          em.set_image(url=f"{guild_info[2]}")
        else:
          pass
        await ctx.reply('Sent!', delete_after = 0, allowed_mentions=discord.AllowedMentions(roles=False, users = False, replied_user=False))
        await ctx.channel.send(embed=em)
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

  @bot.hybrid_command(description="*This command sends the session vote embed.*", with_app_command = True)
  async def svote(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      dt = datetime.datetime.now()
      timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
      timestamp = math.floor(timestamp)
      result = await checkManage(ctx)
      guild_info = await getInfo(ctx)
      if result:
        con = sqlite3.connect("cogs/data/main_db.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT svote_description, svote_color FROM embeds WHERE guild_id = '{int(ctx.guild.id)}'")
        des = res.fetchone()
        if des[1] == None:
          color = discord.Color.from_rgb(43, 112, 182)
        else:
          des1 = des[1]
          des1 = des1[1:-1]
          list = re.split(r',\s?', des1)
          color = discord.Color.from_rgb(int(list[0]), int(list[1]), int(list[2]))
        if des[0] == None:
          em = discord.Embed(title=f"{ctx.guild.name} Session Poll", description=f"{guild_info[3]} **Management Team** *have decided to start a session poll, vote below if you are willing to attend this session!*\n\nRequired Votes: **{guild_info[12]}**", color=color)
        else:
          new_des = des[0].replace("{timestamp}", f"<t:{timestamp}:F>")
          new_string1 = new_des.replace("{ro_name}", guild_info[9])
          new_string2 = new_string1.replace("{ro_owner}", guild_info[10])
          new_string3 = new_string2.replace("{ro_code}", guild_info[11])
          new_string4 = new_string3.replace("{emoji}", guild_info[3])
          em = discord.Embed(title=f"{ctx.guild.name} Session Poll", description=new_string4, color=color)
        if guild_info[1] != "None":
          em.set_image(url=f"{guild_info[1]}")
        else:
          pass
        view = voteButtons(guild_info, self.bot)
        member = guild_info[6]
        member = member[1:-1]
        role = discord.utils.get(ctx.guild.roles, id=int(member))
        await ctx.reply('Sent!', delete_after = 0, allowed_mentions=discord.AllowedMentions(roles=False, users = False, replied_user=False))
        await ctx.channel.send(content=f"@here {role.mention}", embed=em, view=view)
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

  @bot.hybrid_command(description="*This command will ping your staff roles provided on setup.*", with_app_command = True) 
  #@commands.cooldown(1,300, commands.BucketType.guild)
  async def staff(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        channel = discord.utils.get(ctx.guild.channels, id=guild_info[8])
        em = discord.Embed(title="All Moderators", description=f"{ctx.author.mention} needs help ingame, go help them out!", color=discord.Color.from_rgb(103, 156, 255))
        member = guild_info[4]
        member1 = member[1:-1]
        member_list = re.split(r',\s?', member1)
        msg = ""
        for member in member_list:
          staff = discord.utils.get(ctx.guild.roles, id=int(member))
          if staff:
            msg += f"{staff.mention}"
        await channel.send(content=f"{msg}", embed=em)
        await ctx.reply('Sent!', delete_after = 0, allowed_mentions=discord.AllowedMentions(roles=False, users = False, replied_user=False))
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

  @bot.hybrid_command(description="*This will ping your management roles provided on setup.*", with_app_command = True)
  #@commands.cooldown(1,300, commands.BucketType.guild)
  async def manage(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        channel = discord.utils.get(ctx.guild.channels, id=guild_info[8])
        em = discord.Embed(title="Management & Administration", description=f"{ctx.author.mention} needs help ingame, go help them out!", color=discord.Color.from_rgb(255, 191, 95))
        member = guild_info[5]
        member = member[1:-1]
        member_list = re.split(r',\s?', member)
        msg = ""
        for member in member_list:
          staff = discord.utils.get(ctx.guild.roles, id=int(member))
          msg += f"{staff.mention}"
        await ctx.reply('Sent!', delete_after = 0, allowed_mentions=discord.AllowedMentions(roles=False, users = False, replied_user=False))
        await channel.send(content=f"{msg}", embed=em)
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

  @bot.hybrid_command(description="*This command will ping your staff roles provided on setup*", with_app_command = True)
  #@commands.cooldown(1,300, commands.BucketType.guild) 
  async def all(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        channel = discord.utils.get(ctx.guild.channels, id=guild_info[8])
        em = discord.Embed(title="All Staff Members", description=f"{ctx.author.mention} needs help ingame, go help them out!", color=discord.Color.from_rgb(255, 255, 254))
        role1 = discord.utils.get(ctx.guild.roles, id=1057056728002338929)
        member1 = guild_info[5]
        member2 = guild_info[4]
        member1 = member1[1:-1]
        member2 = member2[1:-1]
        member_list1 = re.split(r',\s?', member1)
        member_list2 = re.split(r',\s?', member2)
        msg = ""
        for member in member_list1:
          staff = discord.utils.get(ctx.guild.roles, id=int(member))
          msg += f"{staff.mention}"
        for member in member_list2:
          staff = discord.utils.get(ctx.guild.roles, id=int(member))
          msg += f"{staff.mention}"
        await ctx.reply('Sent!', delete_after = 0, allowed_mentions=discord.AllowedMentions(roles=False, users = False, replied_user=False))
        await channel.send(content=f"{msg}", embed=em)
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

  @bot.hybrid_command(description="*This will start your m command reminders.*", with_app_command = True) 
  async def on(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:

        em = discord.Embed(title="M command reminders are now enabled", description="", color=discord.Color.green())
        await ctx.send(embed=em)
        self.mreminder.start(ctx)
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

  @bot.hybrid_command(description="*This will stop your m command reminders.*", with_app_command = True)
  async def off(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        em = discord.Embed(title="M command reminders are now disabled", description="", color=discord.Color.red())
        await ctx.send(embed=em)
        self.mreminder.cancel()
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

  @bot.hybrid_command(description="*This will make an embed with your provided message.*", with_app_command = True)
  async def embed(self, ctx: commands.Context, *, message: str):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        em = discord.Embed(title=f"{ctx.guild.name}", description=message, color=discord.Color.from_rgb(255, 255, 254))
        await ctx.reply('Sent!', delete_after = 0, allowed_mentions=discord.AllowedMentions(roles=False, users = False, replied_user=False))
        await ctx.channel.send(embed=em)
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

  @bot.hybrid_command(description="*This will send a message to the channel with the given message.*", with_app_command = True)
  async def say(self, ctx: commands.Context, *, message: str):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      result = await checkStaff(ctx)
      guild_info = await getInfo(ctx)
      if result:
        await ctx.reply('Sent!', delete_after = 0, allowed_mentions=discord.AllowedMentions(roles=False, users = False, replied_user=False))
        await ctx.channel.send(message)
        try:
          await ctx.message.delete()
        except:
          pass
        return
      else:
        em = discord.Embed(title="Missing Permissions.", description="You are missing the needed permissions to run this command, make sure you have the `staff/management` roles that you setup during the bot setup.", color=discord.Color.red())
        await ctx.send(embed=em)
    else:
      return 

  @bot.hybrid_command(description="*This will send your advertisement to the channel.*", with_app_command = True)
  async def ad(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
    setup = await checkSetUp(ctx)
    if setup:
      guild_info = await getInfo(ctx)
      em = discord.Embed(title="Our Advertisement", description=f"```{guild_info[14]}```", color = discord.Color.from_rgb(47,49,54))
      await ctx.send(embed=em)
      try:
        await ctx.message.delete()
      except:
        pass
    else:
      return
    
async def setup(bot):
  await bot.add_cog(commands(bot))