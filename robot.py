import ftx
import requests
import config
import math
import datetime

api_endpoint_step = "https://ftx.com/api/markets/STEP-PERP"

client = ftx.FtxClient(api_key=config.API_KEY, api_secret=config.API_SECRET)

order_id_bid = 0
empty_bid = False
current_price_bid = 0


def my_round(var, size):
    result = ((var * 100000) // (size * 100000)) * size
    if size >= 1:
        return math.floor(result)
    else:
        return math.floor(result * 100000) / 100000


def process(json_data, count):
    global client
    global current_price_bid
    global current_price_ask
    global order_id_bid
    global order_id_ask
    global empty_bid
    global empty_ask

    vol_bid = 10000

    json_data_step = requests.get(api_endpoint_step).json()
    best_bid = json_data_step['result']['bid']
    min_price_bid = 0.97*best_bid
    max_price_bid = 0.98*best_bid

    print(str(count) + ') ' + str(datetime.datetime.now()))
    print('    min =', my_round(min_price_bid, 0.0005), 'cur =', current_price_bid, 'max =', my_round(max_price_bid, 0.0005));


    if (not empty_bid) and (count == 1):
        client.cancel_order(order_id_bid)
        empty_bid = True
    elif (current_price_bid < min_price_bid) or (current_price_bid > max_price_bid):
        if empty_bid:
            current_price_bid = my_round(best_bid*0.975, 0.0005)
            result = client.place_order('STEP-PERP', 'buy', current_price_bid, vol_bid)
            order_id_bid = result['id']
            print('Place order ', order_id_bid)
            empty_bid = False
        else:
            client.cancel_order(order_id_bid)
            print('Order cancelling')
            empty_bid = True
    else:
        print('    Order ' + str(order_id_bid))

def main():

    count = 0

    global current_price_bid
    global client
    global order_id_bid
    global empty_bid

    current_price_bid = 0.1
    result = client.place_order('STEP-PERP', 'buy', current_price_bid, 1)
    order_id_bid = result['id']

    empty_bid = False
    while 1:
        count += 1
        json_data = ''
        process(json_data, count)


if __name__ == '__main__':
    main()
