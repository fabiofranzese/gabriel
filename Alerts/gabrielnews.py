import json
import sys
import os
#Adding parent directory as to the list of paths Python searches for modules to import private
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
import time
import private

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)

class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()

            if isinstance(o, bytes):
                return list(o)

            return json.JSONEncoder.default(self, o)

# Valori di configurazione
api_id = private.t_api
api_hash = str(private.t_hash)
phone = private.t_num
username = private.t_usr


# Crea client e si connette
client = TelegramClient(username, api_id, api_hash)

async def message_loop(phone):
        # some functions to parse json date
    await client.start()
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()
    #Questa parte commentata va usata solo se si vuole inserire in input un gruppo Telegram a scelta

    #user_input_channel = input('enter entity(telegram URL or entity id):')
    #if user_input_channel.isdigit():
    #    entity = PeerChannel(int(user_input_channel))
    #else:
    #    entity = user_input_channel
    #my_channel = await client.get_entity(entity)

    #In questo modo il gruppo Telegram è scritto già nel codice
    my_channel = "https://t.me/gabrielnewsPW"
    offset_id = 0
    limit = 1
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    i=0
    while i<=5: #Numero di messaggi che vogliamo leggere
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        
        for message in messages:
            all_messages.append(message.to_dict())
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
        i+=1
    with open('gabriel_messages.json', 'w') as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder)

def ChannelMessages():
    with client:
        client.loop.run_until_complete(message_loop(phone))

def main():
    ChannelMessages()

# Chiamata ai programmi
if __name__ == "__main__":
    main()