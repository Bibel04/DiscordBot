import discord
from discord.ext import commands
from hash_manager import *
from CrackPassword import *
import time

client = commands.Bot(command_prefix="?")
client.remove_command("help")
client.remove_command("decrypt")
client.remove_command("encrypt")
client.remove_command("crack_password")

client.remove_command("generate_rsa")
client.remove_command("decrypt_rsa")
client.remove_command("generate_rsa")

bot_commands = ["encrypt", "decrypt", "crack_password"]


@client.event
async def on_ready():
    print("online")


@client.command()
async def help(ctx):
    message = "Commands:\n"
    for command in bot_commands:
        message += f"• {command}\n"
    await ctx.channel.send(message)


@client.command()
async def decrypt(ctx, coded):
    crack = CrackHashes()
    coded = str(coded)

    before = time.time()
    hashes = crack.guessing_hashes(hash1=coded)
    after = time.time()
    elapsed_time = after - before

    embed = discord.Embed(title="Decrypted text", url="https://pl.wikipedia.org/wiki/MD5", color=0x48f542)
    embed.add_field(name="Time", value=f"{round(elapsed_time)}s", inline=False)
    embed.add_field(name="Coded", value=coded, inline=False)
    embed.add_field(name="Decoded", value=hashes[0], inline=False)
    embed.add_field(name="Hash Type", value=hashes[1], inline=False)
    await ctx.author.send(embed=embed)


@client.command()
async def encrypt(ctx, text, hash_type):
    crack = CrackHashes()
    encrypted_text = crack.creating_hashes(str(text).strip(), str(hash_type).strip(), create_new_hash=True)
    embed = discord.Embed(title="Encrypted text", url="https://pl.wikipedia.org/wiki/MD5", color=0x48f542)
    if len(encrypted_text) == 2:
        embed.add_field(name="Wrong format", value=encrypted_text[0], inline=False)
        embed.add_field(name="Text", value=text, inline=False)
        embed.add_field(name="Encoded", value=encrypted_text[1], inline=False)
    else:
        embed.add_field(name="Text", value=text, inline=False)
        embed.add_field(name="Encoded", value=encrypted_text, inline=False)
        embed.add_field(name="Hash Type", value=str(hash_type).strip(), inline=False)
    await ctx.author.send(embed=embed)


@client.command()
async def play(ctx, game):
    await client.change_presence(activity=discord.Game(name=game))


@client.command()
async def crack_password(ctx, username):
    crack_passwd = CrackPassword()
    cookies = crack_passwd.get_cookies()
    password = crack_passwd.crack_password(username=username, cookies=cookies)
    embed = discord.Embed(title="Password", url="http://localhost/dvwa/vulnerabilities/brute/", color=0x48f542)
    embed.add_field(name="Username", value=username, inline=False)
    embed.add_field(name="Password", value=password, inline=False)
    await ctx.author.send(embed=embed)


@client.command()
async def generate_rsa(ctx, text):
    pass
    # generator = RsaGenerator()


client.run('OTgyMDE5MzcyNjQwMDEwMjcx.Goe03x.Fl95-uZ751DMrRmD6Et5tXeVMIEvbsGG5q8nKs')



# client = discord.Client()
#
# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')
#
# client.run('OTgyMDE5MzcyNjQwMDEwMjcx.Goe03x.Fl95-uZ751DMrRmD6Et5tXeVMIEvbsGG5q8nKs')