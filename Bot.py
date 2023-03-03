from colorama import init, Fore, Back, Style
from discord.ext import commands
from discord import app_commands
import os, configparser, logging
import discord

# Setup & Config

Logo = r'''
   _                   
  /_\  _   _ _ __ __ _ 
 //_\\| | | | '__/ _` |
/  _  \ |_| | | | (_| |
\_/ \_/\__,_|_|  \__,_|               
'''[1:]

with open('Config.ini', 'r') as Config:
	config = configparser.ConfigParser()
	config.read_file(Config)
	Sections = config.sections()
	Token = config.get(Sections[0], 'Token').replace("'", "")
	Prefix = config.get(Sections[0], 'Prefix').replace("'", "")
	Owner = config.get(Sections[0], 'Owner').replace("'", "")
	Status = config.get(Sections[0], 'Status').replace("'", "")

# Example Config.ini

# [Bot]
# Token = 'Your Token'
# Prefix = 'Your Prefix'
# Owner = 'Your ID'
# Status = 'Bot Status'

logging.basicConfig(level=logging.INFO, format=f'{Fore.WHITE}[{Fore.LIGHTBLUE_EX}%(asctime)s{Fore.WHITE}] ({Fore.LIGHTRED_EX}%(levelname)s{Fore.WHITE}) > {Fore.LIGHTBLACK_EX}%(message)s{Fore.RESET}', datefmt='%H:%M:%S')

Intents = discord.Intents.default()
Intents.all()
Intents.message_content = True
Aura = commands.Bot(command_prefix=Prefix, case_insensitive=True, help_command=None, intents=Intents, owner_id=Owner)

def ClearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

# Error Handling

@Aura.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(embed=discord.Embed(title='Error', description=f'Command not found', color=discord.Color.red()))
	elif isinstance(error, commands.CommandOnCooldown):
		await ctx.send(embed=discord.Embed(title='Error', description=f'Command on cooldown, please try again in {error.retry_after:.2f} seconds', color=discord.Color.red()))
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send(embed=discord.Embed(title='Error', description=f'You are missing the following permissions: {", ".join(error.missing_perms)}', color=discord.Color.red()))
	elif isinstance(error, commands.BotMissingPermissions):
		await ctx.send(embed=discord.Embed(title='Error', description=f'I am missing the following permissions: {", ".join(error.missing_perms)}', color=discord.Color.red()))
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(embed=discord.Embed(title='Error', description=f'You are missing the following argument: {error.param.name}', color=discord.Color.red()))
	elif isinstance(error, commands.NotOwner):
		await ctx.send(embed=discord.Embed(title='Error', description=f'You are not the owner of this bot', color=discord.Color.red()))
	elif isinstance(error, commands.CommandInvokeError):
		await ctx.send(embed=discord.Embed(title='Error', description=f'An error occurred while executing the command', color=discord.Color.red()))
		logging.error(error.original)
	else:
		await ctx.send(embed=discord.Embed(title='Error', description=f'An error occurred while executing the command', color=discord.Color.red()))
		logging.error(error)

# Commands

@Aura.command(aliases=['statistics'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def Stats(ctx):
	Server = ctx.guild
	TotalMembers = Server.member_count
	OnlineMembers = len([_ for _ in Server.members if _.status == discord.Status.online])
	TextChannels = len(Server.text_channels)
	VoiceChannels = len(Server.voice_channels)
	Bots = Server.members
	Categories = len(Server.categories)
	Roles = Server.roles
	Emojis = Server.emojis
	VerificationLevel = Server.verification_level
	DefaultNotifications = Server.default_notifications
	ExplicitContentfilter = Server.explicit_content_filter
	ServerName = Server.name
	ServerIcon = Server.icon
	ServerBanner = Server.banner

	Embed = discord.Embed(title=f'Statistics for {ServerName}', color=discord.Color.blue())
	Embed.set_thumbnail(url=ServerIcon)
	Embed.set_image(url=ServerBanner)
	Embed.add_field(name='Total Members', value=TotalMembers, inline=True)
	Embed.add_field(name='Online Members', value=OnlineMembers, inline=True)
	Embed.add_field(name='Categories', value=Categories, inline=True)
	Embed.add_field(name='Text Channels', value=TextChannels, inline=True)
	Embed.add_field(name='Voice Channels', value=VoiceChannels, inline=True)
	Embed.add_field(name='Bots', value=' | '.join([_.name for _ in Bots if _.bot]) if Bots else 0, inline=True)
	Embed.add_field(name='Roles', value=' | '.join([_.name for _ in Roles if not 'everyone' in _.name]) if Roles else 0, inline=True)
	Embed.add_field(name='Emojis', value=' | '.join([_.name for _ in Emojis]) if Emojis else 0, inline=True)
	Embed.add_field(name='Verification Level', value=VerificationLevel, inline=True)
	Embed.add_field(name='Default Notifications', value=DefaultNotifications, inline=True)
	Embed.add_field(name='Explicit Content Filter', value=ExplicitContentfilter, inline=True)
	await ctx.send(embed=Embed)

@Aura.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def Help(ctx):
	Embed = discord.Embed(title='Help', description=f'Prefix: {Prefix}', color=0x2F3136)
	Embed.add_field(name='Stats | Statistics', value='Shows the server stats', inline=True)
	await ctx.send(embed=Embed)

@Aura.event
async def on_ready():
	ClearScreen()
	Activity = discord.Activity(name=Status, type=discord.ActivityType.listening)
	await Aura.change_presence(activity=Activity, status=discord.Status.online)
	print(Fore.LIGHTBLUE_EX + Logo)
	logging.info(f'⚡ {Aura.user.name} is online')
	logging.info(f'╭ Owner: {Owner}')
	logging.info(f'├ Prefix: {Prefix}')
	logging.info(f'╰ Status: {Status}')

@Aura.event
async def on_message(message):
	if message.author.bot:
		return
	if message.content.startswith(Prefix):
		await message.delete()
		logging.info(f'{message.author.name} ~ {message.content}')
		await Aura.process_commands(message)
	else:
		await Aura.process_commands(message)

# Run Bot

Aura.run(Token)
