#!/usr/bin/env python

import re
import os
from random import sample
from string import digits, ascii_letters

import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

alnum = re.compile('[\W]+')
dot = os.path.dirname(__file__)
NAMESPACE_WIDTH = 6
TAG_SEPARATOR = r'/'

def short_id():
    return ''.join(sample(digits + ascii_letters, NAMESPACE_WIDTH))


class Db(object):
    def __init__(self):
        self.storage = {}

    def store(self, link, tags_string):
        tags = [alnum.sub('', tag) for tag in tags_string.split()]
        tags_string = TAG_SEPARATOR.join(tags)
        if self.storage.has_key(tags_string):
            self.storage[tags_string].add(link)
        else:
            self.storage[tags_string] = set()
            self.storage[tags_string].add(link)
        
    def retrieve(self, tags_string):
        return self.storage[tags_string]


db = Db()


class Root(object):
    @cherrypy.expose
    def default(self, *args):
        tmpl = lookup.get_template("index.html")
        if not args:
            return tmpl.render(title="TITLE", body="<p>BODY</p>")
        else:
            return tmpl.render(title="TITLE", body=db.retrieve(args))


class Post(object):
    @cherrypy.expose
    def index(self):
        tmpl = lookup.get_template("post.html")
        return tmpl.render(title="TITLE")

    @cherrypy.expose
    def post(self, link='', title='', tags_string=''):
        if link:
            db.store(link, title, tags_string)


cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8888,
                      })

root = Root()
root.post = Post()
cherrypy.quickstart(root)

