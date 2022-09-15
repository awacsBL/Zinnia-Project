from twitter import TwitterSearchScraper

'''
Used for custom twitter scraping, saved currently for future use
'''

tweets_list = []
f = open("test.jsonl", "a", encoding="utf-8")
for i, test in enumerate(TwitterSearchScraper("hi").get_items()):
    if i > 10:
        break
    f.write(test.json()+"\n")
f.close()
