# Copyright (c) 2008 Yahoo! Inc. All rights reserved.
# Licensed under the Yahoo! Search BOSS Terms of Use
# (http://info.yahoo.com/legal/us/yahoo/search/bosstos/bosstos-2317.html)

""" Functions for downloading REST API's and converting their responses into dictionaries """

__author__ = "Vik Singh (viksi@yahoo-inc.com)"

import urllib2
import urllib

import simplejson
import xml2dict

HEADERS = {"User-Agent": simplejson.load(open("config.json", "r"))["agent"]}

def download(url):
  try:
    r = urllib.urlopen(url).read()
    if all(map(lambda t: r.find(t) > 1, ["</head>", "</body>", "</html>"])):
      raise Error, "Why is this an html response?"
    return r
  except:
    req = urllib2.Request(url, None, HEADERS)
    return urllib2.urlopen(req).read()

def load_json(url):
  return simplejson.loads(download(url))

def load_xml(url):
  return xml2dict.fromstring(download(url))

def load(url):
  dl = download(url)
  try:
    return simplejson.loads(dl)
  except:
    return xml2dict.fromstring(dl)
