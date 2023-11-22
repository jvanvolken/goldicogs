from .hellobot import HelloBot


async def setup(bot):
    await bot.add_cog(HelloBot(bot))