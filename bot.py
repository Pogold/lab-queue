import discord
from discord.ext import commands

import sqlite3
from config import config

bot = commands.Bot(command_prefix=config['prefix'])
bot.remove_command('help')
connection =sqlite3.connect('server.db')
cursor=connection.cursor()


@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
        await ctx.reply(ctx.content)

@bot.event
async def on_connect():
    print('Bot connected to Discord')

@bot.event
async def on_ready():
    
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users  (  
        id INT,
        name TEXT
        )""")
    connection.commit()
    
    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone is None:
               cursor.execute(f"INSERT INTO users VALUES ({member.id},'{member}')")
               connection.commit()
            else:
                pass
    print('Bot is ready')

@bot.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id={member.id} ").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ({member.id},'{member}')")
        connection.commit()
    else:
        pass

@bot.command()
async def create(ctx):
  pass

bot.run(config['token'])