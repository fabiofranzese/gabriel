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
    #while True:
    cmdb = db.CMDB()

    cves = alerts.get_cves()
    
    for cve in cves:
        
        
        vuln_assets = cmdb.fetchAsset(cve["Vendor"], cve["Version"])
            
        # FetchAsset returns the list of vulnerable assets, each of which is a dict with vuln, client_id, asset_id
        if vuln_assets == 0:
            pass
        elif vuln_assets == 1:
            if cve.get('Cvss') > 6.5:
                webex.high_risk(cve, None)
            else:
                webex.low_risk(cve, None)
        '''
        else:
            for asset in vuln_assets:
                if cve.get('Cvss') > 6.5: #Will have to implement it with risk_calc function:
                    webex.high_risk(cve, asset)
                    
                else:
                    webex.low_risk(cve, asset) 
                        
        '''

if __name__ == "__main__":
    main()