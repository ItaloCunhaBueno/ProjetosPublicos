import psutil
from pprint import pprint
from time import sleep

print("CPU USAGE")
while True:
        listOfProcessNames = {}
        # Iterate over all running processes
        for proc in psutil.process_iter():
            if proc.name() != 'System Idle Process':
                # Get process detail as dictionary
                pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
                # Append dict of process detail in list
                if pInfoDict['cpu_percent'] not in listOfProcessNames:
                    listOfProcessNames[pInfoDict['cpu_percent']] = pInfoDict['name']

        print("\r{0} - {1}%".format(listOfProcessNames[max(listOfProcessNames)], round(max(listOfProcessNames)/10, 1)), end='')
        sleep(1)