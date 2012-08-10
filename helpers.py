import re
alnum = re.compile('[\W]+')
TAG_SEPARATOR = r'/'

def sp2sl(tags_string):
    tags = [alnum.sub('', tag) for tag in tags_string.split()]
    tags_string = TAG_SEPARATOR.join(tags)
    return tags_string


