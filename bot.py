# encoding: utf-8
from colour import Color
from discord.ext import commands
import asyncio
import discord
import json
import randomcolor

with open('config.json', encoding='utf-8') as file:
	config = json.load(file)

bot = commands.Bot(command_prefix=config['prefix'], description='Discordで色を見ることが出来るBotです。\n製作者: @katabame#7736\n\nVersion: '+config['version']+'\n変更履歴: '+config['changelog'])
rcolor = randomcolor.RandomColor()

@bot.event
async def on_ready():
	print('[ OK ] Started synesthesia system')
	print('[INFO] Prefix is ' + config['prefix'])

async def send(ctx, arg, arg1=None, arg2=None):
	try:
		if arg and arg1 and arg2:
			arg = arg.strip(',')
			arg1 = arg1.strip(',')
			arg2 = arg2.strip(',')
			c = Color(rgb=(int(arg)/100, int(arg1)/100, int(arg2)/100))
			title = 'rgb(' + arg + ', ' + arg1 + ', ' + arg2 + ')'
		else:
			if ',' in arg:
				lrgb = arg.split(',')
				c = Color(rgb=(int(lrgb[0])/100, int(lrgb[1])/100, int(lrgb[2])/100))
			else:
				c = Color(arg) if arg.startswith('#') else Color('#'+arg)

			if ',' in ctx.message.content:
				title = 'rgb(' + str(int(c.red*100)) + ', ' + str(int(c.green*100)) + ', ' + str(int(c.blue*100)) + ')'
			else:
				title = c.hex

		embed = discord.Embed(title=title, colour=discord.Colour(int(c.hex_l.strip('#'), 16)), url='http://www.colorhexa.com/'+c.hex_l.strip('#'))
		image_url = 'https://placehold.jp/'+c.hex_l.strip('#')+'/ffffff/300x300.png?text=%20'
		embed.set_image(url=image_url)
		embed.add_field(name="HEX", value='`' + c.hex_l + '`', inline=True)
		embed.add_field(name="RGB", value='`rgb(' + str(int(c.red*100)) + '%, ' + str(int(c.green*100)) + '%, ' + str(int(c.blue*100)) + '%)`', inline=True)
		embed.add_field(name="HSL", value='`hsl(' + str(int(c.hue*100)) + '%, ' + str(int(c.saturation*100)) + '%, ' + str(int(c.luminance*100)) + '%)`', inline=True)
		await ctx.message.channel.send(embed=embed)
	except:
		await ctx.message.add_reaction('🚫')

@bot.command(name='color', aliases=['see'], help='指定された色を表示します\n\n例:\n$color #ffd1dc\n$color ffd1dc\n$color 42,42,42\n$color 42, 42, 42', usage='[#hex|hex|r,g,b|r, g, b]')
async def color(ctx, arg, arg1=None, arg2=None):
	await send(ctx, arg, arg1, arg2)

@bot.command(name='random', help='ランダムに色を表示します\n\n例:\n$random\n$random red\n$random blue', usage='(作成したい色)')
async def random(ctx, arg=None):
	if arg:
		rcolor = randomcolor.RandomColor().generate(hue=arg)
	else:
		rcolor = randomcolor.RandomColor().generate()
	await send(ctx, rcolor[0])

@bot.command(name='quit', aliases=['q'], hidden=True)
async def shutdown(ctx):
	print('[INFO] Shutting down...')
	if bot.is_owner(ctx.message.author):
		await ctx.message.add_reaction('👋🏻')
		exit()

if __name__ == '__main__':
	print('[INFO] Preparing synesthesia system...')
	bot.run(config['token'])
