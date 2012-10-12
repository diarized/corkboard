class Db(object):
    def __init__(self):
        self.storage = {}

    def store(self, link, title, path):
        if not self.storage.has_key(path):
            print('storage["{0}"] does not exist. Creating.'.format(path))
            self.storage[path] = set()
        else:
            print('storage["{0}"] exists'.format(path))
        self.storage[path].add(link)
        print('storage["{0}"].add("{1}")'.format(path, link))
        try:
            links_set = self.storage[path]
            print("Stored: {0}".format(links_set))
            return links_set
        except KeyError:
            return 'Nothing stored eventually.'
        
    def retrieve(self, path):
        try:
            print("Retrieving path '{0}'".format(path))
            return self.storage[path]
        except KeyError:
            return 'Nothing here.'
