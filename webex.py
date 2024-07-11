import requests
import private

# Token Bot Gabriel
access_token = private.access_token
ops_list = private.ops
base_url = 'https://webexapis.com'
headers = {
'Authorization': f'Bearer {access_token}',
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
    

def send_message(vuln, client_id, asset_id, cvss, room_id):
    '''
    Invia un messaggio con tutte le informazioni necessarie sulla vulnerabilità scoperta
    '''
    url = base_url + '/v1/messages'
    message = f"Vulnerabilty: {vuln}\nClient: {client_id}\nAsset: {asset_id}\nCVSS: {cvss}"
    params = {
        'roomId': room_id,
        'markdown': message
    }
    res = requests.post(url, headers=headers, json=params)
    
def high_cvss(ops, vuln, client_id, asset_id, cvss):
    room_id = create_room(vuln, client_id)
    invite_ops(ops, room_id)
    send_message(vuln, client_id, asset_id, cvss, room_id)


def low_cvss(vuln, client_id, asset_id, cvss):
    room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vMzlmNjM2YjAtM2Y3Ny0xMWVmLWFhZTAtYzU3ZTM4ZmY5Nzg5'
    send_message(vuln, client_id, asset_id, cvss, room_id)

def choose_ops(ops_list):
    # TO DO: Selezionare operatori in base alla loro disponibilità
    return ops_list

def main():
    cvss = 6
    vuln = "Cisco Routers Firewall"
    client_id = "Maticmind"
    asset_id = "Router 2840"
    if cvss > 7:
        ops = choose_ops(ops_list)
        high_cvss(ops, vuln, client_id, asset_id, cvss)
    else:
        low_cvss(vuln, client_id, asset_id, cvss)

if __name__ == "__main__":
    main()