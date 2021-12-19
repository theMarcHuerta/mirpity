from django.shortcuts import render
import requests
import sys
from subprocess import run,PIPE

import tweepy
import time
import pandas as pd
import sys

def button(request):
    return render(request, 'home.html')

def output(request):
    data=requests.get("https://reqres.in/api/users")
    print(data.text)
    data=data.text
    return render(request, 'home.html', {'data':data})

def external(request):
    inp = request.POST.get('param')

    bearer_token="AAAAAAAAAAAAAAAAAAAAAOLPWwEAAAAAiZGe1iL8ZXtfkhy8WR%2BL7DXafdM%3DL4smFywUxepOzFj3OuVbJXoerMIjHtluhlImwK6Nko2bwxqJ3Y"

    client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

    user_2_lookup = inp

    user_id_main = []
    user_id_main.append(client.get_user(id=None, username=user_2_lookup, user_auth=False, expansions=None, tweet_fields=None, user_fields=None))
    id_string = str(user_id_main[0].data['id'])


    username_list = []
    total_get_user_reqs = 0
    total_get_tweet_reqs = 0
    for mention in tweepy.Paginator(client.get_users_mentions,
                                    id = id_string,
                                    expansions = 'author_id',
                                    user_fields = 'username',
                                    start_time = '2021-01-01T00:00:00Z',
                                    end_time = '2021-12-17T04:00:00Z',
                                    max_results = 5):
        
        if ((mention.meta['result_count'])==0):
            break
        templist = mention.includes['users']
        user_num = len(templist)
        if (user_num == 5):
            for usernum in mention.includes['users']:
                username_list.append(usernum.username)           
        if (user_num == 4):
            if (total_get_tweet_reqs < 50):
                tweet_ids = []
                for tweetid in mention.data:
                    tweet_ids.append(tweetid.id)
                for tweetid in tweet_ids:
                    total_get_tweet_reqs += 1
                    dub = client.get_tweet(id = tweetid, user_auth=False, expansions = 'author_id', tweet_fields=None, user_fields = 'username')
                    wub = dub.includes['users']
                    username_list.append(wub[0].username)
            else:
                for usernum in mention.includes['users']:
                    username_list.append(usernum.username)        
        if (user_num == 3):
            for usernum in mention.includes['users']:
                for i in range(2):
                    username_list.append(usernum.username)
        if (user_num == 2):
            for usernum in mention.includes['users']:
                for i in range(2):
                    username_list.append(usernum.username)
        if (user_num == 1):
            for usernum in mention.includes['users']:
                for i in range(5):
                    username_list.append(usernum.username)
    

    user_dict = {}
    for user in username_list:
        if user not in user_dict:
            user_dict[user] = 0
        user_dict[user] += 1

    tupled_names = [(k, v) for k, v in user_dict.items()]
    top_folk = sorted(tupled_names, key = lambda x: x[1], reverse=True)
    top_folk[:10]

    out_string = "@" + user_2_lookup + " these are your top 10 people who've replied to your tweets the most in 2021!<br><br>"
    for i in range(10):
        out_string = out_string + "@" + str(top_folk[i][0]) + " is ranked " + str(i+1) + " amongst people who've replied to your tweets this year.<br><br>They replied to your tweets " + str(top_folk[i][1]) + " times<br><br><br><br>"

    return render(request, 'home.html', {'data1':out_string})
