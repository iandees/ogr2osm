def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    for (k,v) in attrs.iteritems():
        tags[k] = v

    return tags
