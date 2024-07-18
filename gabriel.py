import db
import webex
import private
import alerts
import time
import random

def risk_calc(asset, cve):
    '''
    From asset and cve, based on the cve's CVSS score and on the asset's value 
    in the client's system, calculates a risk score from 0 to 10
    '''
    return random.random(0,10)

def main():
    cmdb = db.CMDB()
    while True:
        cves = alerts.get_cves()
        for cve in cves:
            vuln_assets = cmdb.fetchAsset(cve["Vendor"], cve["Version"]) 
            # FetchAsset returns the list of vulnerable assets, each of which is a dict with vuln, client_id, asset_id
            if vuln_assets != None:
                for asset in vuln_assets:
                    risk = risk_calc(asset, cve) #TO DO
                    if risk > 7:
                        ops = webex.choose_ops()
                        webex.high_risk(ops, asset.vuln, asset.client, asset.id, cve.cvss, risk)
                    else:
                        webex.low_risk(asset.vuln, asset.client, asset.id, cve.cvss, risk)
        siem_events = cmdb.fetchEventsFromSIEM("http://siem.example.com/api/events", "API_KEY_HERE")
        if siem_events:
            cmdb.processSIEMEvents(siem_events)
        time.sleep(30)

if __name__ == "__main__":
    main()