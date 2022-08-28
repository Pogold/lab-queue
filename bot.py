import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import personqueue
from config import config
from db import database

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

@bot.event
async def on_command_error(ctx, error):
    if not isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif not isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.Do !info")
    elif not isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the appropriate permissions to run this command.")
    elif not isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have sufficient permissions!")
    else:
        print(error)


@bot.command()
async def showq(ctx: commands.Context):
    if len(personqueue.queues) == 0:
        await ctx.author.send('No queues!')
        return -1
    else:
        i = 1
        await ctx.author.send('Queues:')
        for que in personqueue.queues:
            await ctx.author.send('{}.{}'.format(i, que.qname))
            i += 1


@bot.command()
async def show(ctx: commands.Context, queue_name):
    que = personqueue.get_users(queue_name)
    if isinstance(que, str):
        await ctx.author.send(que)
        return -1
    elif not isinstance(que, str):
        await ctx.author.send('Queue {}:'.format(queue_name))
        i = 1
        for person in que.q:
            await ctx.author.send('{}.{}'.format(i, person.name))
            i += 1


@bot.command()
async def create(ctx: commands.Context, queue_name):
    await ctx.author.send(personqueue.create_queue(queue_name, ctx.author, str(ctx.author)))



@bot.command()
async def join(ctx: commands.Context, queue_name):
    await ctx.send(personqueue.join_queue(queue_name, ctx.author, str(ctx.author)))


@bot.command()
async def leave(ctx: commands.Context, queue_name):
    await ctx.send(personqueue.leave_queue(queue_name, ctx.author, str(ctx.author)))


@bot.command()
async def rejoin(ctx: commands.Context, queue_name):
    await ctx.send(personqueue.leave_queue(queue_name, ctx.author, str(ctx.author)))
    await ctx.send(personqueue.join_queue(queue_name, ctx.author, str(ctx.author)))


@bot.command()
async def info(ctx: commands.Context):
    await ctx.author.send('Queue bot commands:\n'
                          '!showq - show all created queues\n'
                          '!show (queue name) - show students in queue\n'
                          '!join - join the queue\n!leave (queue name) - leave the queue\n!'
                          'rejoin (queue name) - re-join the queue\n'
                          '!create (queue name) - create the queue')


bot.run(os.getenv('TOKEN'))
