import discord

def split(arg):
    arg = str(arg)
    return [char for char in arg]

addList = []
block= []

TOKEN_AUTH = "OBSCURIFIED FOR OBV REASONS"

dc = discord.Client()

@dc.event
async def on_ready():
    print('We have logged in as {0.user}'.format(dc))

@dc.event
async def on_message(message):
    if message.author == dc.user:
        return
    
    content = message.content.lower()
    if content == "mod!help":
        await message.channel.send("```mod!add [user]\n  add a user to the no mention list\n\nmod!block [user]\n  block a user from mentioning\n\nmod!list\n  see the no mention list\n\nmod!blist\n  see the mention block list\n\nmod!dis\n  get dissed```")

    if content.startswith("mod!add"):
        person = ''.join(split(content)[8:len(content)])

        person_id = ''
        for char in split(person):
            if char.isdigit():
                person_id = person_id + char

        if (person_id):
            if message.guild.get_member(int(person_id)) or int(person_id) == message.guild.owner_id:
                addList.append(person)
                await message.channel.send("Added {} to the list!".format(person))
            else:
                await message.channel.send("That person does not exist!")
        else:
            await message.channel.send("Make sure you mention the person!")
    
    if content.startswith("mod!block"):
        person = ''.join(split(content)[10:len(content)])

        person_id = ''
        for char in split(person):
            if char.isdigit():
                person_id = person_id + char

        if (person_id):
            if message.guild.get_member(int(person_id)) or int(person_id) == message.guild.owner_id:
                block.append(person)
                await message.channel.send("Blocked {} from mentioning!".format(person))
            else:
                await message.channel.send("That person does not exist!")
        else:
            await message.channel.send("Make sure you mention the person!")

    if content == "mod!list":
        send = ''

        i = 1
        for items in addList:
            send += str(i) + ". " + items + "\n"
            i += 1

        if send:
            await message.channel.send(send)
        else:
            await message.channel.send("No one is in the list!")

    if content == "mod!blist":
        send = ''

        i = 1
        for items in block:
            send += str(i) + ". " + items + "\n"
            i += 1

        if send:
            await message.channel.send(send)
        else:
            await message.channel.send("No one is in the list!")

    if ''.join(split(content)[0:4]) != 'mod!':
        class breakIt(Exception): pass

        try:
            for checks in addList:
                for words in content.split():
                    if checks == words:
                        await message.delete()
                        raise breakIt

        except breakIt:
            pass
        
        canMention = True
        for items in block:
            if message.author == items:
                canMention = False
        
        if canMention:
            if split(content).count("<") > 0:
                index = split(content).index("<")
                if ''.join(split(content)[index:index+3]) == "<@!":
                    await message.delete()
    
    if content == 'mod!dis':
        await message.channel.send("I GOT NOTHING, IM NOT FUNNY :(")

dc.run(TOKEN_AUTH)
