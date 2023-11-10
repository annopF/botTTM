import time
import json
import tabulate as tbl

################################ CONFIG DATA FROM JSON FILE ################################
class bookingDetail():
    def __init__(self, json_path):
        self.json_path = json_path
        self.queue = None              
        self.oneDay = None            
        self.day = None                   
        self.zone_list = None       
        self.startTime = None
        self.start_time = None       
        self.queueTime = None
        self.queue_time = None      
        self.ticketPrice = None
        self.price = None  
        self.fee = None                
        self.limit = None                 
        self.mode =  None             
        self.name_list = None    
        self.url = None  
    def converter(self):
        temp = [val for key, val in self.startTime.items()]
        temp.extend([0,0,0,0])
        start_time = time.mktime(tuple(temp)) #format: (Year, Month, Day, Hour, Minute)
        tempQ = [val for key, val in self.queueTime.items()]
        tempQ.extend([0,0,0,0])
        queue_time = time.mktime(tuple(tempQ))
        price = str(self.ticketPrice+self.fee)

        self.price = price
        self.queue_time = queue_time-5
        self.start_time = start_time-5
    def initialize(self):
        with open(self.json_path, "r") as file:
            data = json.load(file)
        self.queue = data["queue"]               #[BOOL] concert has queue before booking
        self.oneDay = data["oneDay"]             #[BOOL] concert has only one round
        self.day = data["day"]                   #[INT] if concert has multiple days, pick one
        self.zone_list = data["zone_list"]       #[LIST] zone you want to book
        self.startTime = data["startTime"]       #[DICT] เวลาเปิดขายบัตร
        self.queueTime = data["queueTime"]       #[DICT] เวลารับบัตรคิว
        self.ticketPrice = data["ticketPrice"]   #[INT] price you want to book
        self.fee = data["fee"]                   #[INT] ticket fee
        self.limit = data["limit"]               #[INT] no. of tickets to purchase   
        self.mode =  data["mode"]                #[STR] close = continuous seats, any = any seats (required only when limit > 1)
        self.name_list = data["name_list"]       #[LIST] if concert requires a name to be written on the tickets 
        self.url = data["url"]                   #[STR] url to concert main page
        self.converter()
    def update(self):
        with open(self.json_path, "r") as file:
            data = json.load(file)
        self.day = data["day"]
        self.zone_list = data["zone_list"]
        self.ticketPrice = data["ticketPrice"]
        self.limit = data["limit"]
        self.mode = data["mode"]
        print("config updated")

    def showConfig(self):
        table = [["has queue", "is oneday", "chosen day","zone list","price","number of ticket","mode","name list","queue time", "sales begin"], 
                 [self.queue, self.oneDay, self.day, self.zone_list, self.ticketPrice, self.limit, self.mode, self.name_list, self.queueTime, self.startTime]]
        print(tbl.tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
    def showTargetTime(self):
        if self.queue:
            tableQueue = [["queue time","sales begin time"],[self.queueTime, self.startTime]]
            print(tbl.tabulate(tableQueue, headers="firstrow", tablefmt="fancy_grid"))
        else:
            tableNoQueue = [["queue time","sales begin time"],["N/A", self.startTime]]
            print(tbl.tabulate(tableNoQueue, headers="firstrow", tablefmt="fancy_grid"))

    def countdown(self,target):
        while True:
            current_time = time.time()
            time_remaining = target - current_time

            if time_remaining <= 0:
                break

            days, remainder = divmod(int(time_remaining), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_formatted = f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"
            print(f"Time remaining: {time_formatted}", end='\r')
            time.sleep(1)

        return()
    def makeDup(zoneList):
        return [zoneList + zoneList]
################################ CONFIG DATA FROM JSON FILE ################################