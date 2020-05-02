########################################
#### Upload Regularly to the server ####
########################################

import ftplib
import logging
import time
import sys
#logging config, all output to log file but in this case only errors anyway, stored locally not uplaod

logging.basicConfig(format='%(asctime)-15s %(name)s - %(levelname)s - %(message)s')
#sys.stdout = open('upload.log', 'a')
#sys.stderr = sys.stdout

# upload function
def uploadfile(filename):


    session = ftplib.FTP_TLS('', '', '')
    file = open(filename, 'rb')
    filemsg = "STOR " + filename
    session.storbinary(filemsg, file)
    file.close()
    session.quit()


while True:
    try:
        # if Influence finished then break infinite loop
        if uploadfile("GetFollowers.log") == 1:
            print("Completed!")
            break
        # else every 5 mins
        else:
            uploadfile("GetFollowers.log")
            time.sleep(300)
    # catch all, usually addrinfo error (internet issue) so 15 mins sleep best way to sort out
    except Exception as e:
        print(str(e))
        time.sleep(900)
        pass
