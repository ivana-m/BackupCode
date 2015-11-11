from bisect import bisect
from bisect import insort

#specify directory where application files are located. Replace with your own path.
appDir = r"D:\Documents\Academics\Project\Project\project_data\applications_power_ordered"
#specify directory location of output file. Replace with your own path.
outDir = r"D:\Documents\Academics\Project\Project\outputFiles\naive"

#=================================================================#
#input variables
#=================================================================#
powerCap = 1100
numApps = 7
numMachines = 10 #irrelevant for naive...
ALG = "naive"

#name output file
out = open(outDir +"/"+ str(powerCap) + "-" + str(numApps),'w')

#select which applications should be scheduled from the application directory
def schedule_applications(ALG, numApps):
    applications = []
    if(ALG == "naive"):
        #for naive implementation, select the first numApps applications
        for i in range(0,numApps):
            app = open(appDir+"/"+str(i),'r')
            appData = app.read()
            applications.append(appData)
            app.close()
    return applications

#allocate power for each application
def allocate_power(ALG, powerCap, numApps):
    powerPerApp = 0.0
    if(ALG == "naive"):
        powerPerApp = powerCap/numApps
    print(powerPerApp)
    return powerPerApp

#get performance based on power allocation
def get_performance(ALG, powerCap, app, powerPerApp):
    performanceRow = ""
    if(ALG == "naive"):
        app = app.strip()
        runs = app.split("\n")
        numRuns = len(runs)
        shortestTime = 10000000
        shortestRun = ""
        for run in runs:
            perf = float(run.split('\t')[1])
            if(perf <= shortestTime):
                shortestTime = perf
                shortestRun = run
            performanceRow = shortestRun       
    return performanceRow

def get_power(run):
    return float(run.split('\t')[2])

#*****************************************************************************# 
#SIMULATOR MAIN FUNCTION
#*****************************************************************************#

def sim(ALG, powerCap, numApplications, numMachines):
    applications = schedule_applications(ALG, numApplications) #get all the scheduled applications
    if(len(applications) != numApplications):
        print("ERR: Something went wrong with scheduling applications")
        return -1
    #find power allocated to each application
    powerPerApp = allocate_power(ALG, powerCap, numApplications)
    
    #prepare buffer for output file
    outFileBuffer = ""
    currentPow = 0
    for i in range(0, numApplications):
        app = applications[i]
        performanceRow = get_performance(ALG, powerCap, app, powerPerApp)
        currentPow += get_power(performanceRow)
        if(currentPow <= powerCap):
            outFileBuffer += str(i) + "\t" + performanceRow +"\n"
            
    return outFileBuffer

#*****************************************************************************# 
#End of simulator
#*****************************************************************************# 

buff = sim(ALG, powerCap, numApps, numMachines)
if(buff != -1):
    out.write(buff)
out.close()