# Requires to be stored in directory /r1/
# Data assumed to follow the format in readme.txt
# Data taken from https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247?file=24857825
import os, pathlib 
import csv
import datetime
import pandas as pd

def deviceByWeek():
    currentDir = os.getcwd()
    pathlib.Path(currentDir + '/tmp/Device').mkdir(parents=True, exist_ok=True)
    startDate = None

    with open(currentDir + '/r1/device.csv') as deviceFile:
        weekStart = None
        currentDf = []
        fileReader = csv.reader(deviceFile, delimiter=',')
        lineCount = 0
        for row in fileReader:
            if lineCount == 0:
                print("Processing file:", deviceFile)
                lineCount += 1
                continue
            date = datetime.datetime.strptime(row[1], '%m/%d/%Y %H:%M:%S')
            if weekStart is None:
                weekStart = date
                startDate = date
            while (date.date() - weekStart.date()).days >= 7:
                tmpFileName = currentDir + '/tmp/Device/' + weekStart.strftime("%m-%d-%Y") + '.csv'
                f = open(tmpFileName, "w+")
                f.close()
                df = pd.DataFrame(currentDf, columns=['user', 'date', 'pc', 'activity', 'details'])
                df.to_csv(tmpFileName, sep=',', index=False)
                currentDf = []
                weekStart += datetime.timedelta(days=7)
            currentDf.append([row[2], row[1], row[3], 'DeviceConnectionActivity', row[4]])
    return startDate
            

def logonByWeek(startDate):
    currentDir = os.getcwd()
    pathlib.Path(currentDir + '/tmp/Logon').mkdir(parents=True, exist_ok=True)

    with open(currentDir + '/r1/logon.csv') as logonFile:
        weekStart = startDate
        currentDf = []
        fileReader = csv.reader(logonFile, delimiter=',')
        lineCount = 0
        for row in fileReader:
            if lineCount == 0:
                print("Processing file:", logonFile)
                lineCount += 1
                continue
            date = datetime.datetime.strptime(row[1], '%m/%d/%Y %H:%M:%S')
            while (date.date() - weekStart.date()).days >= 7:
                tmpFileName = currentDir + '/tmp/Logon/' + weekStart.strftime("%m-%d-%Y") + '.csv'
                f = open(tmpFileName, "w+")
                f.close()
                df = pd.DataFrame(currentDf, columns=['user', 'date', 'pc', 'activity', 'details'])
                df.to_csv(tmpFileName, sep=',', index=False)
                currentDf = []
                weekStart += datetime.timedelta(days=7)
            currentDf.append([row[2], row[1], row[3], 'LogonActivity', row[4]])
            
def httpByWeek(startDate):
    currentDir = os.getcwd()
    pathlib.Path(currentDir + '/tmp/Http').mkdir(parents=True, exist_ok=True)

    with open(currentDir + '/r1/Http.csv') as httpFile:
        weekStart = startDate
        currentDf = []
        fileReader = csv.reader(httpFile, delimiter=',')
        print("Processing file:", httpFile)
        for row in fileReader:
            date = datetime.datetime.strptime(row[1], '%m/%d/%Y %H:%M:%S')
            while (date.date() - weekStart.date()).days >= 7:
                tmpFileName = currentDir + '/tmp/Http/' + weekStart.strftime("%m-%d-%Y") + '.csv'
                f = open(tmpFileName, "w+")
                f.close()
                df = pd.DataFrame(currentDf, columns=['user', 'date', 'pc', 'activity', 'details'])
                df.to_csv(tmpFileName, sep=',', index=False)
                currentDf = []
                weekStart += datetime.timedelta(days=7)
            currentDf.append([row[2], row[1], row[3], 'HTTPActivity', row[4]])

def outputCombinedByWeek(employeeData):
    currentDir = os.getcwd()
    pathlib.Path(currentDir + '/ExtractedData').mkdir(exist_ok=True)

    deviceFiles = sorted(os.listdir(currentDir+'/tmp/Device'))
    for outputFilename in deviceFiles:
        print("Outputting file", outputFilename)
        outputF = open(currentDir + '/ExtractedData/' + outputFilename, "w+")
        deviceFile = open(currentDir + '/tmp/Device/' + outputFilename)
        device = deviceFile.readline()
        logonFile = open(currentDir + '/tmp/Logon/' + outputFilename)
        logon = logonFile.readline()
        httpFile = open(currentDir + '/tmp/Http/' + outputFilename)
        http = httpFile.readline()

        device = deviceFile.readline()
        if device:
            deviceDt = datetime.datetime.strptime(device.split(',')[1], '%m/%d/%Y %H:%M:%S') 
        logon = logonFile.readline()
        if logon:
            logonDt = datetime.datetime.strptime(logon.split(',')[1], '%m/%d/%Y %H:%M:%S') 
        http = httpFile.readline()
        if http:
            httpDt = datetime.datetime.strptime(http.split(',')[1], '%m/%d/%Y %H:%M:%S') 
        while device or logon or http:
            if device and logon and http:
                if deviceDt < logonDt and deviceDt < httpDt:
                    outputF.write(device)
                    device = deviceFile.readline()
                    if device:
                        deviceDt = datetime.datetime.strptime(device.split(',')[1], '%m/%d/%Y %H:%M:%S') 
                
                elif logonDt < deviceDt and logonDt < httpDt:
                    outputF.write(logon)
                    logon = logonFile.readline()
                    if logon:
                        logonDt = datetime.datetime.strptime(logon.split(',')[1], '%m/%d/%Y %H:%M:%S') 
                else:
                    outputF.write(http)
                    http = httpFile.readline()
                    if http:
                        httpDt = datetime.datetime.strptime(http.split(',')[1], '%m/%d/%Y %H:%M:%S') 
            elif device and logon:
                if deviceDt < logonDt:
                    outputF.write(device)
                    device = deviceFile.readline()
                    if device:
                        deviceDt = datetime.datetime.strptime(device.split(',')[1], '%m/%d/%Y %H:%M:%S') 
                
                else:
                    outputF.write(logon)
                    logon = logonFile.readline()
                    if logon:
                        logonDt = datetime.datetime.strptime(logon.split(',')[1], '%m/%d/%Y %H:%M:%S') 
            elif device and http:
                if deviceDt < httpDt:
                    outputF.write(device)
                    device = deviceFile.readline()
                    if device:
                        deviceDt = datetime.datetime.strptime(device.split(',')[1], '%m/%d/%Y %H:%M:%S') 
                else:
                    outputF.write(http)
                    http = httpFile.readline()
                    if http:
                        httpDt = datetime.datetime.strptime(http.split(',')[1], '%m/%d/%Y %H:%M:%S') 
            elif logon and http:
                if logonDt < httpDt:
                    outputF.write(logon)
                    logon = logonFile.readline()
                    if logon:
                        logonDt = datetime.datetime.strptime(logon.split(',')[1], '%m/%d/%Y %H:%M:%S') 
                else:
                    outputF.write(http)
                    http = httpFile.readline()
                    if http:
                        httpDt = datetime.datetime.strptime(http.split(',')[1], '%m/%d/%Y %H:%M:%S') 
            elif device:
                outputF.write(device)
                device = deviceFile.readline()
                if device:
                    deviceDt = datetime.datetime.strptime(device.split(',')[1], '%m/%d/%Y %H:%M:%S') 
            elif logon:
                outputF.write(logon)
                logon = logonFile.readline()
                if logon:
                    logonDt = datetime.datetime.strptime(logon.split(',')[1], '%m/%d/%Y %H:%M:%S') 
            else:
                outputF.write(http)
                http = httpFile.readline()
                if http:
                    httpDt = datetime.datetime.strptime(http.split(',')[1], '%m/%d/%Y %H:%M:%S')


        deviceFile.close()
        logonFile.close()
        httpFile.close()
        outputF.close()
    

def outputData():
    currentDir = os.getcwd()
    dataDir = currentDir + '/r1'

    print("Expecting data in directory", dataDir)

    startDate = deviceByWeek()
    if startDate is None:
        print("Error: Did not find any device data")
        return
    logonByWeek(startDate)
    httpByWeek(startDate)

    employees = {} # map user -> (employee name, email, role) where user = domain || '/' ||user_id
    LDAPDir = dataDir + '/LDAP'
    ldapFiles = sorted(os.listdir(LDAPDir))
    for ladpFilename in ldapFiles:
        with open(LDAPDir + '/' + ladpFilename) as ldapFile:
            ldapReader = csv.reader(ldapFile, delimiter=',')
            lineCount = 0
            for row in ldapReader:
                if lineCount == 0:
                    print("Processing file:", ladpFilename)
                    lineCount += 1
                else:
                    domain = row[2][:-4].upper()
                    user = domain + '/' + row[1]

                    if user in employees and (employees[user][0] != row[0] or employees[user][1] != row[3] or employees[user][2] != row[4]):
                        print("Contrasting entries: had", employees[user], "for user", user, "but got", (row[0], row[3], row[4]))
                    employees[user] = (row[0], row[3], row[4])
                    lineCount += 1

    outputCombinedByWeek(employees)

    print("done")    




if __name__ == "__main__":
    outputData()