from bisect import bisect
from bisect import insort

#specify directory where application files are located. Replace with your own path.
appDir = r"D:\Documents\Academics\Project\Project\project_data\applications_power_ordered"
#specify directory location of output file. Replace with your own path.
outDir = r"D:\Documents\Academics\Project\Project\outputFiles\david"

#=================================================================#
#input variables
#=================================================================#
powerCap = 90000
numApps = 27
totalApps = 27
numMachines = 10
ALG = "naive"

#name output file
out = open(outDir +"/"+ str(powerCap) + "-" + str(numApps),'w')

app_pool = get_app_pool(totalApps)

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

#get all applications we have 
def get_app_pool(totalApps):
    applications = []
    for i in range(0,totalApps):
        app = open(appDir+"/"+str(i),'r')
        appData = app.read()
        applications.append(appData)
        app.close()
    return applications        

#list only the runs for each app at "race"
def process_apps(applications, ):
    #find power allocated to each application
    processedApps = []
    powerPerApp = allocate_power(ALG, powerCap, numApps)
    for i in range(0, numApps):
        app = applications[i]
        performanceRow = get_performance(ALG, powerCap, app, powerPerApp)
        processedApps.append(str(i) + "\t" + performanceRow +"\n")
    return processedApps

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
        minPowerDiff = powerCap
        powers = []
        for run in runs:
            power = float(run.split('\t')[2])
            powers.append(power)
        position = bisect(powers, powerPerApp, 0, numRuns)
        if(position == 0):
            minPowerDiff = powers[0]
        else:
            minPowerDiff = powers[position-1]
        if(minPowerDiff <= powerPerApp):
            performanceRow = runs[powers.index(minPowerDiff)]
        else: #the power for this task was too little, so it can't be scheduled
            performanceRow = "0\t0\t0"        
    return performanceRow

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
    for i in range(0, numApplications):
        app = applications[i]
        performanceRow = get_performance(ALG, powerCap, app, powerPerApp)
        outFileBuffer += str(i) + "\t" + performanceRow +"\n"
    return outFileBuffer

#*****************************************************************************# 
#End of simulator
#*****************************************************************************# 

buff = sim(ALG, powerCap, numApps, numMachines)
if(buff != -1):
    out.write(buff)
out.close()