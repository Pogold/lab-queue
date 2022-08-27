import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import personqueue
from config import config

load_dotenv()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix=config['prefix'])


# bot.remove_command('help')


@bot.event
async def on_connect():
    print('Bot connected to Discord')


@bot.event
async def on_ready():
    print('Bot is ready')


@bot.command()
async def showq(ctx: commands.Context):
    if len(personqueue.queues) == 0:
        await ctx.send('No queues!')
        return -1
    else:
        i = 1
        await ctx.send('Queues:')
        for que in personqueue.queues:
            await ctx.send('{}.{}'.format(i, que.qname))
            i += 1


@bot.command()
async def show(ctx: commands.Context, queue_name):
    que = personqueue.get_users(queue_name)
    if isinstance(que, str):
        await ctx.send(que)
        return -1
    elif not isinstance(que, str):
        await ctx.send('Queue {}:'.format(queue_name))
        i = 1
        for person in que.q:
            await ctx.send('{}.{}'.format(i, person.name))
            i += 1


@bot.command()
async def create(ctx: commands.Context, queue_name):
    await ctx.send(personqueue.create_queue(queue_name, ctx.message.author.display_name, str(ctx.message.author)))


@bot.command()
async def join(ctx: commands.Context, queue_name):
    await ctx.send(personqueue.join_queue(queue_name, ctx.message.author.display_name, str(ctx.message.author)))


@bot.command()
async def leave(ctx: commands.Context, queue_name):
    await ctx.send(personqueue.leave_queue(queue_name, ctx.author, str(ctx.author)))


@bot.command()
async def rejoin(ctx: commands.Context, queue_name):
    await ctx.send(personqueue.leave_queue(queue_name, ctx.author, str(ctx.author)))
    await ctx.send(personqueue.join_queue(queue_name, ctx.author, str(ctx.author)))


@bot.command()
async def info(ctx: commands.Context):
    await ctx.send('Queue bot commands:\n'
                   '!showq - show all created queues\n'
                   '!show (queue name) - show students in queue\n'
                   '!join - join the queue\n!leave (queue name) - leave the queue\n!'
                   'rejoin (queue name) - re-join the queue\n'
                   '!create (queue name) - create the queue')


bot.run(os.getenv('TOKEN'))
