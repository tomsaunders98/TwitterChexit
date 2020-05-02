####################################################################
##### Upload Regularly to the ftp server for remote monitoring #####
####################################################################

import ftplib
import logging
import time
import sys
#logging config, all output to log file but in this case only errors anyway, stored locally not uplaod
logging.basicConfig(format='%(asctime)-15s %(name)s - %(levelname)s - %(message)s')
sys.stdout = open('upload.log', 'a')
sys.stderr = sys.stdout

# upload function
def uploadfile(filename):
    #not most elegant way of finding last line of file, but check to see if InfluenceWrangle has finished
    for line in open(filename):
        pass
    # if last line is Completed then pass up to main loop
    if line == "Completed!":
        return 1
    session = ftplib.FTP_TLS('', '', '')
    file = open(filename, 'rb')
    filemsg = "STOR " + filename
    session.storbinary(filemsg, file)
    file.close()
    session.quit()


while True:
    try:
        # if Influence finished then break infinite loop
        if uploadfile("InfluenceWrangle.log") == 1:
            print("Completed!")
            break
        # else every 5 mins
        else:
            uploadfile("InfluenceWrangle.log")
            time.sleep(300)
    # catch all, usually addrinfo error (internet issue) so 15 mins sleep best way to sort out
    except:
        time.sleep(900)
        pass














