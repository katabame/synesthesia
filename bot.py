# encoding: utf-8
from colorthief import ColorThief
from colour import Color
from discord.ext import commands
import discord
import json
import os
import randomcolor
import sys
import uuid
import requests

with open('config.json', encoding='utf-8') as file:
    config = json.load(file)

bot = commands.Bot(
    command_prefix=config['prefix'],
    description=f"Discordで色を見ることが出来るBotです。\n"
                f"製作者: @katabame#3778\n"
                f"\n"
                f"Version: {config['version']}\n"
                f"変更履歴: {config['changelog']}")
rcolor = randomcolor.RandomColor()


@bot.event
async def on_ready():
    print('[ OK ] Started synesthesia system')
    print(f"[INFO] Prefix is {config['prefix']}")


async def send(ctx, arg, arg1=None, arg2=None):
    try:
        if arg and arg1 and arg2:
            arg = arg.strip(',')
            arg1 = arg1.strip(',')
            arg2 = arg2.strip(',')
            c = Color(rgb=(int(arg) / 255, int(arg1) / 255, int(arg2) / 255))
            title = f"rgb({arg}, {arg1}, {arg2})"
        else:
            if ',' in arg:
                lrgb = arg.split(',')
                c = Color(rgb=(int(lrgb[0]) / 255, int(lrgb[1]) / 255, int(lrgb[2]) / 255))
            else:
                c = Color(arg) if arg.startswith('#') else Color('#' + arg)

            if ',' in ctx.message.content:
                title = f"rgb({str(int(c.red * 255))}, {str(int(c.green * 255))}, {str(int(c.blue * 255))})"
            else:
                title = c.hex

        embed = discord.Embed(
            title=title,
            colour=discord.Colour(int(c.hex_l.strip('#'), 16)),
            url=f"http://www.colorhexa.com/{c.hex_l.strip('#')}")
        image_url = f"https://placehold.jp/{c.hex_l.strip('#')}/ffffff/300x300.png?text=%20"
        embed.set_thumbnail(url=image_url)
        embed.add_field(
            name="HEX",
            value=f"`{c.hex_l}`",
            inline=True)
        embed.add_field(
            name="RGB Demical",
            value=f"rgb({str(int(c.red * 255))}, {str(int(c.green * 255))}, {str(int(c.blue * 255))})",
            inline=True)
        embed.add_field(
            name="RGB Percent",
            value=f"rgb({str(int(c.red * 100))}%, {str(int(c.green * 100))}%, {str(int(c.blue * 100))}%)",
            inline=True)
        embed.add_field(
            name="HSL",
            value=f"hsl({str(int(c.hue * 100))}, {str(int(c.saturation * 100))}, {str(int(c.luminance * 100))})",
            inline=True)
        await ctx.message.channel.send(embed=embed)
    except Exception as e:
        print(e.args)
        await ctx.message.add_reaction('🚫')


@bot.command(
    name='color',
    aliases=['see'],
    help='指定された色を表示します\n\n例:\n$color #ffd1dc\n$color ffd1dc\n$color 42,42,42\n$color 42, 42, 42',
    usage='[#hex|hex|r,g,b|r, g, b]')
async def color(ctx, arg, arg1=None, arg2=None):
    await send(ctx, arg, arg1, arg2)


@bot.command(name='random',
             help='ランダムに色を表示します\n\n例:\n$random\n$random red\n$random blue',
             usage='(作成したい色)')
async def random(ctx, arg=None):
    random_color = randomcolor.RandomColor().generate(hue=arg) if arg else randomcolor.RandomColor().generate()
    await send(ctx, random_color[0])


@bot.command(
    name='dominant',
    help='指定された画像のドミナントカラーを表示します\n\n例:\n$dominant https://ddlc.moe/images/screen4.png',
    usage='[画像添付 | 画像URL]')
async def dominant(ctx, arg=None):
    tmp = str(uuid.uuid4())
    if arg and arg.startswith('http'):
        with requests.get(url=arg) as data:
            with open(tmp, 'wb') as f:
                f.write(data.content)
    else:
        if ctx.message.attachments[0]:
            await ctx.message.attachments[0].save(tmp)
        else:
            return await ctx.message.add_reaction('🚫')
    rgb = ColorThief(tmp).get_color(quality=1)
    await send(ctx, str(rgb).strip('()'))
    os.remove(tmp)


@bot.command(
    name='quit',
    aliases=['q'],
    hidden=True)
async def shutdown(ctx):
    print('[INFO] Shutting down...')
    if bot.is_owner(ctx.message.author):
        await ctx.message.add_reaction('👋🏻')
        sys.exit(0)


if __name__ == '__main__':
    print('[INFO] Preparing synesthesia system...')
    bot.run(config['token'])
