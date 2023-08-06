from __future__ import annotations

import dataclasses
import importlib.metadata
import json
import time

import bs4
import requests
import selenium.webdriver

__version__ = importlib.metadata.version("aoj-api")
