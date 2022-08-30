import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import personqueue
from config import config
from db import database
import asyncio

load_dotenv()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix=config['prefix'])
database.build()


# bot.remove_command('help')


@bot.event
async def on_connect():
    print('Bot connected to Discord')


@bot.event
async def on_disconnect():
    print('Bot disconnected')


@bot.event
async def on_ready():
    print('Bot is ready')


# @bot.event
# async def on_message(message):
#     for msg in ['!showq', '!show', '!join', '!leave', '!rejoin', '!info']:
#         if msg in message.content:
#             await message.delete()
# channel(1014250769651879936)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.", delete_after=10)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.Do !info", delete_after=10)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the appropriate permissions to run this command.", delete_after=10)
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have sufficient permissions!", delete_after=10)


@bot.command()
async def showq(ctx: commands.Context):
    # if len(personqueue.queues) == 0:
    #     await ctx.author.send('No queues!', delete_after=15)
    #     return -1
    # else:
    #     i = 1
    #     await ctx.author.send('Queues:', delete_after=120)
    #     for que in personqueue.queues:
    #         await ctx.author.send('{}.{}'.format(i, que.qname), delete_after=120)
    #         i += 1
    queues = personqueue.mng2_all_queues()
    if not queues:
        await ctx.author.send('No Queues!', delete_after=15)
        return -1
    else:
        i = 1
        await ctx.author.send('Queues:', delete_after=120)
        for queue in queues:
            await ctx.author.send('{}.{}'.format(i, queue["name"]), delete_after=120)
            i += 1


@bot.command()
async def show(ctx: commands.Context, queue_name):
    users = personqueue.mng2_get_users(queue_name)
    if isinstance(users, str):
        await ctx.author.send(users)
        return -1
    elif users:
        await ctx.author.send('Queue {}:'.format(queue_name), delete_after=120)
        i = 1
        for user in users:
            await ctx.author.send('{}.{}'.format(i, user), delete_after=120)
            i += 1
    else:
        await ctx.author.send('Queue {} is empty!'.format(queue_name), delete_after=120)


@bot.command()
async def create(ctx: commands.Context, queue_name):
    msg = personqueue.mng2_create_queue(queue_name, ctx.author)
    await ctx.author.send(msg, delete_after=120)
    # if personqueue.command_check(ctx.message.content):
    #     await ctx.message.delete()


@bot.command()
async def join(ctx: commands.Context, queue_name):
    msg = personqueue.mng2_join_queue(queue_name, ctx.author)
    await ctx.author.send(msg, delete_after=120)
    # await ctx.channel.send(msg, delete_after=120)


@bot.command()
async def leave(ctx: commands.Context, queue_name):
    msg = personqueue.mng2_leave_queue(queue_name, ctx.author)
    await ctx.author.send(msg, delete_after=120)
    # await ctx.channel.send(msg, delete_after=120)


@bot.command()
async def rejoin(ctx: commands.Context, queue_name):
    msg = personqueue.mng2_rejoin_queue(queue_name, ctx.author)
    await ctx.author.send(msg, delete_after=120)
    # await ctx.channel.send(msg, delete_after=120)


@bot.command()
async def info(ctx: commands.Context):
    await ctx.author.send('Queue bot commands:\n'
                          '!showq - show all created queues\n'
                          '!show (queue name) - show students in queue\n'
                          '!join - join the queue\n!leave (queue name) - leave the queue\n!'
                          '!rejoin (queue name) - re-join the queue\n'
                          '!create (queue name) - create the queue', delete_after=120)


bot.run(os.getenv('TOKEN'))
