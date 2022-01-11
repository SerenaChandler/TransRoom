import crud, model, server, os, json
from random import choice, randint

os.system('dropdb comments')
os.system('createdb comments')

model.connect_to_db(server.app)
model.db.create_all()