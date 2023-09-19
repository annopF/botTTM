import book
import time
import datetime
import json


json_file_path = "F:/Work Folder/ticSeleBot/seatConfig.json"  
with open(json_file_path, "r") as file:
    data = json.load(file)
    
################################ CONFIG DATA FROM JSON FILE ################################
queue = data["queue"]               #[BOOL] concert has queue before booking
oneDay = data["oneDay"]             #[BOOL] concert has only one round
day = data["day"]                   #[INT] if concert has multiple days, pick one
zone_list = data["zone_list"]       #[LIST] zone you want to book
startTime = data["startTime"]       #[DICT] เวลาเปิดขายบัตร
queueTime = data["queueTime"]       #[DICT] เวลารับบัตรคิว
ticketPrice = data["ticketPrice"]   #[INT] price you want to book
fee = data["fee"]                   #[INT] ticket fee
limit = data["limit"]               #[INT] no. of tickets to purchase   
mode =  data["mode"]                #[STR] close = continuous seats, any = any seats (required only when limit > 1)
name_list = data["name_list"]       #[LIST] if concert requires a name to be written on the tickets 
url = data["url"]                   #[STR] url to concert main page
################################ CONFIG DATA FROM JSON FILE ################################

temp = [val for key, val in startTime.items()]
temp.extend([0,0,0,0])
target_time = time.mktime(tuple(temp)) #format: (Year, Month, Day, Hour, Minute)

tempQ = [val for key, val in queueTime.items()]
tempQ.extend([0,0,0,0])
queue_time = time.mktime(tuple(tempQ))
price = str(ticketPrice+fee)
success = False
#*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*#
def queueAndWaitHandler():
    current_time = time.time()
    queueWait = queue_time -5 - current_time
    startWait = target_time - 10 - current_time
    print("\n\n-------<<< CONFIRM BOOKING DETAIL >>>-------\n\nConcert: {}\nHas Queue: {}\nOnly One Day: {}\nChosen Day: {}\nZone: {}\nBooking Start: {}\nTicket Price: {}\nNo.of Tickets: {}\nMultiple Ticket Mode: {}\n--------------------------------------------"
        .format(url,queue,oneDay,day,zone_list,startTime,ticketPrice,limit,mode))
    
    book.loadAndLogin(url)
    print("----------> The program is still running (รอเวลารับบัตรคิว {}) <----------\n\n".format(queueTime))

    time.sleep(queueWait)
    
    book.click_btn_red_DIRECT()
    print("----------> รับคิวเรียบร้อย รอเวลาเปิดขายบัตร at {}".format(startTime))
    time.sleep(startWait)
    print("----------> YOU ARE IN QUEUE!, wait until your turn")
    book.waitInQueue()
    print("----------> IT'S YOUR TURN, Booking starts")


    book.acceptTerms()
    book.clickDropdown(day)

if queue:
    queueAndWaitHandler()
else:
    current_time = time.time()
    startWait = target_time - 10 - current_time
    time.sleep(startWait)
    print("----------> The program is still running (wait until target time) <----------\n\n")
    book.loadAndLogin(url)
    #time.sleep(startWait)

    if oneDay:
        book.click_btn_red_DIRECT()
    else:
        book.moreDay(day)

    book.acceptTerms()

""" for zone in zone_list:
    book.findZone(zone)
    seats = book.findAllSeatUnchecked(price)
    print("len seat:--=", len(seats))
    if len(seats) == 0:
        book.noSeatHandler()
        print("NO seat found, moving to next zone")
        break

    else:  
        if limit == 1:
            click = book.clickSeat(limit, seats)
            print(click)
            if click:
                success = True
                break
        elif limit > 1 and mode == "any":
            click = book.clickSeat(limit, seats)
            print(click)
            break
        elif limit > 1 and mode == "close":
            consecBlock = book.findConsecseats(limit,seats)
            if len(consecBlock) >= limit:
                book.clickSeat(limit,consecBlock)
                break

            else:
                book.noSeatHandler()
                print("NO consec block found, moving to next zone") """

success = False
confirmBookStatus = False
Mstart = time.time()
click = False
for zone in zone_list:
    book.findZone(zone)

    while not success:
        seats = book.findAllSeatUnchecked(price)  
        print("Zone:", price,zone)

        if len(seats) < limit:
            book.noSeatHandler()
            print("NO seat found, moving to next zone")
            break  # Move to the next zone
        
        if limit == 1 or (limit > 1 and mode == "any"):
            if book.clickSeat(limit, seats):
                print("clickis ",click)
                success = True
                break
            
            
        elif limit > 1 and mode == "close":
            consecBlock = book.findConsecseats(limit, seats)
            if len(consecBlock) >= limit:
                if book.clickSeat(limit, consecBlock):
                    print("clickis ",click)
                    success = True
                    break
            else:
                book.noSeatHandler()
                break

    if success and book.completeBooking(name_list):
        break

Mend = time.time()

if success:
    print("------SUCCESS: MAIN LOOP TERMINATED------, TIME TAKEN: ", Mend-Mstart)
else:
    print("Booking was unsuccessful.")

