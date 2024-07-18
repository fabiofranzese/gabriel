from mysql.connector import connect, Error
import requests

class CMDB:
    def __init__(self):
        try:
            self.connection = connect(
                host="localhost",
                user="root",
                password="rootino123", # Nascondi sto schifo
                database="gabriel"
            )
        except Error as e:
            print(e)

    # CTI notifies threat, check if assets are affected
    def fetchAsset(self, vendor: str, versione: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT Prodotto, Hostname, SDL FROM cmdb WHERE vendor='{vendor}' and versione='{versione}';")
            result = cursor.fetchall()
            for row in result:
                print(row)

    # If SIEM detects a new device
    def addToDB(self, vendor: str, software: str, prodotto: str, versione: str, hostname: str, sdl: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO cmdb VALUES('{vendor}','{software}','{prodotto}','{versione}','{hostname}','{sdl}')")
            self.connection.commit()


    # If HOSTNAME updates to a new VERSIONE:
    def updateAsset(self, hostname: str, versione: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"UPDATE cmdb SET Versione = '{versione}' WHERE Hostname = '{hostname}';")
            self.connection.commit()

    # If HOSTNAME is no longer an asset
    def removeFromDB(self, hostname: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM cmdb WHERE Hostname = '{hostname}';")
            self.connection.commit()


   # Fetch events from SIEM
    def fetchEventsFromSIEM(self, siem_url: str, api_key: str):
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(siem_url, headers=headers)
            response.raise_for_status()
            events = response.json()
            return events
        except requests.exceptions.RequestException as e:
            print(f"Error fetching events from SIEM: {e}")
            return None

    # Process SIEM events to update CMDB
    def processSIEMEvents(self, events):
        for event in events:
            action = event.get('action')
            hostname = event.get('hostname')
            versione = event.get('versione')
            vendor = event.get('vendor')
            software = event.get('software')
            prodotto = event.get('prodotto')
            sdl = event.get('sdl')

            if action == 'add':
                self.addToDB(vendor, software, prodotto, versione, hostname, sdl)
            elif action == 'update':
                self.updateAsset(hostname, versione)
            elif action == 'remove':
                self.removeFromDB(hostname)

# Esempio di utilizzo
cmdb = CMDB()
siem_events = cmdb.fetchEventsFromSIEM("http://siem.example.com/api/events", "API_KEY_HERE")
if siem_events:
    cmdb.processSIEMEvents(siem_events)


cmdb.removeFromDB("duel0")
cmdb.fetchAsset("Francesco","22.04")
