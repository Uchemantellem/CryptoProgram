import requests
import json
import datetime
import notify2
from secret_data import *


CACHE_FNAME = 'coinbase.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_" + "_".join(res)

# Cache
def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    # check cache
    if unique_ident in CACHE_DICTION:
        print("Fetching cached data...")
        return CACHE_DICTION[unique_ident]

    # request and store in cache
    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params = params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def get_market_price(coin):
    url = "https://api.coinbase.com/v2/prices/" + coin + "-USD/spot"
    params = {}
    data = requests.get(url, params = params)
    data = json.loads(data.text)
    currenttime = datetime.datetime.now()
    info = {}
    info[data["data"]["amount"]] = currenttime
    print("$" + data["data"]["amount"])
    return info



# process for notification for monitor
# ICON_PATH = "C:\Users\uched\Desktop\randomscreenies\questions"
# initialise the d-bus connection 
# notify2.init("Coin Notifier") 
  
# # create Notification object 
# n = notify2.Notification(None, icon = ICON_PATH) 
  
# # set urgency level 
# n.set_urgency(notify2.URGENCY_NORMAL) 
  
# # set timeout for a notification 
# n.set_timeout(10000) 

def monitor(coin, target):
    price_time = get_market_price(coin)
    print(price_time)
    while True:
        for k, v in price_time.items():
            if v < datetime.datetime.now() - datetime.timedelta(seconds=15) :
                price_time = get_market_price(coin)
            if float(k) >= float(target):
                # send text - further implementation
                # update notification data for Notification object 
                # n.update(k, v) 
              
                # # show notification on screen 
                # n.show() 
              
                # # short delay between notifications 
                # time.sleep(15) 
                  
                print("buy now!")
                # exit()
# help! lol
def load_help_text():
    with open('help.txt') as f:
        return f.read()

info = input("What information are you looking for? For help type <help>: \n Prices, Monitor\n")

if info == "prices":
    info = input("What coin? All caps please :)\n")
    get_market_price(info)
if info == "monitor":
    coin = input("What coin? \n")
    target = input("Target price? \n")
    monitor(coin, target)
if info == "help":
    help = load_help_text()
    print(help)

