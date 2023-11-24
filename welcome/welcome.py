# Image and File Manipulation Libraries
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFilter

# Discord Bot Libraries
import discord
from redbot.core import commands

docker_cog_path = "/data/cogs/Welcome"

Avatars_Dir       = docker_cog_path + "/Avatars"
background_image  = docker_cog_path + "/welcome_background.jpg"
avatar_background = docker_cog_path + "/avatar_background.png"

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
        Path(Avatars_Dir).mkdir(parents=True, exist_ok=True)
        avatar_filename = Avatars_Dir + f"/avatar_{author.id}.png"

        # Download and save the avatar image
        await author.avatar.save(avatar_filename)
        
        # Checks if background image path is a valid file, send just member avatar instead.
        if Path(background_image).is_file():
            # Opens the background and avatar images
            welcome_background = Image.open(background_image)
            avater_image = Image.open(avatar_filename)

            # Records the width and height of the background and avatar images
            background_width, background_height = welcome_background.size
            avatar_width, avatar_height = avater_image.size

            #Apply GaussianBlur filter
            blurred_background = welcome_background.filter(ImageFilter.GaussianBlur(5))

            # Set the background's margin
            margins = background_width * 0.07

            # Draw shadow and save new background image
            draw = ImageDraw.Draw(blurred_background, "RGBA")
            draw.rounded_rectangle(((margins, margins), (background_width - margins, background_height - margins)), fill=(0, 0, 0, 160), radius = 10)

            # Construct a circular mask for the avatar image
            mask = Image.new('L', (avatar_width, avatar_height), 0)
            draw = ImageDraw.Draw(mask) 
            draw.ellipse((0, 0, avatar_width, avatar_height), fill=255)
            
            # Overlays avatar onto background
            blurred_background.paste(avater_image, ((background_width - avatar_width)/2, margins * 1.05), mask)

            # Saves the blurred background as the avatar background
            blurred_background.save(avatar_background)

            # Sends a welcome message in the command's origin channel
            await channel.send(f"Welcome to the treehouse, {author.mention}! Make yourself at home!", file = discord.File(avatar_background))
        else:
            await channel.send(f"Hello {author.mention}!", file = discord.File(avatar_filename))


    @commands.command()
    async def set_background(self, ctx):
        """Sets the background of the welcome message!"""
        
        # Get important information about the context of the command
        channel = ctx.channel
        author = ctx.message.author

        # Download and save the attachment file
        await ctx.message.attachments[0].save(background_image)

        # Sends message in the command's origin channel
        await channel.send(f"Thanks for the new Welcome Message background, {author.mention}! This will do nicely!")



