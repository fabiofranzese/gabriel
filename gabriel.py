import mysql.connector
import requests
from webexteamssdk import WebexTeamsAPI
import time

def send_webex_notification(asset_id, cvss_score):
    api = WebexTeamsAPI(access_token="") # TODO: token per il SOC
    message = f"Asset {asset_id} vulnerability. CVSS: {cvss_score}"
    api.messages.create(roomId="", text=message) # TODO: inserire room ID


def connect_to_cmdb():
    return mysql.connector.connect(
        host="localhost",
        user="gabriel",
        password="", # TODO: implementare la open di un file sul nostro sistema. Niente leak di credenziali qui.
        database=""
    )

def check_asset_in_cmdb(asset_id):
    conn = connect_to_cmdb()
    cursor = conn.cursor()
    query = "SELECT asset_id, cvss_score FROM assets WHERE asset_id = %s" # Ci prendiamo il parametro della funzione
    cursor.execute(query, (asset_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_threat_notifications():
    # TODO: implementare API e capire dove acchiappare gli alert
    talos_notifications = requests.get("URL_TALOS_API").json()
    telegram_notifications = requests.get("URL_TELEGRAM_API").json()
    discord_notifications = requests.get("URL_DISCORD_API").json()
    
    # Per ora ritorniamo un JSON
    return talos_notifications + telegram_notifications + discord_notifications

def process_notifications(notifications):
    for notification in notifications:
        asset_id = notification.get("asset_id")
        asset = check_asset_in_cmdb(asset_id) # Qui facciamo la query
        if asset:
            asset_id, cvss_score = asset
            if cvss_score > 7:
                send_webex_notification(asset_id, cvss_score)

def main():
    while True:
        try:
            notifications = get_threat_notifications()
            process_notifications(notifications)
        except Exception as e:
            print(f"ERRORE: {e}")
        # Sleep 60.
        time.sleep(60)

if __name__ == "__main__":
    main()