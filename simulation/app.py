import sys
import urllib
import logging
from requests import Request

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='app.log',
                    filemode='a')


def ads_request(method, url, headers, data):
    req = Request(method, url, headers=headers, data=data)
    prepped = req.prepare()
    return ''


def show_banner_pic_request(url):
    pass


def ads_link_request(url):
    pass


def run():
    pass


if __name__ == '__main__':
    pass
