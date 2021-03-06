#!/usr/bin/env python3

from twitoff import DB

class User(DB.Model):
    """
        Database table for twitter users.
    """

    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(50), nullable=False)
    username = DB.Column(DB.String(50), nullable=False)
