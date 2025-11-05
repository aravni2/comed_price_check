import pandas as pd
import numpy as np
import requests
import datetime as dt
import pygame
import time

def get_price (interval = 0):
    # retrieve response
    resp_5min = requests.get('https://hourlypricing.comed.com/api?type=5minutefeed')
    resp_5min.json()
    
    # convert time
    time_5m = int(resp_5min.json()[interval]['millisUTC']) 
    time_cst = dt.datetime.fromtimestamp(time_5m/1000.0).strftime('%Y-%m-%d %I:%M')
    
    
    cur_price_5m = resp_5min.json()[interval]['price']
    price_diff = float(resp_5min.json()[interval]['price']) - float(resp_5min.json()[interval+1]['price'])

    return (time_cst,cur_price_5m,price_diff)



# initiate pygame
pygame.init()
channel = pygame.mixer.Channel(0)

s_ding = pygame.mixer.Sound('airplane_ding.wav')
d_ding = pygame.mixer.Sound('airplane_ding_ding.wav')
exit = pygame.mixer.Sound('exit.wav')

while True:
    try:
        prev_time, prev_price_5m, prev_price_diff = get_price(1)
        time_cst_5m, cur_price_5m, price_diff = get_price()

        print(f'Current Interval: {time_cst_5m}')
        print(f'\tcurrent price: {cur_price_5m}')
        print(f'\tprevious price: {prev_price_5m}')
        print(f'\tdiff: {price_diff}')
        print(f'\tprevious price: {prev_price_5m}, previous diff: {prev_price_diff:.4f}')
        cur_price_5m = float(cur_price_5m)
        if(cur_price_5m < 3):
            channel.play(d_ding,0)
        elif(cur_price_5m < 5):
            channel.play(s_ding,0)
        
        elif(cur_price_5m >=10):
            channel.play(exit,1)
    except Exception as e:
        print(f"Request failed: {e}")
    
    time.sleep(120)  # Wait for 5mins
