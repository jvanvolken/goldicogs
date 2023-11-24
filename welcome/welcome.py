# Image and File Manipulation Libraries
from pathlib import Path
from PIL import Image
from PIL import ImageDraw

# Discord Bot Libraries
import discord
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
        await author.display_icon.save(filename)
        avatar_file = discord.File(filename)

        # Sends a welcome message in the command's origin channel
        if Path(BackgroundImage).is_file():
            avatar_background = docker_cog_path + "avatar_background.png"

            img = Image.open(BackgroundImage)
            width, height = img.size

            margins = width * 0.07

            draw = ImageDraw.Draw(img, "RGBA")
            draw.rounded_rectangle(((margins, margins), (width - margins, height - margins)), fill=(0, 0, 0, 160), radius = 10)
            img.save(avatar_background)

            await channel.send(f"Hello {author.mention}!", file = avatar_file)
            await channel.send(f"Welcome to the treehouse, {author.mention}! Make yourself at home!", file = discord.File(avatar_background))
        else:
            await channel.send(f"Hello {author.mention}!", file = avatar_file)



    @commands.command()
    async def set_background(self, ctx):
        """Sets the background of the welcome message!"""
        
        # Get important information about the context of the command
        channel = ctx.channel
        author = ctx.message.author

        # Download and save the attachment file
        await ctx.message.attachments[0].save(BackgroundImage)

        # Sends message in the command's origin channel
        await channel.send(f"Thanks for the new Welcome Message background, {author.mention}! This will do nicely!")



