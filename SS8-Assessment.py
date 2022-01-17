import time
import subprocess
from collections import namedtuple
from datetime import datetime
 
def remote_df(user, ip, path):     
    """
    Executes df on remote host and return
    (total, free, used) as int in bytes
    """
    Result = namedtuple('diskfree', 'total used free')
    output = subprocess.check_output(['ssh', '%s@%s' % (user, ip), '-C', 'df'], shell=False)
    output = output.splitlines()
    for line in output[1:]:                                                                                                     
        result = line.decode().split()
        if result[-1] == path:
            used = int(result[2])
            free = int(result[3])
            total = used + free
            return Result(total, used, free)
        else:
            raise Exception('Path "%s" not found' % path)
        
#print(remote_df('root', '192.168.0.182', '/'))

if __name__ == '__main__':
    time_interval = int(input("Please enter the time interval you would like: "))
    while True:
        with open('IP.txt', 'r') as IPFile, open("log.txt", 'a') as logFile:
            for line in IPFile:
                dskUsage = remote_df('root', line, '/')
                sttime = datetime.now().strftime('%Y/%m/%d_%H:%M:%S - ')
                logFile.write(sttime + " " + line + " " + 'total=' + str(dskUsage[0]) + ' used=' + str(dskUsage[0]) + ' free=' + str(dskUsage[2]) + "\n")
                logFile.flush()
            time.sleep(time_interval)