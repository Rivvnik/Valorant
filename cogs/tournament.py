import discord
from discord.ext import commands
from discord.utils import get

table_list = ['joker_teams', 'joker_users', 'joker_team_results', 'joker_user_results', 'joker_actives']


class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_permissions(ban_members=True)
    async def db(self, ctx):
        """<reset>/(enter):(table):::admin:Direct referential database manipulation.\n\n`>>db reset`\n`>>db enter users`"""

    @commands.group(aliases=['configure', 'cfg'])
    @commands.has_permissions(kick_members=True)
    async def config(self, ctx):
        """<team>/<player>/<leaderboard>:<add|pop>/<leader>:::mod:Global configuration command\n\n`>>config team add user_1_id user_2_id . . .`\n`>>config team pop team_id`"""

    @db.command()
    async def reset(self, ctx):
        for table in table_list:
            await self.bot.pg.execute(f'DROP TABLE IF EXISTS {table} CASCADE')
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u = "CREATE TABLE ", "PRIMARY KEY", "NOT NULL", "integer", "bigint", "serial", "text", " REFERENCES ", "_id", "s (", "), ", "joker_", ", time timestamptz)", ", losses ", "wins ", "team", "user", "s (id ", "s(id", "_result", ", active_"
        for dude in [
            f'{a}{l}{p}{r}{f} {b}{u}{o}{d}{u}losses {d})',
            f'{a}{l}{q}{r}{e} {c} {b}, {p}{i} {d}{h}{l}{p}{s}{k}region {g}, league {g})',
            f'{a}{l}{p}{t}{r}{f} {b}, {p}{i} {d}{h}{l}{p}{s}{k}{o}{d}{n}{d}{m}',
            f'{a}{l}{q}{t}{r}{f} {b}, {q}{i} {e}{h}{l}{q}{s}{k}{o}{d}{n}{d}{m}'
        ]:
            await self.bot.pg.execute(dude)

    @config.group(aliases=['teams', 't'])
    async def team(self, ctx):
        """meat cleaver"""

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

def setup(bot):
    bot.add_cog(Tournament(bot))