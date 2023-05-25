#!/usr/bin/python3

import requests

def count_words(subreddit, word_list, after=None, count_dict=None):
if count_dict is None:
count_dict = {}headers = {"User-Agent": "Mozilla/5.0"}
url = f"https://www.reddit.com/r/{subreddit}/hot.json"
params = {"limit": 100, "after": after}

response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    posts = data["data"]["children"]
    
    for post in posts:
        title = post["data"]["title"].lower()
        for word in word_list:
            if word.lower() in title:
                if word.lower() in count_dict:
                    count_dict[word.lower()] += 1
                else:
                    count_dict[word.lower()] = 1
    
    after = data["data"]["after"]
    if after is not None:
        count_words(subreddit, word_list, after, count_dict)
    else:
        sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")
else:
    print("Error: Invalid subreddit or no posts match.")
    return

