import requests
import private

ops_list = private.ops
access_token = private.access_token
base_url = 'https://webexapis.com'
headers = {
    'Authorization': f'Bearer {private.access_token}',
    'Content-Type': 'application/json'
    }

def create_room(vuln, client_id):
    '''
    Crea room Webex
    '''
    url = base_url + '/v1/rooms'
    room_name = f"Vulnerabilty {vuln}; Client: {client_id}"
    params = {
        'title': room_name,
        'description': f"Vulnerability on client {client_id} "
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
    

def send_message(vuln, client_id, asset_id, cvss, risk, room_id):
    '''
    Invia un messaggio con tutte le informazioni necessarie sulla vulnerabilità scoperta
    '''
    url = base_url + '/v1/messages'
    message = f"Vulnerabilty: {vuln}\nClient: {client_id}\nAsset: {asset_id}\nCVSS: {cvss}\n Risk: {risk}"
    params = {
        'roomId': room_id,
        'markdown': message
    }
    res = requests.post(url, headers=headers, json=params)
    
def high_risk(ops, vuln, client_id, asset_id, cvss, risk):
    room_id = create_room(vuln, client_id)
    invite_ops(ops, room_id)
    send_message(vuln, client_id, asset_id, cvss, risk, room_id)


def low_risk(vuln, client_id, asset_id, cvss, risk):
    room_id = private.low_cvss_roomid
    send_message(vuln, client_id, asset_id, cvss, risk, room_id)

def choose_ops():
    # TO DO: Selezionare operatori in base alla loro disponibilità
    return private.ops

def main():
    vuln = "Cisco Routers Firewall"
    client_id = "Maticmind"
    asset_id = "Router 2840"
    ops = choose_ops()
    high_risk(ops, vuln, client_id, asset_id, 8, 9.5)    
    low_risk(vuln, client_id, asset_id, 5, 2.3)

if __name__ == "__main__":
    main()