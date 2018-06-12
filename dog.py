class Dog(object):
    """
    This class describes a Dog and features entries needed to make it a dog
    in the WordPress database.
    """
    def __init__(self, guid,name,description):
        super(Dog,self).__init__()
        self.guid = guid
        self.name = name
        self.description = description
        self.excerpt = 'Default Excerpt'
        self.ping = 'Default Ping'
        self.pinged = 'Default pinged'
        self.post_content_filtered = 'Default post_content_filtered'
