from redbot.core import commands

class HelloBot(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        userAvatarUrl = member.avatar_url
        if channel is not None:
            await channel.send(f'Welcome {member.mention}!!/n{userAvatarUrl}')

    @commands.command()
    async def hello(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do things!")