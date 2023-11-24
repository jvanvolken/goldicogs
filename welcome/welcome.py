# Image and File Manipulation Libraries
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageFont

# Discord Bot Libraries
import discord
from redbot.core import commands


# Cog Directory in Unreal Engine
docker_cog_path = "/data/cogs/Welcome"

# Necessary Directories withing the Cog Directory
Avatars_Dir       = docker_cog_path + "/Avatars"
Font_Dir          = docker_cog_path + "/Fonts"

# Define Filepaths
background_image  = docker_cog_path + "/welcome_background.jpg"
avatar_background = docker_cog_path + "/avatar_background.png"
welcome_font      = Font_Dir + "/TheCottage.ttf"


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
            avatar_image = Image.open(avatar_filename)

            # Records the width and height of the background and avatar images
            background_width, background_height = welcome_background.size
            avatar_width, avatar_height = avatar_image.size

            # Resize avatar image to fit the background
            resize_ratio = (background_height / avatar_height) * 0.4
            resized_avatar = avatar_image.resize((round(avatar_width * resize_ratio), round(avatar_height * resize_ratio)), Image.ANTIALIAS)
            resized_width, resized_height = resized_avatar.size

            #Apply GaussianBlur filter
            blurred_background = welcome_background.filter(ImageFilter.GaussianBlur(5))

            # Set the background's margin
            margins = background_width * 0.07

            # Draw shadow and save new background image
            draw = ImageDraw.Draw(blurred_background, "RGBA")
            draw.rounded_rectangle(((margins, margins), (background_width - margins, background_height - margins)), fill=(0, 0, 0, 160), radius = 10)

            # Set welcome message and desired width
            welcome_message = f"Welcome to the treehouse, {author.display_name}!"
            message_width = (background_width - (margins * 2)) * 0.75

            # Increase font size until it fills the desired space
            fontsize = 1
            font = ImageFont.truetype(welcome_font, fontsize)
            while font.getsize(welcome_message)[0] < message_width:
                fontsize += 1
                font = ImageFont.truetype(welcome_font, fontsize)

            # Overlay text onto blurred background
            position = (round((background_width - message_width)/2), background_height - round(margins) - font.getsize(welcome_message)[1]/2)
            draw.text(position, welcome_message, (255,255,255), font = font)
            
            # Construct a circular mask for the avatar image
            mask = Image.new('L', resized_avatar.size, 0)
            draw = ImageDraw.Draw(mask) 
            draw.ellipse((0, 0) + resized_avatar.size, fill=255)
            
            # Overlay avatar onto blurred background
            position = (round((background_width - resized_width)/2), round(margins * 1.5))
            blurred_background.paste(resized_avatar, position, mask)


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



