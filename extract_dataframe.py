import json
import pandas as pd
from textblob import TextBlob

def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list


    # an example function
    # def find_statuses_count(self)->list:
    #     statuses_count 
        
    def find_full_text(self)->list:
        text = [item['text'] for item in self.tweets_list]
        return text;
       
    
    def find_sentiments(self, text)->list:
        polarity, subjectivity = [], []
        for tweet in text:
            blob = TextBlob(tweet)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)
        return polarity, subjectivity

    def find_created_time(self)->list:
       
        created_at = [item['created_at'] for item in self.tweets_list]
        return created_at
    def find_source(self)->list:
        source = [item['source'] for item in self.tweets_list]

        return source

    def find_screen_name(self)->list:
        screen_name = [item['user']['screen_name']
                       if 'user' in item else '' for item in self.tweets_list]
        return screen_name

    def find_followers_count(self)->list:
        followers_count = [item['user']['followers_count']
                           if 'user' in item else '' for item in self.tweets_list]
        return followers_count

    def find_friends_count(self)->list:
        friends_count = [item['user']['followers_count']
                         if 'user' in item else '' for item in self.tweets_list]
        return friends_count

    def is_sensitive(self)->list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = ' '

        return is_sensitive

    def find_favourite_count(self)->list:
        favorite_count = [item['retweeted_status']['favorite_count']
                          if 'retweeted_status' in item.keys() else 0 for item in self.tweets_list]

        return favorite_count
    
    def find_retweet_count(self) -> list:
        """Find retweet count of each tweet.
        """
        retweet_count = [item['retweeted_status']['retweet_count']
                         if 'retweeted_status' in item.keys() else 0 for item in self.tweets_list]
        return retweet_count

    def find_hashtags(self) -> list:
        """Find hashtags of each tweet.
        """
        hashtags = [item['entities']['hashtags'] if 'entities' in item.keys(
        ) else '' for item in self.tweets_list]
        return hashtags

    def find_mentions(self) -> list:
        """Find mentions of each tweet.
        """
        mentions = [item['entities']['user_mentions']
                    if 'entities' in item.keys(
        ) else '' for item in self.tweets_list]
        return mentions

    def find_location(self)->list:
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''
        
        return location

    def find_lang(self) -> list:
        """Find lang of tweets.
        """
        lang = [item['lang'] for item in self.tweets_list]

        return lang
    
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("./data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above

    