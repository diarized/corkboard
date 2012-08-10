#!/usr/bin/env python

import os
from random import sample
from string import digits, ascii_letters

import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

from helpers import sp2sl
from linkstorage import Db
db = Db()

NAMESPACE_WIDTH = 6

def short_id():
    return ''.join(sample(digits + ascii_letters, NAMESPACE_WIDTH))

class Root(object):
    @cherrypy.expose
    def default(self, *args):
        tmpl = lookup.get_template("index.html")
        if not args:
            return tmpl.render(title="TITLE", body="<p>BODY</p>")
        else:
            return tmpl.render(title="TITLE", body=db.retrieve(args))

    @cherrypy.expose
    def post(self, link='', title='', tags_string=''):
        tags_string = sp2sl(tags_string)
        if link:
            db.store(link, title, tags_string)
            raise cherrypy.InternalRedirect(tags_string)
            #tmpl = lookup.get_template("index.html")
            #links = db.retrieve(tags_string)
            #all_links = ''
            #for link in links:
            #    all_links = all_links + '<p>' + link + '</p>'
            #return tmpl.render(title="TITLE", body=all_links)
        else:
            tmpl = lookup.get_template("post.html")
            return tmpl.render(title="TITLE")


cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8888,
                      })

root = Root()
cherrypy.quickstart(root)

