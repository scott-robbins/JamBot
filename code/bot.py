from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
import asyncio
import discord
import random
import time
import os

# LOAD client API AUTH/SERVERS
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Load client and Set command prefix
bot = commands.Bot(command_prefix = "$")


@bot.event
async def on_ready():
	guild = get(bot.guilds, name=GUILD)
	print(f'{bot.user} has connected to Discord!')		
	print(f'{guild.name}(id: {guild.id})')
	members = '\n - '.join([member.name for member in guild.members])
	print(f'Guild Members:\n - {members}')

@bot.command(name="ping", pass_context=True)
async def ping(ctx):
	ping_ = bot.latency
	ping =  round(ping_ * 1000)
	print('ping command received')
	await ctx.send(f"my ping is {ping}ms")

@bot.event
async def on_message(message):
	guild = get(bot.guilds, name=GUILD)
	allowed = ['mp3','wav','flac']
	# we do not want the bot to reply to itself
	if message.author == bot.user:
		return
	# Now process the Attachment
	member = message.author	
	for a in message.attachments:
		fname = a.filename
		sz = a.size
		if fname.split('.')[1] not in allowed:
			await member.dm_channel.send('You cant send me that kind of file')
			return
		else:
			f = await a.read(use_cached=False)	
			print('%s is uploading %s' % (message.author, fname))
			open(os.getcwd()+'/LocalData/Music/'+fname,'wb').write(f)
			await member.dm_channel.send('Thanks! Now join a voice channel, and send me the play command.')
			return 
	await bot.process_commands(message)


@bot.command(name='play', pass_context=True)
async def play(context, args):
	if args:
		audio_file = os.getcwd()+'/LocalData/Music/'+args
		print('Playing %s' % audio_file)
	else:
		# TODO: Tell user what they did wrong
		return
	user = context.message.author
	vc = context.author.voice.channel
	voice_client = await vc.connect()
	guild =  get(bot.guilds, name=GUILD)
	voice = get(bot.voice_clients, guild=guild)
	try:
		if voice != None:
			player = discord.FFmpegPCMAudio(audio_file)
			voice.play(player)
			voice.source.volume = 1.00
	except discord.ext.commands.errors.CommandInvokeError:
		await voice.disconnect()
	

@bot.command(name='show-songs', pass_context=True)
async def show_songs(context):
	content = '**Songs available:**\n'
	for fname in os.listdir(os.getcwd()+'/LocalData/Music'):
		content += ('- *%s*\n' % fname)
	channel = context.message.channel
	await context.send(content)

def setup():
	# Setup Local Music Repo
	if not os.path.isdir(os.getcwd()+'/LocalData/'):
		os.mkdir(os.getcwd()+'/LocalData/')
	if not os.path.isdir(os.getcwd()+'/LocalData/Music'):
		os.mkdir(os.getcwd()+'/LocalData/Music')


def main():
	# Load Folders of local data/music 
	setup()
	# Run It using API token
	bot.run(TOKEN)


if __name__ == '__main__':
	main()
