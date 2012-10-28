import pprint

DEBUG=False

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
    def __init__(self, link, title=''):
        self.name = link
        self.title = title


class Dir(object):
    def __init__(self, name, parent):
        if DEBUG:
            print('Dir.__init__(): initialization of directory ' + name)
        if parent:
            parent_path = parent.path()
            self.name = parent_path + name
            if DEBUG:
                print('Dir.__init__(): there is a parent = ' + parent_path)
        else:
            self.name = name
            if DEBUG:
                print('Dir.__init__(): there is no parent. I am root. Name for root is ' + name)
        self.parent = parent
        self.files = {}

    def add(self, link):
        self.files[link.name] = link

    def get(self, file_name):
        if DEBUG:
            print('Dir.get(): getting {0} by {1}'.format(file_name, self.name))
        try:
            dir_name = self.files[file_name]
        except KeyError:
            if DEBUG:
                print('Dir.get(): there is no {0}. Creating.'.format(file_name))
            dir_name = Dir(file_name, self)
            self.files[file_name] = dir_name
        return dir_name

    def ls(self):
        return self.files

    def lsR(self):
        print('DIR {0} ================================='.format(self.path()))
        for link in self.files.keys():
            try:
                self.files[link].lsR()
            except AttributeError:
                print link

    def path(self):
        if DEBUG:
            print('Dir.path(): dir name is {0}'.format(self.name))
        return self.name


class FileSystem(object):
    def __init__(self):
        self.root = Dir('/', None)
        self.length = 0

    def get(self, path):
        path = path.replace(' ', '/') # validation here
        path = path.lstrip('/')
        path_list = path.split('/')
        if DEBUG:
            print path_list
        cwd = self.root
        for subdir in path_list:
            if cwd.name == '/':
                path_to_subdir = subdir
            else:
                path_to_subdir = cwd.name + '/' + subdir
            if DEBUG:
                print('FileSystem.get(): getting the next subdir: ' + path_to_subdir)
            tmp = cwd.get(path_to_subdir)
            cwd = tmp
        return cwd

    def add(self, path, link):
        cwd = self.get(path)
        if DEBUG:
            print('FileSystem.add(): fs.add({0})'.format(path))
            print('FileSystem.add(): got Dir "{0}"'.format(cwd.name))
            print('FileSystem.add(): "{0}".add("{1}")'.format(cwd.name, link.name))
        cwd.add(link)
        self.length += 1
        return cwd

    def walk(self):
        self.root.lsR()

