from redbot.core import commands

class HelloBot(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        userAvatarUrl = member.display_avatar
        if channel is not None:

            await channel.send(f'Welcome {member.mention}!!\n{userAvatarUrl}')

    @commands.command()
    async def hello(self, ctx):
        """This does stuff!"""
        await ctx.send("I can do things!")

    @commands.command()
    async def test_cmd(self, ctx):
        """This responds to the text command!"""
        channel = ctx.channel
        await channel.send("Hello {ctx.message.author.mention}!")