import tweepy
import time
import pandas as pd
import sys

bearer_token="AAAAAAAAAAAAAAAAAAAAAOLPWwEAAAAAiZGe1iL8ZXtfkhy8WR%2BL7DXafdM%3DL4smFywUxepOzFj3OuVbJXoerMIjHtluhlImwK6Nko2bwxqJ3Y"

client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

user_2_lookup = str(sys.argv[1])

user_id_main = []
user_id_main.append(client.get_user(id=None, username=user_2_lookup, user_auth=False, expansions=None, tweet_fields=None, user_fields=None))
id_string = str(user_id_main[0].data['id'])

mentions = []
for mention in tweepy.Paginator(client.get_users_mentions,
                                id = id_string,
                                expansions = 'author_id',
                                user_fields = 'username',
                                start_time = '2021-11-15T00:00:00Z',
                                end_time = '2021-12-15T00:00:00Z',
                                max_results = 30):
    mentions.append(mention)

usernames = []
for page in mentions:
    for user in page.includes['users']:
        usernames.append(user.data['username'])

user_dict = {}
for user in usernames:
    if user not in user_dict:
        user_dict[user] = 0
    user_dict[user] += 1

tupled_names = [(k, v) for k, v in user_dict.items()]
top_folk = sorted(tupled_names, key = lambda x: x[1], reverse=True)
top_folk[:10]

for i in range(10):
    print("@" + str(top_folk[i][0]), "is ranked", str(i+1) ,"amongst people who've replied to your tweets this year.<br><br>They replied to your tweets", str(top_folk[i][1]), "times<br><br><br><br>", end = '')
