#!/usr/bin/python3
"""This module makes a request to the reddit api"""
import requests


def count_words(subreddit, word_list, after='', tok={}):
    """
    recursively calls the reddit api to fetch all hot articles
    and counts how many times the keywords
    appear in those articles
    """
    headers = {
        'User-Agent': 'My User Agent 1.0',
    }
    try:
        if after is None:
            sorted_tok = sorted(tok.items(), key=lambda x: x[1], reverse=True)
            dict_sorted_tok = dict(sorted_tok)
            for key, value in dict_sorted_tok.items():
                if value != 0:
                    print('{}: {}'.format(key, value))
            return None
        if after == '':
            res = requests.get('https://www.reddit.com/r/'+subreddit
                               + '/hot.json', headers=headers,
                               allow_redirects=False)
            # Initializing the tok dictionary that holds the count
            word_list = sorted(word_list)
            for key in word_list:
                tok[key.lower()] = 0
        else:
            res = requests.get('https://www.reddit.com/r/'+subreddit
                               + '/hot.json?after={}'.format(after),
                               headers=headers, allow_redirects=False)
        subreddit_data = res.json()
    except Exception as e:
        return (None)
    if 'error' in subreddit_data.keys():
        return (None)
    details = subreddit_data['data']['children']
    tokens = []
    for detail in details:
        tokens = detail['data']['title'].split(' ')
        for token in tokens:
            token = token.lower()
            if token in word_list:
                tok['{}'.format(token)] = tok['{}'.format(token)] + 1
    after = subreddit_data['data']['after']
    return (count_words(subreddit, word_list, after, tok))
