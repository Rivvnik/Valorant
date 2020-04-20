import discord
from discord.ext import commands
from discord.utils import get


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('----------')
        print(f'Logged in as {self.bot.user.name}')
        print(f'Client ID: {self.bot.user.id}')
        print('----------')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            await ctx.message.add_reaction(emoji='❌')
        except:
            pass
        if isinstance(error, commands.NotOwner):
            await ctx.send('You are not my father.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Sorry. You do not have the permissions necessary to execute this command.')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('Sorry; I was unable to find that command. Check your syntax.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Sorry. It looks like you\'re missing an argument or two. Or three. Check your syntax.')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('Sorry. This command has not been constructed for use within private channels.')
        else:
            await ctx.send(f'Alright! Okay. I have no idea what the fuck you just said.\n`{error}`')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        try:
            await ctx.message.add_reaction(emoji='✅')
        except:
            pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if isinstance(message.channel, discord.DMChannel):  # add an AND statement to this to prevent randoms getting entered into teams
                team_name = message.content.lower()
                await self.bot.pg.execute('INSERT INTO joker_teams (active_wins, active_losses, name) VALUES ($1, $1, $2) ON CONFLICT (name) DO NOTHING', 0, team_name)
                team_id = await self.bot.pg.fetch('SELECT id FROM joker_teams WHERE name=$1', team_name)
                await self.bot.pg.execute('UPDATE joker_users SET team_id=$1 WHERE id=$2', team_id[0]['id'], message.channel.recipient.id)
                region = await self.bot.pg.fetch('SELECT region FROM joker_users WHERE id=$1', message.channel.recipient.id)
                if region[0]['region'] == 'NA':
                    # give the people some NA times
                    return
                else:
                    # give the people some EU times
                    return

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot and not isinstance(reaction.emoji, str):
            if reaction.message.id in self.bot.message_ids and reaction.emoji.name == 'shard':
                rough = get(user.roles, name='NA | ☑️ HL Open League Members') if get(user.roles, name='NA | ☑️ HL Open League Members') is not None else get(user.roles, name='NA | ✅ HL Pre-Made Team Members') if get(user.roles, name='NA | ✅ HL Pre-Made Team Members') is not None else get(user.roles, name='EU | ☑️ HL Open League Members') if get(user.roles, name='EU | ☑️ HL Open League Members') is not None else get(user.roles, name='EU | ✅ HL Pre-Made Team Members') if get(user.roles, name='EU | ✅ HL Pre-Made Team Members') is not None else get(user.roles, name='Skeleton Key')
                region = rough.name[:2]
                league = 'open league' if rough.name[11:15] == 'Open' else 'pre made'
                await self.bot.pg.execute('INSERT INTO joker_users (id, region, league) VALUES ($1, $2, $3) ON CONFLICT (id) DO NOTHING', user.id, region, league)
                await user.send("What team are you looking to be a part of throughout this tournament?")

def setup(bot):
    bot.add_cog(Utility(bot))