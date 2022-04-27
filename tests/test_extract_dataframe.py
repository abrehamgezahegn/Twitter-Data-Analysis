import os
import sys
import unittest
import zipfile

import pandas as pd
from extract_dataframe import TweetDfExtractor, read_json

sys.path.append(os.path.abspath(os.path.join('../..')))


with zipfile.ZipFile("data/Economic_Twitter_Data.zip", "r") as zip_ref:
    zip_ref.extractall("data/")
_, tweet_list = read_json("data/Economic_Twitter_Data.json")

columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
           'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']


class TestTweetDfExtractor(unittest.TestCase):
    """A class for unit-testing function in the extract_dataframe.py file.
    Args:
        unittest.TestCase this allows the new class to inherit
        from the unittest module
    """

    def setUp(self) -> pd.DataFrame:
        """
        Returns:
            pd.DataFrame: DF from Economic_Twitter_data.json file.
        """
        self.df = TweetDfExtractor(tweet_list[:5])

    # def test_find_statuses_count(self):
    #     """Test find status count module."""
    #     self.assertEqual(self.df.find_statuses_count(), [40, 40, 40, 40, 40])

    def test_find_full_text(self):
        text = ['RT @nikitheblogger: Irre: Annalena Baerbock sagt, es bricht ihr das Herz, dass man nicht bedingungslos schwere Waffen liefert.\nMir bricht e…', 'RT @sagt_mit: Merkel schaffte es in 1 Jahr 1 Million "Flüchtlinge" durchzufüttern, jedoch nicht nach 16 Jahren 1 Million Rentner aus der Ar…',
                'RT @Kryptonoun: @WRi007 Pharma in Lebensmitteln, Trinkwasser, in der Luft oder in der Zahnpasta irgendwo muss ein Beruhigungsmittel bzw. Be…', 'RT @WRi007: Die #Deutschen sind ein braves Volk!. Mit #Spritpreisen von 2 Euro abgefunden. Mit #inflation abgefunden. Mit höheren #Abgaben…', 'RT @RolandTichy: Baerbock verkündet mal so nebenhin in Riga das Ende der Energieimporte aus Russland. Habeck rudert schon zurück, Scholz sc…']

        self.assertEqual(self.df.find_full_text(), text)

    def test_find_sentiments(self):
        self.assertEqual(self.df.find_sentiments(self.df.find_full_text()), ([
                         0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]))

        created_at = ['Fri Apr 22 22:20:18 +0000 2022', 'Fri Apr 22 22:19:16 +0000 2022',
                      'Fri Apr 22 22:17:28 +0000 2022', 'Fri Apr 22 22:17:20 +0000 2022', 'Fri Apr 22 22:13:15 +0000 2022']

        self.assertEqual(self.df.find_created_time(), created_at)

    def test_find_source(self):
        source = ['<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>',
                  '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>']

        self.assertEqual(self.df.find_source(), source)

    def test_find_screen_name(self):
        screen_name = ['McMc74078966', 'McMc74078966',
                       'McMc74078966', 'McMc74078966', 'McMc74078966']
        self.assertEqual(self.df.find_screen_name(), screen_name)

    def test_find_followers_count(self):
        f_count = [3, 3, 3, 3, 3]
        self.assertEqual(self.df.find_followers_count(), f_count)

    def test_find_friends_count(self):
        friends_count = [3, 3, 3, 3, 3]
        self.assertEqual(self.df.find_friends_count(), friends_count)

    def test_find_is_sensitive(self):
        self.assertEqual(self.df.is_sensitive(), [
                         '', '', '', '', ''])

    def test_find_favourite_count(self):
        self.assertEqual(self.df.find_favourite_count(),
                         [2356, 1985, 16, 1242, 1329])

    def test_find_retweet_count(self):
        self.assertEqual(self.df.find_retweet_count(), [355, 505, 4, 332, 386])

    def test_find_hashtags(self):
        hashtags = [[], [], [], [{'text': 'Deutschen', 'indices': [16, 26]}, {'text': 'Spritpreisen', 'indices': [
            54, 67]}, {'text': 'inflation', 'indices': [95, 105]}, {'text': 'Abgaben', 'indices': [130, 138]}], []]
        self.assertEqual(self.df.find_hashtags(), hashtags)

    # def test_find_mentions(self):
    #     self.assertEqual(self.df.find_mentions(), )

    def test_find_location(self):
        self.assertEqual(self.df.find_location(), ['', '', '', '', ''])


if __name__ == '__main__':
    unittest.main()