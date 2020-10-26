from flask import session
from json import JSONEncoder


class Department:
    def __init__(self, key):
        self.id = key
        self.name = session['departments'][str(key)].get('name')
        self.superdepartment = session['departments'][str(key)].get('superdepartment')


class Office:
    def __init__(self, key):
        self.id = key
        self.country = session['offices'][str(key)].get('country')
        self.address = session['offices'][str(key)].get('address')
        self.city = session['offices'][str(key)].get('city')


class ResourceEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
