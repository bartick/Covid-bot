import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import psycopg2
import typing

from utils.menu import paginate

load_dotenv('../.env')

class TagsCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.connect_database.start()
    
    @tasks.loop(count=1)
    async def connect_database(self):
        self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        self.cur = self.conn.cursor()
    
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def tag(self,ctx, *,tags:str=""):
        command =  """SELECT REPLY FROM tags WHERE LOWER(TAGS) = %s"""
        self.cur.execute(command,(tags.lower(),))
        reply = self.cur.fetchone()
        if not reply==None:
            await ctx.send(reply[0])
        else:
            await ctx.send('No Tags found...')

    @tag.command()
    @commands.guild_only()
    @commands.check_any(commands.is_owner(),commands.has_permissions(manage_guild=True))
    async def create(self, ctx, *,tags:str=""):
        new_tag = tags.split("\"")
        if len(new_tag)!=3:
            new_tag = tags.split(' ')
            reply = tags[len(new_tag[0]):].strip()
            tag = new_tag[0]
        else:
            reply = tags[len(new_tag[1])+2:].strip()
            tag = new_tag[1]
        if tag.lower() in ['create','claim','search','delete','owned','transfer']:
            await ctx.send('You cannot create these tags')
            return
        command = """SELECT REPLY FROM tags WHERE LOWER(TAGS) = %s"""
        self.cur.execute(command,(tag.lower(),))
        if not self.cur.fetchone()==None:
            await ctx.send('This tag is already present. Please use another tag...')
            return
        command = """INSERT INTO tags (TAGS, OWNER, SERVER, REPLY) VALUES (%s, %s, %s, %s)"""
        self.cur.execute(command,(tag,ctx.author.id,ctx.guild.id,reply))
        self.conn.commit()
        await ctx.send('Successfully added tag!')

    @tag.command()
    @commands.guild_only()
    @commands.check_any(commands.is_owner(),commands.has_permissions(manage_guild=True))
    async def claim(self, ctx, *, tags:str=""):
        command = """SELECT OWNER FROM tags WHERE LOWER(TAGS) = %s AND SERVER = %s"""
        self.cur.execute(command, (tags.lower(),ctx.guild.id))
        owner = self.cur.fetchone()
        if not owner==None:
            user = self.bot.get_user(owner[0])
            if user==None or owner not in ctx.guild.members:
                command = """UPDATE tags SET OWNER = %s WHERE LOWER(TAGS) = %s AND SERVER = %s"""
                self.cur.execute(command,(ctx.author.id, tags.lower(), ctx.guild.id))
                self.conn.commit()
            else:
                await ctx.send('Owner already in the server.')
        else:
            await ctx.send('Tag not found...')

    @tag.command()
    @commands.guild_only()
    async def search(self, ctx, *,tags:str=""):
        pass

    @tag.command()
    @commands.guild_only()
    async def delete(self, ctx, *, tags:str=""):
        command = """DELETE FROM tags WHERE LOWER(TAGS) = %s AND OWNER = %s"""
        self.cur.execute(command,(tags.lower(),ctx.author.id))
        rows_deleted = self.cur.rowcount
        if rows_deleted>0:
            self.conn.commit()
            await ctx.send('Tag successfully deleted...')
        else:
            await ctx.send('Cannot delete a tag that is not present.')

    @tag.command()
    @commands.guild_only()
    async def owned(self, ctx, user:typing.Union[discord.Member, discord.User]):
        pass
        # user = ctx.author if user==None else user
        # command = """SELECT TAGS FROM tags WHERE OWNER = %s"""
        # self.cur.execute(command,(user.id,))
        # tags = self.cur.fetchall()
        # total_tags = []
        # for i in range(int(len(tags)/10)):
        #     pass
    
    @tag.command()
    @commands.guild_only()
    async def transfer(self, ctx, user:typing.Union[discord.Member, discord.User], *, tags:typing.Optional[str]):
        command = """UPDATE tags SET OWNER = %s WHERE OWNER = %s AND SERVER = %s"""
        if not tags==None:
            command += """ AND LOWER(TAGS) = %s"""
            self.cur.execute(command,(user.id, ctx.author.id, ctx.guild.id, tags))
        else:
            self.cur.execute(command,(user.id, ctx.author.id, ctx.guild.id))
        rows_updated = self.cur.rowcount
        if rows_updated>0:
            self.conn.commit()
            await ctx.send('Successfully transfered tag')
        else:
            await ctx.send('You cannot transfer these tags')


def setup(bot):
    bot.add_cog(TagsCmd(bot))