  
import asyncio

async def paginate(msg, embeds, author, bot):
	emojis=['⬅️','➡️','🗑️']
	for emoji in emojis:
		await msg.add_reaction(emoji)
	check = lambda p: p.message_id == msg.id and p.user_id == author.id and p.emoji.name in emojis
	index=0
	while True:
		try:
			done, pending=await asyncio.wait([bot.wait_for('raw_reaction_add',check=check),bot.wait_for('raw_reaction_remove',check=check)], return_when=asyncio.FIRST_COMPLETED, timeout=60)
			reaction = done.pop().result()
			if reaction.emoji.name==emojis[0]:
				index-=1
				if index<0:
					index=0
					continue
				await msg.edit(embed=embeds[index])
			elif reaction.emoji.name==emojis[1]:
				index+=1
				if index>len(embeds)-1:
					index=len(embeds)-1
					continue
				await msg.edit(embed=embeds[index])
			else:
				await msg.delete()
				break
		except Exception:
			embeds[index].color=0xFF0000
			await msg.edit(embed=embeds[index])
			break