import discord
from discord.ext import commands
from discord.utils import get
import binascii
import asyncpg
import os
import json
import datetime

bot = commands.Bot(command_prefix='>>', case_insensitive=True, owner_id=310863530591256577)
bot.remove_command('help')
bot.path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'utils/utils.json')
with open(bot.path, 'r') as f:
    bot.utils = json.load(f)

extensions = (
    'cogs.utility',
    'cogs.tournament',
    'cogs.admin',
)


async def create_db_pool():
    bot.pg = await asyncpg.create_pool(database="postgres", user="postgres", password=" ")


async def swapper(ctx, title, description, embed_list: list):
    index = 0
    emojis = ['\N{LEFTWARDS BLACK ARROW}', '\N{BLACK RIGHTWARDS ARROW}', '\N{CROSS MARK}']
    for embed in embed_list:
        embed.set_footer(text=f'Page {embed_list.index(embed) + 1}/{len(embed_list)}')
    message = await ctx.send(embed=embed_list[index])
    for emoji in emojis:
        await message.add_reaction(emoji)
    while True:
        reaction, user = await bot.wait_for('reaction_add', check=lambda r, u: not u.bot and r.message.id == message.id and u.id == ctx.author.id and r.emoji in emojis)
        if reaction.emoji == emojis[0]:
            if index > 0:
                index -= 1
                await message.edit(embed=embed_list[index])
            await message.remove_reaction(emoji=reaction.emoji, member=user)
        elif reaction.emoji == emojis[1]:
            if index <= (len(embed_list) - 2):
                index += 1
                await message.edit(embed=embed_list[index])
            await message.remove_reaction(emoji=reaction.emoji, member=user)
        elif reaction.emoji == emojis[2]:
            nemb = discord.Embed(color=int(f'0x{binascii.hexlify(str(id).encode())[9:15].decode()}', 16), description=description).set_author(name=f'{title} machine closed.', icon_url=bot.user.avatar_url)
            await message.edit(embed=nemb)
            await message.clear_reactions()
            break

bot.swapper = swapper


async def EmbedAssembly(member):
    embeds = []
    mmbed = discord.Embed(color=0x6000ff)
    for command in bot.commands:
        arguments = str()
        desc = str()
        help_string = str(command.help).split(':', 5)
        perm = help_string[4]
        if perm == 'owner' and member.id != 310863530591256577:
            continue
        elif perm == 'mod' and not member.guild_permissions.manage_messages:
            continue
        elif perm == 'admin' and not member.guild_permissions.ban_members:
            continue
        if command.cog_name is None:
            mmbed.set_author(name='The Help Card', url='https://en.wikipedia.org/wiki/Tetrahydrocannabinol', icon_url=bot.user.avatar_url)
            mmbed.description = 'For all to use.'
            for arg in help_string[:4]:
                arguments = arguments + f'{arg} '
            for arg in help_string[5:]:
                desc = desc + f'{arg}'
            mmbed.add_field(name=f'**{command.name}**', value=f'`{str(bot.command_prefix)}{command.name} {arguments.strip()}`\n{desc}', inline=False)
    embeds.append(mmbed)

    for cog in bot.cogs:
        embed = discord.Embed(color=0x6000ff, description='For all to use.')
        if cog == 'Admin':
            embed.set_author(name='The Help Card - Admin', icon_url=bot.user.avatar_url)
            embed.description = 'Only Administrators may see and use these commands.'
        elif cog == 'Tournament':
            embed.set_author(name='The Help Card - Tourneys', icon_url=bot.user.avatar_url)
            embed.description = 'Tourney-related commands.'
        elif cog == 'Utility':
            embed.set_author(name='The Help Card - Utility', icon_url=bot.user.avatar_url)
        for command in bot.get_cog(cog).get_commands():
            arguments = str()
            desc = str()
            help_string = str(command.help).split(':', 5)
            perm = help_string[4]
            if perm == 'owner' and member.id != 310863530591256577:
                continue
            elif perm == 'mod' and not member.guild_permissions.manage_messages:
                continue
            elif perm == 'admin' and not member.guild_permissions.ban_members:
                continue

            for arg in help_string[:4]:
                arguments = arguments + f'{arg} '
            for arg in help_string[5:]:
                desc = desc + f'{arg}'
            embed.add_field(name=f'**{command.name}**', value=f'`{str(bot.command_prefix)}{command.name} {arguments.strip()}`\n{desc}', inline=False)
        embeds.append(embed)

        page_count = len(embeds)
        for embed in embeds:
            x = embeds.index(embed)
            y = x + 1
            embed.set_footer(text=f'Page {y}/{page_count}')
    return embeds


@bot.command(aliases=['h'])
async def help(ctx):
    """<command>:::::Seriously?"""
    index = 0
    embeds = await EmbedAssembly(ctx.author)
    await ctx.message.delete()
    await bot.swapper(ctx, 'Help', f'`{str(bot.command_prefix)}help` or `{str(bot.command_prefix)}h` to reopen.', embeds)

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f'`{extension}` cannot be loaded. [{error}]')

bot.loop.run_until_complete(create_db_pool())
bot.run(bot.utils["TOKEN"])