import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import urllib.request
import pickle
import os.path

"""
Quick utility for downloading magenta_data

"""

base = "http://download.magenta.tensorflow.org/"
key_file = "magenta_keys"


def get_keys():
    if not os.path.isfile(key_file + '.pkl'):
        print("Downloading keys from magenta")
        page = urlopen(base).read()
        soup = bs(page)
        items = soup.find_all("key")
        data = [item.text for item in items]
        print(data)
        with open(key_file + '.pkl', 'wb') as f:
            pickle.dump(data, f)
    else:
        print("using previously found keys")
        data = pickle.load(open(key_file + '.pkl', "rb"))
    return data


def download(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return data


def magenta_fetch(target):
    url = base + target
    make_directory(target)
    print("Fetching {}".format(target))
    urllib.request.urlretrieve(url, filename=target)


def make_directory(target):
    directory, file = os.path.split(target)
    if not os.path.isdir(directory):
        print("making directory {}".format(directory))
        os.mkdir(directory)


def get_all_magenta():
    """
    grabs all the data
    :return:
    """
    keys = get_keys()
    for key in keys:
        magenta_fetch(key)


def get_by_file(filename):
    keys = get_keys()
    for target in keys:
        if filename in target:
            magenta_fetch(target)

