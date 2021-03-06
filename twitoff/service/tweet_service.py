#!/usr/bin/env python3

"""
    Service for dealing with the `tweet` table in the database.
"""

import pickle
import logging
import os
import re

#import basilica
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from decouple import config
import tweepy
from sqlalchemy import func
import pandas as pd

from twitoff import DB
from twitoff.models.User import User
from twitoff.models.Tweet import Tweet
from twitoff import REDIS


LOG = logging.getLogger("twitoff")

class TweetService:
    """
        Service for dealing with the `tweet` table in the database.
    """
    def __init__(self):
        pass

    def getTweetsByUserId(self, user_id):
        """
            Retrieve tweets of the given user. This method deals with
            tweets stored locally and does not call the twitter API.

            @type username: int
            @rtype: List[Tweet]
        """
        LOG.info(f"Querying database for tweets from user with id {user_id}")
        res = Tweet.query.filter(Tweet.user_id == user_id).all()
        LOG.info("Success!")
        return res

    def getAllTweetsAsDF(self):
        res = Tweet.query.all()
        df = pd.DataFrame([[t.text, t.user_id] for t in res])
        return df

    def addTweets(self, tweets):
        """
            Adds the given tweets to the database

            @type tweets: List[tweepy.models.Status]
        """
        assert all(isinstance(tweet, tweepy.models.Status) for tweet in tweets)
        
        LOG.info("Adding tweets to database")

        if len(tweets) == 0:
            LOG.info("No tweets found!")
            return

        first_tweet = tweets[0]
        user = User.query.get(first_tweet.user.id)
        LOG.info(f"First tweet: {first_tweet.full_text}")

        # invalidate redis cache for the user
        keys = [
            key for key in REDIS.keys()
            if user.username in str(key)
        ]
        LOG.info(f"Found {len(keys)} cached models for the user, invalidating them")
        for key in keys:
            REDIS.delete(key)

        twitoff_tweets = [
            Tweet(
                id=tweet.id,
                user_id=tweet.user.id,
                text=tweet.full_text[:500],
                date=tweet.created_at,
            ) for tweet in tweets
            if not Tweet.query.get(tweet.id)
        ]

        DB.session.add_all(twitoff_tweets)
        DB.session.commit()

        LOG.info("Success!")
