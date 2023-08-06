import requests 

class HeliumApi(object):
    """docstring"""
 
    def __init__(self):
       pass

    def getTokenSupply(self):
    	r = requests.get('https://api.helium.io/v1/stats/token_supply')
    	return r.json()
    
    def getStats(self):	
    	r = requests.get('https://api.helium.io/v1/stats')
    	return r.json()

    def getBlockHeight(self):
    	r = requests.get('https://api.helium.io/v1/blocks/height')
    	return r.json()

    def getBlockStats(self):
    	r = requests.get('https://api.helium.io/v1/blocks/stats')
    	return r.json()

    def getBlockDescription(self):
    	r = requests.get('https://api.helium.io/v1/blocks')
    	return r.json()

    def getBlockTransactions(self,height):
    	r = requests.get(f'https://api.helium.io/v1/blocks/{height}/transactions')
    	return r.json()

    def getAccounts(self):
    	r = requests.get(f'https://api.helium.io/v1/accounts')
    	return r.json()

    def getRichestAccounts(self):
    	r = requests.get('https://api.helium.io/v1/accounts/rich')
    	return r.json()

    def getHotspotsByOwnerAddress(self,address):
    	r = requests.get(f'https://api.helium.io/v1/accounts/{address}/hotspots')
    	return r.json()

    def getActivitiesByAddress(self,address):
    	r = requests.get(f'https://api.helium.io/v1/accounts/{address}/roles')
    	return r.json()