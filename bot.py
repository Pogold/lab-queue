import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import discord_queue
from config import config

load_dotenv()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix=config['prefix'])
bot.remove_command('help')


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
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("```Command not found.```", delete_after=10)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("```Missing a required argument.Do !info```", delete_after=10)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("```You do not have the appropriate permissions to run this command.```", delete_after=10)
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("```I don't have sufficient permissions!```", delete_after=10)


@bot.command()
async def showall(ctx: commands.Context):
    queues = discord_queue.get_all()
    if not queues:
        await ctx.author.send('**No Queues!**', delete_after=15)
        return -1
    else:
        i = 1
        await ctx.author.send('**Queues:**', delete_after=120)
        for q in queues:
            await ctx.author.send('`{}.{}`'.format(i, q["name"]), delete_after=120)
            i += 1


@bot.command()
async def show(ctx: commands.Context, queue_name):
    users = discord_queue.get_users(queue_name)
    if isinstance(users, str):
        await ctx.author.send(users)
        return -1
    elif users:
        await ctx.author.send('**Queue `{}`:**'.format(queue_name), delete_after=120)
        i = 1
        for user in users:
            await ctx.author.send('**{}.{}**'.format(i, user), delete_after=120)
            i += 1
    else:
        await ctx.author.send('Queue `{}` is empty!'.format(queue_name), delete_after=10)


@bot.command()
async def create(ctx: commands.Context, queue_name):
    await ctx.author.send(discord_queue.create(queue_name, ctx.author), delete_after=120)


@bot.command()
async def join(ctx: commands.Context, queue_name):
    await ctx.author.send(discord_queue.join(queue_name, ctx.author), delete_after=120)


@bot.command()
async def leave(ctx: commands.Context, queue_name):
    await ctx.author.send(discord_queue.leave(queue_name, ctx.author), delete_after=120)


@bot.command()
async def rejoin(ctx: commands.Context, queue_name):
    await ctx.author.send(discord_queue.rejoin(queue_name, ctx.author), delete_after=120)


@bot.command()
async def info(ctx: commands.Context):
    await ctx.author.send('Queue bot commands:\n'
                          '**!showq** - show all created queues\n'
                          '**!show** (queue name) - show students in queue\n'
                          '**!join** - join the queue\n!leave (queue name) - leave the queue\n!'
                          '**!rejoin** (queue name) - re-join the queue\n'
                          '**!create** (queue name) - create the queue', delete_after=120)


bot.run(os.getenv('TOKEN'))
