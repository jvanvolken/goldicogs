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
        
        # Setup a circular mask
        avater_image = Image.open(avatar_filename)
        masksize = avater_image.size
        mask = Image.new('L', masksize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + masksize, fill=255)
        
        # Apply the mask to the avatar image
        # avater_image = Image.open(avatar_filename)
        # new_avatar = ImageOps.fit(avater_image, mask.size, centering=(0.5, 0.5))
        # new_avatar.putalpha(mask)
        # new_avatar.save(avatar_filename)
        
        # Checks if background image path is a valid file, send just member avatar instead.
        if Path(background_image).is_file():
            # Opens the background image and the avatar image
            welcome_background = Image.open(background_image)

            # Records the width and height of the background image
            width, height = welcome_background.size

            #Apply GaussianBlur filter
            blurred_background = welcome_background.filter(ImageFilter.GaussianBlur(5))

            # Set the background's margin
            margins = width * 0.07

            # Draw shadow and save new background image
            draw = ImageDraw.Draw(blurred_background, "RGBA")
            draw.rounded_rectangle(((margins, margins), (width - margins, height - margins)), fill=(0, 0, 0, 160), radius = 10)

            # Overlays avatar onto background
            blurred_background.paste(avater_image, (0, 0), mask)

            # Saves the blurred background as the avatar background
            blurred_background.save(avatar_background)

            # Sends a welcome message in the command's origin channel
            await channel.send(f"Hello {author.mention}!", file = discord.File(avatar_filename))
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



