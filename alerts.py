'''
Prende tutti gli alerts da tutte le fonti, dalla cartella Alerts e contiene le funzioni per normalizzarli e fornirli a gabriel.py 
'''
import json
import re
import private
from Alerts import csirt

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

def get_cves():
    cves = []
    cves = cves + (csirt_cves())
    return cves

if __name__ == '__main__':
    get_cves()