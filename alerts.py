'''
Prende tutti gli alerts da tutte le fonti, dalla cartella Alerts e contiene le funzioni per normalizzarli e fornirli a gabriel.py 
'''
import json
import re
import private
# from Alerts import csirt

# Per demo, import di gabrielnews
from Alerts import gabrielnews
'''
def get_csirt_cvss(message):
    pattern = re.compile(r'Rischio: (.+)')
    if pattern == None:
        return None
    match = pattern.search(message['message'])
    try:
        emoji = match.group(1).strip()
    except:
        return None
    if emoji == '🟡':
        return(5)
    elif emoji == '🟠':
        return (7)
    elif emoji == '🔴':
        return (9)
    else:
        return None

def get_csirt_link(message):
    pattern = re.compile(r'🔗 (.+)')
    match = pattern.search(message['message'])
    try:
        return match.group(1).strip()
    except:
        return None

def csirt_cves():
    csirt.ChannelMessages()
    cves = []
    with open('channel_messages.json', "r") as file:
        # Carica il contenuto del file JSON in un dizionario
        messages = json.load(file)
    for message in messages:
        cvss = get_csirt_cvss(message)
        if cvss == None:
            continue
        cve = {}
        cve['Description'] = message['message'].split("\n")[0]
        cve['Cvss'] = get_csirt_cvss(message)
        cve['Resources'] = get_csirt_link(message)
        cves.append(cve)
    return cves

'''

def get_gabriel_vendor(message):
    pattern = re.compile(r'Vendor: (.+)')
    #match = pattern.search(message['message'])
    match = pattern.search(message)
    return match.group(1).strip()

def get_gabriel_prodotto(message):
    pattern = re.compile(r'Prodotto: (.+)')
    match = pattern.search(message)
    return match.group(1).strip()

def get_gabriel_cvss(message):
    pattern = re.compile(r'Rischio: (.+)')
    match = pattern.search(message)
    emoji = match.group(1).strip()
    if emoji == '🟡':
        return(5)
    elif emoji == '🟠':
        return (7)
    elif emoji == '🔴':
        return (9)
    else:
        return None

def get_gabriel_vuln(message):
    pattern = re.compile(r'Vulnerabilità: (.+)')
    #match = pattern.search(message['message'])
    match = pattern.search(message)
    return match.group(1).strip()

def get_gabriel_version(message):
    pattern = re.compile(r'Versione: (.+)')
    match = pattern.search(message)
    return match.group(1).strip()

def gabriel_cves():
    # gabrielnews.ChannelMessages() # Assicurati di chiamare questa funzione solo se necessario
    cves = []
    with open('gabriel_messages.json', "r") as file:
        # Carica il contenuto del file JSON in un dizionario
        messages = json.load(file)
    
    for message in messages:
        if 'message' in message:
            cve = {}
            message_content = message['message']  # Faccio qui la conversione
            cve['Vendor'] = get_gabriel_vendor(message_content)
            cve['Prodotto'] = get_gabriel_prodotto(message_content)
            cve['Version'] = get_gabriel_version(message_content)
            cve['Cvss'] = get_gabriel_cvss(message_content)
            cve['Description'] = get_gabriel_vuln(message_content)
            cves.append(cve)
        else:
            # Gestisci il caso in cui la chiave 'message' non esista
            # print(f"Chiave 'message' non trovata nel messaggio: {message}")
            pass

    return cves

def get_cves():
    cves = []
    gabrielnews.ChannelMessages()
    cves = cves + (gabriel_cves()) # Cambiato con gabriel_cves
    return cves

if __name__ == '__main__':
    get_cves()