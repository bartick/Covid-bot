import discord
from discord.ext import commands

class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        return
    
    @commands.command(
        name='members',
        description='Tells you total server member.',
        aliases=['mbs']
    )
    @commands.guild_only()
    @commands.check_any(commands.has_permissions(manage_guild=True), commands.has_role(782638194217844770))
    async def members(self, ctx):
        embed = discord.Embed(color=0x00FFFF)
        embed.title = "Total Members"
        embed.description = ctx.guild.member_count
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Extra(bot))