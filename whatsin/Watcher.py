import time, traceback, datetime
from datetime import timedelta
from threading import Timer
from whatsin import db
from whatsin.models import Fridge_item

class Watcher:
    def __init__(self):
        self.starttime = time.time()

    def run(self):
        self.every()
    
    def checkSellby(self, payload):
        print( "Checking sell-bys...")
        offItems = []
        todaysDate = datetime.datetime.now()
        for Fridge_item in payload:
            formatted_item_date = Fridge_item.use_by.strftime("%d-%m-%Y")
            formatted_today_date = todaysDate.strftime("%d-%m-%Y")

            if formatted_item_date < formatted_today_date:
                print(Fridge_item.item_name + " is off, it went off on " + str(Fridge_item.use_by))
                offItems.append(Fridge_item)
            elif formatted_item_date == formatted_today_date:
                print(Fridge_item.item_name + " is going off today...")
        return offItems


    def every(self):
        payload = Fridge_item.query.all()
        self.checkSellby(payload)
        Timer(10, self.every).start()

        
    def action(self):
        print("tick", time.time())

    
