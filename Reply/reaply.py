#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, sys
import pandas as pd

def main(argv):
    print(argv[0])
    url = "https://api.reply.io/v1/campaigns?name=" + argv[0]

    payload = {}
    headers = {
      'x-api-key': 'QJt4ZhWZ7IEXPhPNbIDlHxGB'
    }
    
    response = requests.request("GET", url, headers=headers, data = payload)
    print(response.status_code)
    
    companyId = response.json()["id"]
    
    print(argv[1]+".csv")
    
    df = pd.read_csv(argv[1]+".csv")
    for index, row in df.iterrows():
        url = "https://api.reply.io/v1/actions/removepersonfromcampaignbyid"

        payload = "{\r\n\"campaignId\": " + str(companyId) + ",\r\n\"email\": \"" + str(row[0]) + "\"\r\n}"
        headers = {
          'Content-Type': 'application/json',
          'x-api-key': 'QJt4ZhWZ7IEXPhPNbIDlHxGB'
        }
        
        response = requests.request("POST", url, headers=headers, data = payload)
        
        print(response.status_code)
    
    
if __name__=="__main__":
    main(sys.argv[1:])