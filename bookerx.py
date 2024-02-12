from multiprocessing import Queue, Process
from pipelineLauncher import startS_Booker
import json


print("Ticket Booker Project: BookerX, Version 11.0.2")
json_path = "seatConfig.json"
with open(json_path, "r") as file:
    data = json.load(file)

zone_list = data["zone_list"]

              
if __name__ == "__main__":
    sig_queue = Queue()
    
    for idx,zone in enumerate(zone_list):
        if isinstance(zone, list):
            segment = len(zone)
            print(f"{segment} workers will be employed in zone {zone[0]}")
            for idx_i,zone_i in enumerate(zone):
                Process(target=startS_Booker, args=(sig_queue,zone_i,idx_i,segment,)).start()

        else:
            Process(target=startS_Booker, args=(sig_queue,zone,None,None,)).start()
