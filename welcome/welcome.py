import discord
from redbot.core import commands

docker_cog_path = "/data/cogs/Welcome/Avatars/"

class Welcome(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = member.guild.system_channel
    #     userAvatarUrl = member.display_avatar
    #     if channel is not None:

    #         await channel.send(f'Welcome {member.mention}!!\n{userAvatarUrl}')

    @commands.command()
    async def test_cmd(self, ctx):
        """This responds to the text command!"""

        # Get important information about the context of the command
        channel = ctx.channel
        author = ctx.message.author

        # Download the avatar image
        filename = docker_cog_path + f"avatar_{author.id}.jpg"
        await author.avatar.save(filename)
        avatar_file = discord.File(filename)

        # Sends message in the command's origin channel
        await channel.send(f"Hello {author.mention}!", file = avatar_file)