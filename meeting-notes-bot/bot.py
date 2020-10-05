import discord
import os
import json
from dotenv import load_dotenv

client = discord.Client()
load_dotenv()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!regnotes'):
        message_args = message.content.split()

        if len(message_args) != 3:
            await message.channel.send('Bad format! Try something different')
            return

        json_entry = message_args[1]
        link = message_args[2]

        meeting_link_data = await open_json_file('./meeting-note-links.json')

        if json_entry in meeting_link_data:
            await message.channel.send(f'An entry already exists for {json_entry}! Updating...')

        meeting_link_data.update({json_entry: link})

        await save_to_json_file(meeting_link_data, './meeting-note-links.json')

        await message.channel.send(f'Saved link for {json_entry}')

    if message.content.startswith('!servenotes'):
        message_args = message.content.split()

        if len(message_args) != 2:
            await message.channel.send('Bad format! Try something different')
            return

        json_entry = message_args[1]

        meeting_link_data = await open_json_file('./meeting-note-links.json')

        if json_entry not in meeting_link_data:
            await message.channel.send(f'No entry exists for {json_entry}')
            return

        await message.channel.send(f'Here\'s that link! {meeting_link_data[json_entry]}')


async def open_json_file(fp):
    with open(fp) as file:
        return json.load(file)


async def save_to_json_file(data, fp):
    with open(fp, 'w') as file:
        json.dump(data, file)


def main():
    client.run(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()
