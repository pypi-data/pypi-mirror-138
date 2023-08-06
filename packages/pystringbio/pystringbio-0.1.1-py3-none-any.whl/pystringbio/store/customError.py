class StringRedisError(Exception):
    """Base class for other exceptions"""
    pass

class UniprotKeyMissing(StringRedisError):
    def __init__(self, uniprotQuery):
        self.uniprotQuery = uniprotQuery
    
    def __str__(self):
        return f"Uniprot Key {self.uniprotQuery} not found"

class StringKeyMissing(StringRedisError):
    def __init__(self, stringKeyQuery):
        self.stringKeyQuery = stringKeyQuery
    
    def __str__(self):
        return f"String Key {self.stringKeyQuery} not found"

class PpiKeyMissing(StringRedisError):
    def __init__(self, query):
        self.query = query
    
    def __str__(self):
        return f"Unknown protein Interaction Key {self.query}"