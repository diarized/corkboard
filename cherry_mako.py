#!/usr/bin/env python

import os
from random import sample
from string import digits, ascii_letters

import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

from helpers import tags_to_path
from linkstorage import Db
db = Db()

NAMESPACE_WIDTH = 6 # number of combinations = (36+10)^6 = 9.5 billion 

def short_id():
    return ''.join(sample(digits + ascii_letters, NAMESPACE_WIDTH))

class Root(object):
    def __init__(self):
        self.log = cherrypy.log

    @cherrypy.expose
    def default(self, *args):
        self.log.error("default() invoked.")
        tmpl = lookup.get_template("index.html")
        if not args:
            return tmpl.render(title="TITLE", body="<p>BODY</p>")
        else:
            return tmpl.render(title="TITLE", body=db.retrieve('/'.join(args)))


    @cherrypy.expose
    def post(self, link='', title='', tags_string=''):
        """
        http://hostname/post, NOT http://hostname/post.html
        """
        if link:
            if tags_string:
                path = tags_to_path(tags_string)
            else:
                path = ''
            self.log.error(">>>" + link + "<<<")
            db.store(link, title, path)
            self.log.error("Link {0} stored in {1}".format(link, path))
            raise cherrypy.InternalRedirect("/{0}".format(path))
            tmpl = lookup.get_template("index.html")
            links_set = db.retrieve(path)
            p_links = ''
            for link in links_set:
                p_links = p_links + '<p>' + link + '</p>\n'
            return tmpl.render(title="TITLE", body=all_links)
        else:
            self.log.error("No link")
            tmpl = lookup.get_template("post.html")
            return tmpl.render(title="TITLE")


cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8888
                        })

root = Root()
cherrypy.quickstart(root)

