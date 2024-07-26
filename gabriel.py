#import db
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
    #cmdb = db.CMDB()
    #while True:
        cves = alerts.get_cves()
        for cve in cves:
            try:
                vuln_assets = cve["Vendor"]
            except:
                vuln_assets = 1 
            # FetchAsset returns the list of vulnerable assets, each of which is a dict with vuln, client_id, asset_id
            if vuln_assets == None:
                pass
            elif vuln_assets == 1:
                if cve.get('Cvss') > 6.5:
                    webex.high_risk(cve, None)
                else:
                    webex.low_risk(cve, None)
            else:
                for asset in vuln_assets:
                    risk = risk_calc(asset, cve) #TO DO
                    if risk > 6.5:
                        webex.high_risk(cve, asset)
                    else:
                        webex.low_risk(cve, asset)
        
        """siem_events = cmdb.fetchEventsFromSIEM("http://siem.example.com/api/events", "API_KEY_HERE")
        if siem_events:
            cmdb.processSIEMEvents(siem_events)
        time.sleep(30)"""

if __name__ == "__main__":
    main()