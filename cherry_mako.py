#!/usr/bin/env python

import cherrypy
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

from helpers import tags_to_path
from linkstorage import FileSystem, Link
fs = FileSystem()

from crawler import recursive_urls

class Root(object):
    """ Root CherryPy application object """
    def __init__(self):
        self.log = cherrypy.log

    @cherrypy.expose
    def default(self, *args):
        """
        processing of all GET requests
        (if not handled by functions exposed below)
        """
        self.log.error("default() invoked.")
        tmpl = lookup.get_template("index.html")
        if not args:
            return tmpl.render(title="TITLE", body=fs.root.files)
        else:
            # args is a tuple
            path = '/'.join(args)
            dir_at_path = fs.get(path)
            return tmpl.render(title="TITLE", body=dir_at_path.files)

    @cherrypy.expose
    def post(self, url='', title='', path=''):
        """
        http://hostname/post, NOT http://hostname/post.html
        """
        if not url:
            self.log.error("No link")
            tmpl = lookup.get_template("post.html")
            return tmpl.render(title="TITLE")

        if not path:
            path = '/uncategorized' 
        if not path.startswith('/'):
            path = '/' + path

        self.log.error(">>>" + url + "<<<")
        link = Link(url, title)
        fs.add(path, link)
        self.log.error("Link {0} stored in {1}".format(link, path))
        raise cherrypy.InternalRedirect("/{0}".format(path))
#        dir_at_path = fs.get(path)
#        tmpl = lookup.get_template("index.html")
#        return tmpl.render(title="TITLE", body=dir_at_path.files)


cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8888
                        })
recursive_urls(["http://stackoverflow.com/questions/tagged/python"], fs)
root = Root()
cherrypy.quickstart(root)

