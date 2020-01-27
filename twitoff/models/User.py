#!/usr/bin/env python3

from twitoff import DB

class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(20), nullable=False)