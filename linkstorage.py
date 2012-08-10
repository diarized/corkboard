from helpers import sp2sl

class Db(object):
    def __init__(self):
        self.storage = {}

    def store(self, link, title, tags_string):
        tags_string = sp2sl(tags_string)
        if self.storage.has_key(tags_string):
            self.storage[tags_string].add(link)
        else:
            self.storage[tags_string] = set()
            self.storage[tags_string].add(link)
        
    def retrieve(self, tags_string):
        try:
            return self.storage[tags_string]
        except KeyError:
            return 'Nothing here.'
