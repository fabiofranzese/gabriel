import db
import webex
import private
import alerts
import time
import random
import webhook

def risk_calc(value, cvss):
    '''
    From asset and cve, based on the cve's CVSS score and on the asset's value 
    in the client's system, calculates a risk score from 0 to 10
    '''
    if value == -1:
        return cvss
    else:
        return (value + cvss) // 2

cmdb = db.CMDB()

def main():
    #while True:

    cves = alerts.get_cves()

    for cve in cves:
        vuln_assets = cmdb.fetchAsset(cve["Vendor"], cve["Version"], cve["Prodotto"])
        if not vuln_assets:
            pass
        else:
            for asset in vuln_assets: 
                risk = risk_calc(asset.get('Value', -1), cve.get('Cvss'))
                if risk >= 6:
                    webex.high_risk(cve, asset, risk)
                else:
                    webex.low_risk(cve, asset, risk) 

if __name__ == "__main__":
    main()
    webhook.app.run(debug=True)