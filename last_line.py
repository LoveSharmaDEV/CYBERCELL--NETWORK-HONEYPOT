import threading
from Mal_Class import End_game
def file_updater():
    obj = End_game()
    fileHandle = open ( '/root/HONEYPOT/logs/log.txt',"r" )
    file = open('last_command.txt' , "w")
    lineList = fileHandle.readlines()
    fileHandle.close()
    Last_l = lineList[len(lineList)-1]
    obj.mal_done(Last_l)
    file.write(lineList[len(lineList)-1])
    threading.Timer(10 , file_updater).start()

file_updater()

