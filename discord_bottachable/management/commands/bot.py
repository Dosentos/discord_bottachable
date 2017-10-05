from discord_bottachable import settings
from django.core.management.base import BaseCommand
# from discord_bottachable.models import User, Attachment, Tag

import asyncio
import discord
import re

client = discord.Client()
class Command(BaseCommand):
    help = 'discord-bottachable runner management command'

    def handle(self, *args, **kwargs):
        client.run(settings.DISCORD_BOT_TOKEN)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')


    elif message.content.startswith('!SaveMe!'):
            message_saved, error_message = handle_link(message.content)
            if message_saved:
                await client.send_message(message.channel, "Thank you, link published on discord-bottachable.discordapp.com")
            else:
                await client.send_message(message.channel, error_message)

# This function handles all the 
def handle_link(msg):
    errors = '-----------ERRORS-----------\n'
    msg = msg.strip('!SaveMe!')
    if 'http://' in msg or 'https://' in msg or 'www.' in msg:
        message_dict = split_link_message(msg)

        if message_dict['title'] != '':
            pass
        else:
            errors = "%s - Title is required\n" % (errors)

        if message_dict['tags'] != '':
            pass
        else:
            errors = "%s " % (errors)
    else:
        errors = "%s Links should contain 'https:', 'http:' or 'www.' prefix" % (errors)

    bot_response = "url: %s\n title: %s\n tags: %s" %(message_dict['url'],message_dict['title'],message_dict['tags'])
    print(bot_response)
    return (False, errors)

# This method splits user's message to url, title and tags.
def split_link_message(msg):
    message_dict = {'url':'', 'title':'', 'tags': ''}
    title = False
    tags = False
    url_set = False
    splitted_message = re.split('(tags: |title:)', msg)

    for part in splitted_message:
        if 'http://' in part or 'https://' in part or 'www.' in part:
            if not url_set:
                message_dict['url'] = part
                url_set = True
            else:
                print("Warning, user's message contains more than one link")

        elif 'title:' in part:
            title = True
            tags = False

        elif 'tags:' in part:
            title = False
            tags = True

        else:
            if title == True and tags == False:
                message_dict['title'] = "%s %s" %(message_dict['title'], part)
            elif tags == True and title == False:
                if message_dict['tags'] == '':
                    message_dict['tags'] == part
                else:
                    message_dict['tags'] = "%s, %s" %(message_dict['tags'], part)

    message_dict['url'].strip()
    message_dict['title'].strip()
    message_dict['tags'].strip()
    return message_dict;