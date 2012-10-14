#!/usr/bin/env python
#inspired by Kay Zhu http://stackoverflow.com/users/853611/kay-zhu

import re
import requests
from bs4 import BeautifulSoup as bs
from linkstorage import Db
db = Db()


def get_urls_from_response(r):
    soup = bs(r.text)
    urls = [link.get('href') for link in soup.find_all('a')]
    real_urls = [url for url in urls if not url == '#']
    return real_urls


def print_url(args):
    print args['url']

def categorize(url):
    match = re.search('://(.+?)/', url)
    if match:
        host_name = match.group(1)
    else:
        return False
    host_name_components = host_name.split('.')
    if host_name_components[0] == 'www':
        match = re.search('://.+?/(.+?)/', url)
        if match:
            directory = match.group(1)
            return '{0}/{1}'.format(host_name_components[-2], directory)
        else:
            return host_name_components[-2]
    else:
        return '{0}/{1}'.format(host_name_components[-2], host_name_components[-3])

depth = 0
def recursive_urls(urls, db):
    """
    Given a list of starting urls, recursively finds all descendant urls
    recursively
    """
    global depth
    depth = depth + 1
    print('Depth = {0}'.format(depth))
    if depth > 2:
        return
    if len(urls) == 0:
        return
    responses = []
    for url in urls:
        if not url:
            continue
        try:
            rs = requests.get(url, hooks=dict(args=print_url))
        except (ValueError, requests.exceptions.ConnectionError):
            continue
        if rs.status_code == 200:
            responses.append(rs)
            path = categorize(rs.url)
            if path:
                db.store(rs.url, 'autogenerated', path)
    url_lists = [get_urls_from_response(response) for response in responses]
    urls = sum(url_lists, [])  # flatten list of lists into a list
    recursive_urls(urls, db)

if __name__ == "__main__":
    try:
        recursive_urls(["http://www.onet.pl/"], db)
    except KeyboardInterrupt:
        db.dump()
