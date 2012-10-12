import re
alnum = re.compile('[\W]+')
TAG_SEPARATOR = r'/'

def tags_to_path(tags_string):
    tags = [alnum.sub('', tag) for tag in tags_string.split()]
    path = TAG_SEPARATOR.join(tags)
    return path


