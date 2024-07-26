import requests
import private

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
    if asset != None:
        client = asset.get('Client')
    else:
        client = 'Unknown'
    room_name = f"Vulnerabilty {cve.get('Id', 'Unknown')}; Client: {client}"
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
    for op in ops:
        params = {
        'roomId': room_id,
        'personEmail': op["email"]
        }
        res = requests.post(url, headers=headers, json=params)
    

def send_message(cve, asset, room_id):
    '''
    Invia un messaggio con tutte le informazioni necessarie sulla vulnerabilità scoperta
    '''
    url = base_url + '/v1/messages'
    message = ""
    for field in cve:
        message += f"\n{field}: {cve.get(field)}"
    if asset != None:
        for field in asset:
            message += f"\n{field}: {asset.get(field)}"
    params = {
        'roomId': room_id,
        'markdown': message
    }
    res = requests.post(url, headers=headers, json=params)
    
def choose_ops():
    # TO DO: Selezionare operatori in base alla loro disponibilità
    return private.ops

def high_risk(cve, asset):
    if asset == None:
        send_message(cve, asset, private.high_cvss_roomid)
    else:
        ops = choose_ops()
        room_id = create_room(cve, asset)
        invite_ops(ops, room_id)
        send_message(ops, cve, asset, room_id)


def low_risk(cve, asset):
    room_id = private.low_cvss_roomid
    send_message(cve, asset, room_id)

def main():
    cve = {'Description': '#Docker: risolta vulnerabilità con gravità “critica” nel plugin #Authz del progetto open source #Moby', 'Cvss': 7, 'Resources': 'https://www.csirt.gov.it/contenuti/sanata-vulnerabilita-in-moby-per-docker-al02-240726-csirt-ita'}
    high_risk(cve, None)

if __name__ == "__main__":
    main()