import discord
from pathlib import Path
from redbot.core import commands

docker_cog_path = "/data/cogs/Welcome"

Avatars = docker_cog_path + "/Avatars"
BackgroundImage = docker_cog_path + "/background_image.jpg"

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
    async def test_welcome(self, ctx):
        """Demonstrates the welcome message!"""

        # Get important information about the context of the command
        channel = ctx.channel
        author = ctx.message.author

        # Setup avatar folder and filename
        Path(Avatars).mkdir(parents=True, exist_ok=True)
        filename = Avatars + f"/avatar_{author.id}.jpg"

        # Download and save the avatar image
        await author.avatar.save(filename)
        avatar_file = discord.File(filename)

        # Sends message in the command's origin channel
        await channel.send(f"Hello {author.mention}!", file = avatar_file)

        if Path(BackgroundImage).if_file():
            await channel.send(f"With this background!", file = discord.File(BackgroundImage))

    @commands.command()
    async def set_background(self, ctx):
        """Sets the background of the welcome message!"""
        
        ctx.message.attachment.save(BackgroundImage)


