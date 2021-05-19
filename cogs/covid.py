import discord
from discord.ext import commands, tasks
import aiohttp

class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.state_api = 'https://api.covid19india.org/data.json'
        # self.district_api = 'https://api.covid19india.org/state_district_wise.json'
        self.state_code = {
            "TT":"Total",
            "AN":"Andaman and Nicobar Islands",
            "AP":"Andhra Pradesh",
            "AR":"Arunachal Pradesh",
            "AS":"Assam",
            "BR":"Bihar",
            "CH":"Chandigarh",
            "CT":"Chhattisgarh",
            "DN":"Dadra and Nagar Haveli and Daman and Diu",
            "DL":"Delhi",
            "GA":"Goa",
            "GJ":"Gujarat",
            "HR":"Haryana",
            "HP":"Himachal Pradesh",
            "JK":"Jammu and Kashmir",
            "JH":"Jharkhand",
            "KA":"Karnataka",
            "KL":"Kerala",
            "LA":"Ladakh",
            "LD":"Lakshadweep",
            "MP":"Madhya Pradesh",
            "MH":"Maharashtra",
            "MN":"Manipur",
            "ML":"Meghalaya",
            "MZ":"Mizoram",
            "NL":"Nagaland",
            "OR":"Odisha",
            "PY":"Puducherry",
            "PB":"Punjab",
            "RJ":"Rajasthan",
            "SK":"Sikkim",
            "UN":"State Unassigned",
            "TN":"Tamil Nadu",
            "TG":"Telangana",
            "TR":"Tripura",
            "UP":"Uttar Pradesh",
            "UT":"Uttarakhand",
            "WB":"West Bengal"
        }
        self.catche.start()
    
    @tasks.loop(seconds=43200)
    async def catche(self):
        async with aiohttp.ClientSession() as session:
            result1 = await session.get(self.state_api)
            catche = await result1.json()
            catche = catche['statewise']
            self.state_catche = {}
            for i in catche:
                self.state_catche[i['statecode']] = i
            # result2 = await session.get(self.district_api)
            # self.district_catche = await result2.json()
        await session.close()
    
    @commands.command(
        name='state',
        description='Gives you the covid info about the state you want.\n**Example:** ?state wb',
        aliases=['s']
    )
    @commands.guild_only()
    async def state(self, ctx, *, state:str="TT"):
        if not state.upper() in self.state_code.keys():
            embed = discord.Embed()
            embed.color = 0xFF0000
            embed.title = "Please Check the state codes from the list below"
            description = ""
            for key,val in self.state_code.items():
                description = description + key + " → " + val + "\n"
            embed.description=description
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        else:
            data = self.state_catche[state.upper()]
            embed = discord.Embed()
            embed.title = f'📊 {data["state"]}'
            embed.color = 0x00FF00
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.add_field(name="🦠 Active", value=data['active'], inline=False)
            embed.add_field(name='😷 Confirmed', value=data['confirmed'],inline=False)
            embed.add_field(name='☠️ Deaths', value=data['deaths'], inline=False)
            embed.add_field(name='✅ Recovered', value=data['recovered'], inline=False)
            embed.add_field(name='🕐 Last Updated Time', value=data['lastupdatedtime'], inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text=data['statenotes'] if len(data['statenotes'])>0 else None)

            await ctx.send(content=ctx.author.mention, embed=embed)
    
    # @commands.command()
    # @commands.guild_only()
    # async def district(self, ctx):
    #     await ctx.send('district')
    

def setup(bot):
    bot.add_cog(Covid(bot))