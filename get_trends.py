import tweepy
import re
import sys
from hidden import *
from pprint import pprint
from iso3166 import countries


def getcities_forcountry(c_code):
    """ Receives a string that is a ISO country code and returns a dict that
        is a mapping of 'city name' : 'Where on earth Yahoo ID' for that country
    """
    jtrendlst = api.trends_available()
    city_woeid = dict()
    # print(jtrendlst)
    for loc in jtrendlst:
        if loc['countryCode'] == c_code and loc['parentid'] != 1:
            k, v = loc['name'], loc['woeid']
            city_woeid[k] = v
    return city_woeid


def gettrends_forcity(ci_name, ci_woeid):
    """ Receives a the city name and its WOEID and prints out the top 5
        trends for that city
    """
    try:
        jobjcity = api.trends_place(ci_woeid)
    except Exception as e:
        print(e)
        print(
            f"No trends are available for City: '{ci_name}' with WOEID ID '{ci_woeid}'\n")
    else:
        trends = jobjcity[0]['trends']
        for i, trend in enumerate(trends[:5], 1):
            print(f"{i}. {trend['name']:<40} {trend['url']}")


def titlecase(s):
    """ Receives a string that is the user's city input and returns the city name
        that is title()'ed'.
    """
    if s.count('-') > 1:
        return re.sub(r"[A-Za-z]+(-[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)
    elif s.count(' de ') > 0:
        return re.sub(r"[A-Za-zñáéíóú]+( [A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)
    else:
        return s.title()


# My API credentials are in "hidden" module
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

print("""   Enter ISO COUNTRY codes like
    AU / AUS for Australia
    DE / DEU for Germany
    """)
user_country = input("Country code: ")

try:
    c_code = countries.get(user_country).alpha2
    c_name = countries.get(user_country).name
except KeyError:
    wikiurl = "https://en.wikipedia.org/wiki/ISO_3166-1"
    sys.exit(
        f"'{user_country}' is not a valid Country code. For ISO codes refer {wikiurl}")

dloc = getcities_forcountry(c_code)

if len(dloc) < 1:
    print(f"No locations found for Country {c_code}-{c_name}")
else:
    print(f"Trends are available for the following cities in {c_name}")
    pprint(list(dloc.keys()), indent=4, compact=True)
    while True:
        print("To Exit hit 'Enter' OR")
        user_city = input(f"Pick a city in {c_code}: ")
        if len(user_city) < 1:
            break
        ci_name = titlecase(user_city)
        ci_woeid = dloc.get(ci_name)
        gettrends_forcity(ci_name, ci_woeid)
