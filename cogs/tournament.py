import discord
from discord.ext import commands
from discord.utils import get
from asyncio import sleep as slep

table_list = ['joker_teams', 'joker_users', 'joker_team_results', 'joker_user_results', 'joker_actives']


class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.message_ids = []

    async def prompter(self, ctx, prompt, constraint):
        try:
            message = await ctx.send(prompt)
            response = await self.bot.wait_for('message', check=lambda m: not m.author.bot and m.author.id == ctx.author.id and eval(constraint))
            await message.delete()
            await response.delete()
            return response
        except Exception as e:
            await ctx.send(f'uhhhhhh ```{e}```')
            return

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def db(self, ctx):
        """<reset>::::admin:Direct referential database manipulation."""
        return

    @commands.group(aliases=['t'])
    @commands.has_permissions(ban_members=True)
    async def tourney(self, ctx):
        """<toggle>/<loop>/(board):(activate):::admin:Invoke high-level tournament actions"""

    @commands.group(aliases=['configure', 'cfg'])
    @commands.has_permissions(kick_members=True)
    async def config(self, ctx):
        """<team>/(signups):<add|pop|leader>/(desc)/(switch):<id(s)>::mod:Global configuration command\n\n`>>config team add user_1_id user_2_id . . .`\n`>>config signups description`"""
        return

    @commands.group(aliases=['portal'])
    async def panel(self, ctx):
        """::::mod:Automatically updating administrator panel."""
        return

    @config.group(aliases=['teams', 't'])
    async def team(self, ctx):
        """meat cleaver"""
        return

    @config.group(aliases=['su', 'sign', 'signup'])
    async def signups(self, ctx):
        """breet beaver"""
        return

    @tourney.group(aliases=['leaderboard', 'lb'])
    async def board(self, ctx):
        return

    @db.command()
    async def reset(self, ctx):
        for table in table_list:
            await self.bot.pg.execute(f'DROP TABLE IF EXISTS {table} CASCADE')
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u = "CREATE TABLE ", "PRIMARY KEY", "NOT NULL", "integer", "bigint", "serial", "text", " REFERENCES ", "_id", "s (", "), ", "joker_", ", time timestamptz)", ", losses ", "wins ", "team", "user", "s (id ", "s(id", "_result", ", active_"
        for dude in [
            f'{a}{l}{p}{r}{f} {b}{u}{o}{d}{u}losses {d}, name {g})',
            f'{a}{l}{q}{r}{e} {c} {b}, {p}{i} {d}{h}{l}{p}{s}{k}region {g}, league {g})',
            f'{a}{l}{p}{t}{r}{f} {b}, {p}{i} {d}{h}{l}{p}{s}{k}{o}{d}{n}{d}{m}',
            f'{a}{l}{q}{t}{r}{f} {b}, {q}{i} {e}{h}{l}{q}{s}{k}{o}{d}{n}{d}{m}'
        ]:
            await self.bot.pg.execute(dude)

    @team.command()
    async def add(self, ctx, *, args: str):
        args = [x.strip() for x in args.split(' ')]
        users = []
        for arg in args:
            try:
                if self.bot.get_user(int(arg)) is not None:
                    users.append(self.bot.get_user(int(arg)))
            except ValueError as e:
                continue
        await ctx.send(f'The users I got from that are {", ".join([x.display_name for x in users[:-1]])}, and {users[-1].display_name}.\nIs this correct?')
        await ctx.send(f"Let's assume it's correct for now. Who's the leader?")

    @team.command()
    async def pop(self, ctx, team_id):
        users = await self.bot.pg.fetch('SELECT id FROM joker_users WHERE team_id=$1', int(team_id))
        for record in users:
            await self.bot.pg.execute('UPDATE joker_users SET team_id=$1 where id=$2', None, record['id'])
        await self.bot.pg.execute('DELETE FROM joker_teams WHERE id=$1', int(team_id))
        return

    @signups.command(aliases=['description', 'd'])
    async def desc(self, ctx):
        warning = "**NOTE**: In order to effectively participate in this tournament, you must ensure that I (your overlord robot) am able to send messages to you.\nIf you fail to ensure this simple prerequisite, the hindrance to your overall participation will wholly be on you.\n\n__Be aware of this prior to entry.__"
        description = await self.prompter(ctx, "Please provide a description for how you'd like your users to sign up.\n\nNote that a warning ensuring my ability to message users will be automatically appended to your description.", 'm.content')
        description = f"{description.content}\n\n{warning}"
        embed = discord.Embed(color=0xBEE5C4, description=description).set_author(name='Sign Up Protocol', icon_url=self.bot.user.avatar_url)
        self.bot.sign_up_protocol = embed
        await ctx.send(embed=self.bot.sign_up_protocol)
        return

    @signups.command(aliases=['sw', 'check'])
    async def switch(self, ctx):
        channel = await self.prompter(ctx, "Please mention the channel in which you'd like me to aggregate user sign-ups.", 'm.channel_mentions')
        channel = channel.channel_mentions[0]
        message = await channel.send(embed=self.bot.sign_up_protocol)
        await message.add_reaction(get(self.bot.emojis, name='shard'))
        self.bot.message_ids.append(message.id)
        return

    @tourney.command()
    async def loop(self, ctx):
        return

    @tourney.command()
    async def toggle(self, ctx):
        return

    @board.command()
    async def activate(self, ctx):
        return

def setup(bot):
    bot.add_cog(Tournament(bot))
