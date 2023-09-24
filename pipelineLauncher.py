import book
import time
import configData
import logging
from logging_config import configure_logging

configure_logging()

json_file_path = "F:/Work Folder/ticSeleBot/seatConfig.json"  
success = False

config = configData.bookingDetail(json_file_path)
config.initialize()
config.showConfig()
config.showTargetTime()
#*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*#
fuckedUpSeat = []
def queueAndWaitHandler():
    """ current_time = time.time()
    queueWait = config.queue_time -5 - current_time
    startWait = config.start_time - 10 - current_time """
   
    book.loadAndLogin(config.url)
    print("----------> The program is still running (รอเวลารับบัตรคิว {}) <----------\n\n".format(config.queueTime))
    config.countdown(config.queue_time)
    
    book.click_btn_red_DIRECT()
    print("----------> รับคิวเรียบร้อย รอเวลาเปิดขายบัตร at {}".format(config.startTime))
    config.countdown(config.start_time)

    print("----------> YOU ARE IN QUEUE!, wait until your turn")
    logging.info("----------> YOU ARE IN QUEUE!, wait until your turn")
    if book.waitInQueue(json_file_path): #if waitInQueue() returns True, it means the config file has changed, will call config.update() to read the config file again
        config.update()
    print("----------> IT'S YOUR TURN, Booking starts")


    book.acceptTerms()
    book.clickDropdown(config.day)

def normalBookingHandler():
 
    book.loadAndLogin(config.url) #load URL and login with the given username and password 
    print("----------> The program is still running (wait until target time) <----------\n\n")
    config.countdown(config.start_time)

    if config.oneDay: #if concert has one round, click button directly by calling click_btn_red_DIRECT()
        book.click_btn_red_DIRECT()
    else:
        book.moreDay(config.day) #if concert has multiple rounds, click call moreDay() to handle it properly

    book.acceptTerms() #click accept terms and conditions by calling acceptTerms()

if config.queue:
    queueAndWaitHandler()
else:
    normalBookingHandler()
    

success = False #success flag change to TRUE if the seats are clicked successfully, default=False
Mstart = time.time()
for zone in config.zone_list: #loop through zones in zone list
    book.findZone(zone)
    while not success: #this while loop keep looping over a zone in case the click fucntion got intercepted by "this seat has been taken" popup
        seats= book.findAllSeatUnchecked(config.price, fuckedUpSeat)  
        print("FUCKUP ", fuckedUpSeat)
        print("Zone:", config.price,zone)
        logging.info(f"----> current zone {zone, config.price}")

        if len(seats) < config.limit:
            book.noSeatHandler() #if no. of seat available in this one less than the desired number, Move to the next zone
            print("NO seat found, moving to next zone")
            break  #move to next zone by exiting this zone-level while loop and go to seatmap-level for loop
        
        if config.limit == 1 or (config.limit > 1 and config.mode == "any"):
            seatStage = book.clickSeat(config.limit, seats)
            
            print("SEAT stage: ", seatStage)

            if seatStage == True and book.completeBooking(config.name_list):
                success = True
                print("SUCCESS STAGE", success)
                break
            else:
                print("fucked --->")
                fuckedUpSeat.append(seatStage)
            
        elif config.limit > 1 and config.mode == "close":
            consecBlock = book.findConsecseats(config.limit, seats) #allocate continuous block of empty seats
            if len(consecBlock) >= config.limit:
                seatStage = book.clickSeat(config.limit, consecBlock)
                print("SEAT stage: ", seatStage)
                if seatStage == True and book.completeBooking(config.name_list): 
                    success = True

                    break
            else:
                fuckedUpSeat.append(seatStage)
                book.noSeatHandler()
                break

    if success:
        break
    else:
        print("FAILED---->")
        success = False

Mend = time.time()

if success:
    print("------SUCCESS: MAIN LOOP TERMINATED------, TIME TAKEN: ", Mend-Mstart)
    logging.info(f"------SUCCESS: MAIN LOOP TERMINATED------, TIME TAKEN: {Mend-Mstart}")
else:
    print("****************** BOOKING WAS UNSUCCESSFUL ******************.")
    logging.info("****************** BOOKING WAS UNSUCCESSFUL ******************.")

