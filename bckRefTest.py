from whatsin import db
from whatsin.models import *

items = Fridge_item.query.all()
for item in items:
    print(item.fridge_item_owner.username)
