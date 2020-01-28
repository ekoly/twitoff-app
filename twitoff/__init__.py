#!/usr/bin/env python3

from twitoff.app import make_app

APP, DB = make_app()

from twitoff import Routes
from twitoff.service.UtilService import UtilService

UTIL = UtilService()
