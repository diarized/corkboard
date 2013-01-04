#!/usr/bin/env python

import cherrypy
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])

from linkstorage import FileSystem, Link, Path, DEBUG
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
        if DEBUG:
            self.log.error("default() invoked.")
        tmpl = lookup.get_template("index.html")
        if not args:
            return tmpl.render(title=fs.root.name, parent=fs.root.name, files=fs.root.files)
        else:
            # args is a tuple
            path = '/'.join(args)
            dir_at_path = fs.get(path)
            return tmpl.render(
                    title=dir_at_path.name,
                    parent=dir_at_path.parent.name,
                    files=dir_at_path.files)

    @cherrypy.expose
    def post(self, url='', title='', tags=''):
        """
        http://hostname/post, NOT http://hostname/post.html
        """
        if not url:
            self.log.error("No link")
            tmpl = lookup.get_template("post.html")
            return tmpl.render(title="TITLE")
        path = Path(tags).path
        if DEBUG:
            self.log.error(">>> URL " + url + "<<<")
            self.log.error(">>> PATH " + path + "<<<")
        link = Link(url, title)
        fs.add(path, link)
        if DEBUG:
            self.log.error("Link {0} stored in {1}".format(link, path))
        raise cherrypy.InternalRedirect("/{0}".format(path))

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8888
                        })
#recursive_urls(["http://stackoverflow.com/questions/tagged/python"], fs)
recursive_urls(["http://www.bankier.pl/"], fs)
root = Root()
cherrypy.quickstart(root)

