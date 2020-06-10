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
    
    def checkOffies(self, payload):
        print( "Checking for off items...")
        offItems = []
        todaysDate = datetime.datetime.now()
        for item in payload:
            formatted_item_date = item.use_by.strftime("%d-%m-%Y")
            formatted_today_date = todaysDate.strftime("%d-%m-%Y")
            if formatted_item_date < formatted_today_date:
                offItems.append(item)
        print("OFF ITEM(s) == " + str(offItems))
        return offItems

    def checkIffies(self, payload):
        iffyItems = []
        todaysDate = datetime.datetime.now()
        for item in payload:
            formatted_item_date = item.use_by.strftime("%d-%m-%Y")
            formatted_today_date = todaysDate.strftime("%d-%m-%Y")
            if formatted_item_date == formatted_today_date:
                iffyItems.append(item)
        print("IFFY ITEM(s) == " + str(iffyItems))
        return iffyItems


    def every(self):
        payload = Fridge_item.query.all()
        iffyItems = self.checkIffies(payload)
        offItems = self.checkOffies(payload)
        Timer(86400, self.every).start()
        
    def action(self):
        print("tick", time.time())

    
