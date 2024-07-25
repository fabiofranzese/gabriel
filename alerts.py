'''
Prende tutti gli alerts da tutte le fonti, dalla cartella Alerts e contiene le funzioni per normalizzarli e fornirli a gabriel.py 
'''
import json
import re
import private
from Alerts import csirt

def get_csirt_risk(message):
    pattern = re.compile(r'Rischio: (.+)')
    match = pattern.search(message['message'])
    emoji = match.group(1).strip()
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
    return match.group(1).strip()

def csirt_cves():
    csirt.ChannelMessages()
    cves = []
    with open('../Alerts/channel_messages.json', "r") as file:
        # Carica il contenuto del file JSON in un dizionario
        messages = json.load(file)
    for message in messages:
        cve = {}
        cve['Description'] = message['message'].split("\n")[0]
        cve['Risk'] = get_csirt_risk(message)
        cve['Resources'] = get_csirt_link(message)
        cves.append(cve)
        print(cve)
        print()

def get_cves():
    cves = []
    cves.append(csirt_cves())
    print(cves)
    return cves

if __name__ == '__main__':
    get_cves()