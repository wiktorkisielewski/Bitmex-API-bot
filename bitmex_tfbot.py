from bitmex import bitmex
import random
import json
import time
import requests

client = bitmex(
    test=True,
    api_key='1_Yp2iykWN3tXXD8Bo-mJaHD',
    api_secret='pNGVevk6MKPGoBtfP8uNaaEFM9z5d8zDj9emEm_syeq0ny2A'
)

def trade_details():
    global size
    global stop_loss
    global take_profit
    global leverage

    response = requests.get("https://www.bitmex.com/api/v1/orderBook/L2?symbol=xbt&depth=1").json()
    xbt_ask = response[0]['price']
    pre_size = client.User.User_getMargin().result()

    leverage = 25
    size = round((1/10 * (pre_size[0]['marginBalance']) * xbt_ask * 1/100000000) * leverage)
    stop_loss = round(xbt_ask / leverage * 3/100)
    take_profit = round(xbt_ask / leverage * 9/100)
    #print(size, stop_loss, take_profit)

    time.sleep(1)


def long_or_short():
    direction = random.choice([True, False])
    global position_d
    if direction == True:
        position_d = 'Buy'
    else:
        position_d = 'Sell'


def place_order(position_d, leverage, size, stop_loss, take_profit):
    response = client.Order.Order_new(
        symbol='XBTUSD',
        orderQty=size,
        ordType='Market',
        side=position_d).result()
    list = client.Position.Position_get(filter=json.dumps({'symbol': 'XBTUSD'})).result()
    global position_op
    position_op = round(list[0][0]['avgEntryPrice'])
    print(position_op)
    if position_d == 'Buy':
        response = client.Order.Order_new(
            symbol='XBTUSD',
            ordType='Stop',
            side='Sell',
            orderQty=size,
            stopPx=position_op - stop_loss
        ).result()
        response = client.Order.Order_new(
            symbol='XBTUSD',
            orderQty=size,
            side='Sell',
            ordType='Limit',
            price=(position_op + take_profit)
        ).result()
    else:
        response = client.Order.Order_new(
            symbol='XBTUSD',
            ordType='Stop',
            side='Buy',
            orderQty=size,
            stopPx=position_op + stop_loss

        ).result()
        response = client.Order.Order_new(
            symbol='XBTUSD',
            orderQty=size,
            side='Buy',
            ordType='Limit',
            price=(position_op - take_profit)
        ).result()

    response = client.Position.Position_updateLeverage(
        symbol='XBTUSD',
        leverage=leverage
    ).result()


def main_loop(size):
    check_pos = client.Position.Position_get(filter=json.dumps({'isOpen': 'True'})).result()
    check_shorts = client.Position.Position_get(filter=json.dumps({'currentQty': (size)})).result()
    check_longs = client.Position.Position_get(filter=json.dumps({'currentQty': (size)})).result()

    if (len(check_shorts[0]) == 0) and (len(check_longs[0]) == 0) and (len(check_pos[0]) == 1):
      client.Order.Order_cancelAll().result()
      time.sleep(5)
      long_or_short()
      place_order(position_d, leverage, size, stop_loss, take_profit)
    elif ((len(check_pos[0]) == 0) and len(check_longs[0]) == 0) and ((len(check_pos[0]) == 0) and len(check_shorts[0]) == 0):
      client.Order.Order_closePosition(symbol='XBTUSD').result()

    time.sleep(5)


while True:
    trade_details()
    main_loop(size)