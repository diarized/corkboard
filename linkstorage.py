import pprint

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

    def dump(self):
        pprint.pprint(self.storage)


class Link(object):
    def __init__(self, link, title='', tags=[]):
        self.name = link
        self.title = title
        self.tags = tags


class Dir(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = {}

    def add(self, file):
        self.files[file.name] = file

    def get(self, file_name):
        try:
            dir = self.files[file_name]
        except KeyError:
            dir = Dir(file_name, self)
            self.files[file_name] = dir
        return dir

    def ls(self):
        pprint.pprint(self.files)

    def lsR(self):
        print('DIR {0} ================================='.format(self.path()))
        for file in self.files.keys():
            try:
                self.files[file].lsR()
            except AttributeError:
                print file

    def path(self):
        print('entering path()')
        cwd = self
        print('my name is {0}'.format(self.name))
        full_path = self.name
        while cwd.parent:
            print('checking path of {0}'.format(cwd.parent.name))
            full_path = cwd.parent.name + '/' + full_path
            cwd = cwd.parent
        return '/' + full_path.lstrip('/')

class FileSystem(object):
    def __init__(self):
        self.root = Dir('/', None)

    def get(self, path):
        path_list = path.split('/')
        cwd = self.root
        for dir in path_list:
            cwd = cwd.get(dir)
        return cwd

    def add(self, path, file):
        cwd = self.get(path)
        cwd.add(file)
        return cwd

    def walk(self):
        self.root.lsR()

