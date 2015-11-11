class Task(object):
    
    def __init__(self, index, configIndex, power, time, performance):
        self.index = int(index)
        self.configIndex = int(configIndex)
        self.requiredPower = float(power)
        self.time = float(time)
        self.allocatedPower = float(power)
        self.performance = float(performance)
        
    def allocate_power(self, power):
        self.allocatedPower = float(power)

import bisect
#specify directory where application files are located. Replace with your own path.
taskDir = r"D:\Documents\Academics\Project\Project\applications"#project_data\applications_power_ordered"

#specify directory location of output file. Replace with your own path.
outDirNaive = r"D:\Documents\Academics\Project\Project\outputFiles\newDesign\withTime\most_performing\naive"
outDirDavid = r"D:\Documents\Academics\Project\Project\outputFiles\newDesign\withTime\most_performing\david"


#select which applications should be loaded from the application directory
def load_tasks(n):
    tasks = []
    
    for i in range(0,n):
        taskFile = open(taskDir+"/"+str(i),'r')
        taskRuns = []
        for line in taskFile:
            properties = line.strip().split('\t')
            index = i
            configIndex = properties[0]
            performance = properties[1]
            power = properties[2]
            time = properties[3]
            tsk = Task(index, configIndex, power, time, performance)
            taskRuns.append(tsk)
        tasks.append(taskRuns)
        taskFile.close()
    return tasks

def get_closestTask(taskFile, powerPerTask):
    minPowDiff = powerPerTask
    closestTask = None
    for task in taskFile:
        diff = powerPerTask
        if(task.requiredPower <= powerPerTask):
            diff = powerPerTask - task.requiredPower
            if(diff <= minPowDiff):
                minPowDiff = diff 
                closestTask = task
    if(closestTask is None):
        return Task(taskFile[0].index, 0, 0, 0, 0)
    else:
        return closestTask

def naive_simulator(tasks, numTasks, powerCap):
    powerPerTask = powerCap / numTasks
    outFileBuff = ""
    for taskFile in tasks:
        closestTask = get_closestTask(taskFile, powerPerTask)
        outFileBuff += new_line(closestTask, powerPerTask)
    return outFileBuff.strip()

def new_line(task, var):
    tab = "\t"
    nl = "\n"
    index = str(task.index)
    configIndex = str(task.configIndex)
    time = str(task.time)
    power = str(task.requiredPower)
    performance = str(task.performance)
    var = str(var)
    return index + tab + configIndex + tab + time + tab + performance + tab + power + tab + var + nl

def new_empty_line(task, var):
    tab = "\t"
    nl = "\n"
    index = str(task.index)
    configIndex = str(task.configIndex)
    var = str(var)
    zero = "0"
    return index + tab + configIndex + tab + zero + tab + zero + tab + zero + tab + var + nl
    
def get_race(taskFile):
    highestTask = None
    maxVal = -1
    for task in taskFile:
        ratio = task.performance/task.requiredPower
        if(ratio >= maxVal):
            maxVal = ratio
            highestTask = task
    return highestTask

def get_least_energy(taskFile):
    minVal = 100000000000000000
    bestTask = None
    for task in taskFile:
        product = task.time * task.requiredPower
        if(product <= minVal):
            minVal = product
            bestTask = task
    return bestTask

def get_shortest_time(taskFile):
    minVal = 10000000000000000
    shortestTask = None
    for task in taskFile:
        if(task.time <= minVal):
            minVal = task.time
            shortestTask = task
    return shortestTask 

def get_most_performing(taskFile):
    maxPerf = -1
    maxTask = None
    for task in taskFile:
        if(task.performance >= maxPerf):
            maxPerf = task.performance
            maxTask = task
    return maxTask    

def process_group(taskGroup, longestTime):
    buff = ""
    for task in taskGroup:
        buff += new_line(task, longestTime)
    return buff

def david_simulator(tasks, numTasks, powerCap):
    outFileBuff = ""
    currentPower = 0
    timeBoundary = 0
    taskGroup = []
    longestTime = 0
    for taskFile in tasks:
        #task = get_race(taskFile)
        #task = get_least_energy(taskFile)
        #task = get_shortest_time(taskFile)
        task = get_most_performing(taskFile)
        currentPower += task.requiredPower
        if(currentPower <= powerCap):
            taskGroup.append(task)
            if(task.time >= longestTime):
                longestTime = task.time            
        else:
            outFileBuff+= process_group(taskGroup, longestTime)
            currentPower = 0
            taskGroup = []
            longestTime = 0
            if(task.requiredPower <= powerCap):
                taskGroup.append(task)
                currentPower = task.requiredPower
                longestTime = task.time
            else:
                outFileBuff+= new_empty_line(task, longestTime)
            
    if(len(taskGroup) > 0):
        outFileBuff += process_group(taskGroup, longestTime)
    return outFileBuff.strip()
    
#=================================================================#
#input variables
#=================================================================#
#powerCap = 2000
#numTasks = 10

for numTasks in range(1,28):
    tasks = load_tasks(numTasks)
    for powerCap in range(100, 10100, 100):
        #name output file
        outN = open(outDirNaive +"/"+ str(powerCap) + "-" + str(numTasks),'w')
        #name output file
        outD = open(outDirDavid +"/"+ str(powerCap) + "-" + str(numTasks),'w')
        
        outN.write(naive_simulator(tasks, numTasks, powerCap))
        outN.close()
        outD.write(david_simulator(tasks, numTasks, powerCap)) 
        outD.close()