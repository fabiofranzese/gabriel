import configparser
import json
import asyncio
from datetime import date, datetime
import time

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

def ChannelMessages():
    # some functions to parse json date
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()

            if isinstance(o, bytes):
                return list(o)

            return json.JSONEncoder.default(self, o)


    # Reading Configs
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Setting configuration values
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']

    api_hash = str(api_hash)

    phone = config['Telegram']['phone']
    username = config['Telegram']['username']

    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash)

    async def main(phone):
        await client.start()
        print("Client Created")
        # Ensure you're authorized
        if await client.is_user_authorized() == False:
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        me = await client.get_me()
        #Questa parte commentata solo se si vuole inserire in input un gruppo Telegram a scelta

        #user_input_channel = input('enter entity(telegram URL or entity id):')
        #if user_input_channel.isdigit():
        #    entity = PeerChannel(int(user_input_channel))
        #else:
        #    entity = user_input_channel
        #my_channel = await client.get_entity(entity)

        #In questo modo il gruppo Telegram è scritto già nel codice
        my_channel = "https://t.me/CSIRT_italia"
        offset_id = 0
        limit = 1
        all_messages = []
        total_messages = 0
        total_count_limit = 0

        i=0
        while i<=5: #Numero di messaggi che vogliamo leggere
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
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
            
        with open('channel_messages.json', 'w') as outfile:
            json.dump(all_messages, outfile, cls=DateTimeEncoder)

    with client:
        client.loop.run_until_complete(main(phone))


def letturajson():
    import json
    import time


    # Nome del file JSON da aprire
    nome_file = "channel_messages.json"

    # Apre il file in modalità lettura
    with open(nome_file, "r") as file:
        # Carica il contenuto del file JSON in un dizionario
        dati = json.load(file)

    # Stampa il contenuto del dizionario
        for m in dati:
            print("ALERT:",m["message"])
            print("DATA:",m["date"])

# Chiamata ai programmi
if __name__ == "__main__":
    def esegui_ogni_40_minuti():
        while True:
            # Il tuo codice qui
            print("-----Esecuzione ogni 10 secondi-----")
            ChannelMessages()
            letturajson()
            time.sleep(10)  # tempo in secondi
esegui_ogni_40_minuti()
