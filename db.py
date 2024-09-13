from mysql.connector import connect, Error
import requests
import os

class CMDB:
    def __init__(self):
        try:
            self.connection = connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""), # REDACTED
                database=os.getenv("DB_NAME", "gabriel")
            )
        except Error as e:
            print(e)

    # CTI notifies threat, check if assets are affected
    def fetchAsset(self, vendor: str, versione: str, prodotto: str):
        query = "SELECT Hostname, SDL, Value FROM cmdb WHERE vendor=%s and versione=%s and Prodotto=%s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (vendor, versione, prodotto))
            results = cursor.fetchall()
            self.connection.commit()
        vuln_assets = []
        for result in results:
            asset = {'Hostname' : result[0], 'SDL' : result[1], 'Value':result[2], 'Contract': self.get_plan(result[1])}
            vuln_assets.append(asset)
        return vuln_assets
            

    # If SIEM detects a new device
    def addToDB(self, vendor: str, software: str, prodotto: str, versione: str, hostname: str, sdl: str):
        query = "INSERT INTO cmdb (vendor, software, prodotto, versione, hostname, sdl) VALUES (%s, %s, %s, %s, %s, %s);"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (vendor, software, prodotto, versione, hostname, sdl))
            self.connection.commit()

    # If HOSTNAME updates to a new VERSIONE:
    def updateAsset(self, hostname: str, versione: str):
        query = "UPDATE cmdb SET Versione = %s WHERE Hostname = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (versione, hostname))
            self.connection.commit()

    # If HOSTNAME is no longer an asset
    def removeFromDB(self, hostname: str):
        query = "DELETE FROM cmdb WHERE Hostname = %s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (hostname,))
            self.connection.commit()    

    def choose_ops(self):
        query = "SELECT email, id FROM operatori ORDER BY Numero_ticket ASC LIMIT 1;"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            self.connection.commit()
        # Eseguire query sulla tabella degli operatori e ritornare una lista con elemento un dizionario con webex id ed email dell'operatore
        return (result[0][0], result[0][1])
    
    def add_ticket(self, id, hostname, sdl, room_id):
        sql = "insert into ticket (operatore_id, Hostname, SDL, Room_id) values (%s, %s, %s, %s);"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (id, hostname, sdl, room_id))            
            self.connection.commit()
        return
    
    def delete_ticket(self, room_id):
        sql = "delete from ticket where room_id=%s;"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (room_id,))
            self.connection.commit()

    def get_plan(self, sdl):
        query = "select Tipo from contratti where ID=%s;"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (sdl,))
            result = cursor.fetchall()
        return result[0][0]

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
