import requests
from datetime import date, datetime
from stats_page import get_inflation, osmo_neutron

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def million_converter(value):
    try:
        value = float(value) 
    except: 
        return value
    if value >= 1000000000:
        value = round(value/1000000000,2)
        value = str(value)+"B"

    elif value > 1000000: 
        value = round(value/1000000,2)
        value = str(value)+"M"
    
    elif value > 1000: 
        value = round(value/1000,2)
        value = str(value)+"K"
    return value


class Nolus:
    def __init__(self):
        self.url_dapp = 'https://etl-cl.nolus.network:8080/api'
        self.url_chain = 'https://nolus-api.lavenderfive.com:443'

    async def get_tvl(self):
        try:
            data = requests.get(self.url_dapp + '/total-value-locked')
            tvl = data.json()['total_value_locked']
            return (tvl)
        except Exception as e: 
            print ("Error getting TVL", e)
            return "Error"

    async def get_validators(self): 
        validators = 0
        try:
            data = requests.get(self.url_chain + '/cosmos/staking/v1beta1/validators')
            data = data.json()
            for i in range(0,len(data['validators'])): 
                if data['validators'][i]['status'] == 'BOND_STATUS_BONDED': 
                    validators += 1
        except Exception as e: 
            print ("Error getting validators",e)
            validators = "Error"
        return validators

    async def get_buybacks(self):
        try:
            data = requests.get (self.url_dapp + '/buyback-total')
            data = data.json()
            buybacks = (int(float(data['buyback_total'])))
        except Exception as e: 
            print ("Error getting buybacks", e)
            buybacks = "Error"
        return (buybacks)

    async def get_revenue(self): 
        try:
            data = requests.get(self.url_dapp + '/revenue')
            revenue = (data.json()['revenue'])
        except Exception as e: 
            print ("Error getting revenue", e)
            revenue = "Error"
        return revenue
    
    async def get_price(self): 
        try:
            data = requests.get('https://api-osmosis.imperator.co/tokens/v2/nls')
            price = data.json()[0]['price']
        except Exception as e: 
            try:
                print ("Error with getting price from Osmosis", e)
                data = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=nolus&vs_currencies=usd')
                price = data.json()['nolus']['usd']
            except Exception as e: 
                print ("Error getting price from both Osmosis and Coingecko!")
                print ("Error",e)
                price = "Error"
        return price

    async def get_community_pool(self)->float: 
        try:
            data = requests.get(self.url_chain + '/cosmos/distribution/v1beta1/community_pool')
            community_pool = float(data.json()['pool'][0]['amount'])/1000000
        except Exception as e: 
            print ("Error getting the communit pool's size", e)
            community_pool = "Error"
        return community_pool
    
    async def get_total_supply(self)->float:
        try:
            data = requests.get (self.url_chain + '/cosmos/bank/v1beta1/supply')
            all_tokens_on_chain = data.json()['supply'] #this shows the supply of every single token on the self blockchain
            for token in all_tokens_on_chain:
                if token['denom'] == 'unls':
                    total_supply = (round(int(token['amount'])/1000000,2))
                    return total_supply
        except Exception as e: 
            print ("Error getting the total supply", e)
            return "Error"
        
    async def get_circulating_supply(self)->float: 
        try:
            data = requests.get("https://supply.nolus.io/?type=circulating",headers=headers)
            circulating_supply = data.json()
        except Exception as e:
            print (e)
            print ("Error getting the circulating supply")
            circulating_supply = "Error"
        return circulating_supply 
            
    async def get_market_cap(self)->float: 
        try:
            market_cap = float(self.price) * float(self.circulating_supply) 
        except: 
            print ("Error calculating Market Cap!")
            market_cap = "Error"
        return (market_cap)
    

    async def get_bonded_tokens(self): 
        try:
            data = requests.get(self.url_chain + '/cosmos/staking/v1beta1/pool')
            response = float(data.json()['pool']['bonded_tokens'])/1000000
            return (response)
        except Exception as e: 
            print ("Error getting bonded tokens!", e)
            return "Error"
    
    async def get_bonded_ratio(self): 
        try:
            return round(float(self.bonded_tokens)/ float(self.total_supply) * 100,2)
        except Exception as e: 
            print ("Error getting bonded ratio", e)
            return "Error"


    async def get_total_tx(self): 
        try:
            data = requests.get(self.url_dapp + '/total-tx-value')
            total_tx = data.json()['total_tx_value']
            return total_tx
        except Exception as e: 
            print ("Error getting total txs", e)
            return "Error"

    async def get_message(self): 
        today = date.today().strftime("%B %d, %Y")
        messageToBeSent = ':calendar: **' + today + '** :calendar:\n'
        messageToBeSent = messageToBeSent + '**__Nolus Stats - Update/3 minutes__**\n\n'

        messageToBeSent = messageToBeSent + '```Market Stats```'
        messageToBeSent = messageToBeSent + ':dollar: `Price:` **$' + str(round(self.price,3)) 
        messageToBeSent = messageToBeSent + '**\n:moneybag: `Market Capitalization:` **$' + million_converter(self.market_cap)+'**'

        messageToBeSent = messageToBeSent + '\n'+'```Protocol Stats```'
        messageToBeSent = messageToBeSent +':lock: `Total Value Locked:` **$' + million_converter(self.tvl) + '**'
        messageToBeSent = messageToBeSent +'\n:gem: `Buybacks (in $NLS):` **' + million_converter(self.buybacks) + '**'
        messageToBeSent = messageToBeSent +'\n:money_with_wings: `Revenue:` **$' + million_converter(self.revenue) + "**"
        messageToBeSent = messageToBeSent +'\n:moneybag: `Total TX value:` **$' + million_converter(self.total_tx) + "**" 
        messageToBeSent = messageToBeSent +'\n<:ntrn:1231598255956295730> `axl.USDC apr (Neutron):` **' + (self.apr_ntrn) +" + " + (self.extra_apr)+ f"** ~ deposits : {self.deposit_check_ntrn}"
        messageToBeSent = messageToBeSent +'\n<:osmo:1231598304995971112> `axl.USDC apr (Osmosis):` **' + (self.apr_osmo) + " + " + (self.extra_apr) + f"** ~ deposits : {self.deposit_check_osmo}"

        messageToBeSent = messageToBeSent + '\n'+'```Network Stats```'
        messageToBeSent = messageToBeSent +':trophy: `Staking APR:` **' + (self.inflation) + '**'
        messageToBeSent = messageToBeSent +'\n🔐 `Total Bonded :` **' + million_converter(self.bonded_tokens) + '**'
        messageToBeSent = messageToBeSent +'\n:bar_chart: `Bonded Ratio:` **' + f'{self.bonded_ratio}%' + '**'
        messageToBeSent = messageToBeSent +'\n:unlock: `Unbonding Period:` **' + f'{self.bonding_period} days' + '**'
        messageToBeSent = messageToBeSent +'\n:technologist: `Max Validators:` **' + f'{self.validators}' + '**'



        messageToBeSent = messageToBeSent + '\n```Token Stats```'
        messageToBeSent = messageToBeSent +':briefcase: `Max Supply:` **' + million_converter(1000000000) +'**'
        messageToBeSent = messageToBeSent + '\n:left_luggage: `Total Supply:` **' + million_converter(self.total_supply) +'**'
        messageToBeSent = messageToBeSent +'\n:recycle: `Circulating Supply:` **' + million_converter(self.circulating_supply) + '**'
        messageToBeSent = messageToBeSent +'\n🌇 `Community Pool:` **$' + million_converter(self.community_pool) + '**'
        messageToBeSent = messageToBeSent + '\n\n' + f"*Last Update: {self.time_updated}*"
        return messageToBeSent
    

    async def update_values(self):
        self.tvl = await self.get_tvl()
        self.buybacks = await self.get_buybacks() 
        self.revenue = await self.get_revenue()
        self.price = await self.get_price()
        self.community_pool = await self.get_community_pool()
        self.total_supply = await self.get_total_supply()
        self.circulating_supply = await self.get_circulating_supply()
        self.market_cap = await self.get_market_cap()
        self.bonded_tokens = await self.get_bonded_tokens()
        self.total_tx = await self.get_total_tx()
        self.inflation = await get_inflation()
        self.apr_osmo, self.deposit_check_osmo, self.apr_ntrn, self.deposit_check_ntrn = await osmo_neutron()
        self.bonding_period = 21
        self.validators = await self.get_validators()
        self.bonded_ratio = await self.get_bonded_ratio()
        self.extra_apr = '12%'

        self.time_updated = datetime.now().strftime("%H:%M:%S")
        self.message = await self.get_message()
