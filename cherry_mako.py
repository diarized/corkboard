#!/usr/bin/env python

import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

from helpers import tags_to_path
from linkstorage import Db, FileSystem, Dir, Link
#db = Db()
fs = FileSystem()

from crawler import recursive_urls

class Root(object):
    def __init__(self):
        self.log = cherrypy.log

    @cherrypy.expose
    def default(self, *args):
        self.log.error("default() invoked.")
        tmpl = lookup.get_template("index.html")
        if not args:
            return tmpl.render(title="TITLE", body=fs.root.files)
        else:
            # args is a tuple
            path = '/'.join(args)
            dir = fs.get(path)
            return tmpl.render(title="TITLE", body=dir.files)


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
recursive_urls(["http://stackoverflow.com/questions/tagged/python"], fs)
root = Root()
cherrypy.quickstart(root)

