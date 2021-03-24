from replit import db

def set_value(key, value):
  db[key] = value

def get_value(key):
  return db[key]