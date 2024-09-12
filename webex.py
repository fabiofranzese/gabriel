import requests
import private
import db
from gabriel import cmdb


ops_list = private.ops
access_token = private.access_token
base_url = 'https://webexapis.com'
headers = {
    'Authorization': f'Bearer {private.access_token}',
    'Content-Type': 'application/json'
    }


def create_room(cve, asset):
    '''
    Crea room Webex
    '''
    url = base_url + '/v1/rooms'
    '''if asset != None:
        client = asset.get('Client')
    else:
        client = 'Unknown'''
    room_name = f"Vulnerabilty on {cve.get('Vendor')} {cve.get('Prodotto')}; SDL: {asset['SDL']}"
    params = {
        'title': room_name,
        'description': cve.get('Description')
    }
    res = requests.post(url, headers=headers, json=params)

    return res.json()['id']

def invite_ops(ops, room_id):
    '''
    Invita gli operatori nella room Webex
    '''
    url = base_url + '/v1/memberships'
    params = {
    'roomId': room_id,
    'personEmail': ops
    }
    res = requests.post(url, headers=headers, json=params)
    

def send_message(cve, asset, room_id, risk, nome):
    '''
    Invia un messaggio con tutte le informazioni necessarie sulla vulnerabilità scoperta
    '''
    url = base_url + '/v1/messages'
    if not nome:
        message = 'È stata rilevata una nuova vulnerabilità!\nEcco i dettagli:'
    else:
        message = f"Ciao {nome}, è stata rilevata una nuova vulnerabilità!\nPuoi eseguire i seguenti comandi:\n- Invia 'Done' se la vulnerabilità è stata gestita;\n- Invia 'Help' per avere supporto.\n\nEcco i dettagli:"
    for field in cve:
        message += f"\n- {field}: {cve.get(field)}"
    if asset != None:
        for field in asset:
            if field.lower() == 'value':
                continue 
            message += f"\n- {field}: {asset.get(field)}"
        message += f"\nRisk: {risk}"
    params = {
        'roomId': room_id,
        'markdown': message
    }
    res = requests.post(url, headers=headers, json=params)
    
def delete_room(room_id):
    # Funzione che rileva quando l'operatore invia il messaggio 'done' ed elimina la stanza
    url = base_url + '/v1/rooms/' + room_id
    params = {
        'roomId': room_id,
    }
    print(room_id)
    res = requests.delete(url, headers=headers, json=params)
    print(res)
    db.CMDB.delete_ticket(cmdb, room_id)

def high_risk(cve, asset, risk):
    if asset == None:
        send_message(cve, asset, private.high_cvss_roomid)
    else:
        ops = db.CMDB.choose_ops(cmdb)
        room_id = create_room(cve, asset)
        db.CMDB.add_ticket(cmdb, ops[1], asset["Hostname"], asset["SDL"], room_id)
        invite_ops(ops[0], room_id)
        send_message(cve, asset, room_id, risk, 'Fabio')


def low_risk(cve, asset, risk):
    room_id = private.low_cvss_roomid
    send_message(cve, asset, room_id, risk, None)

def main():
    cve = {'Description': '#Docker: risolta vulnerabilità con gravità “critica” nel plugin #Authz del progetto open source #Moby', 'Cvss': 7, 'Resources': 'https://www.csirt.gov.it/contenuti/sanata-vulnerabilita-in-moby-per-docker-al02-240726-csirt-ita'}
    high_risk(cve, None)

if __name__ == "__main__":
    main()