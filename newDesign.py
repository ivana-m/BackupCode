class Task(object):
    
    def __init__(self, index, configIndex, power, time, performance, startTime = 0, endTime = 0, currentPower = 0):
        self.index = int(index)
        self.configIndex = int(configIndex)
        self.requiredPower = float(power)
        self.time = float(time)
        self.allocatedPower = float(power)
        self.performance = float(performance)
        self.startTime = float(startTime)
        self.endTime = float(endTime)
        self.currentPower = float(currentPower)
    def allocate_power(self, power):
        self.allocatedPower = float(power)

import bisect
#specify directory where application files are located. Replace with your own path.
taskDir = r"D:\Documents\Academics\Project\Project\applications"#project_data\applications_power_ordered"

#specify directory location of output file. Replace with your own path.
outDirNaive = r"D:\Documents\Academics\Project\Project\outputFiles\newDesign\withTime\naive"
outDirDavid = r"D:\Documents\Academics\Project\Project\outputFiles\newDesign\withTime\david"


#select which applications should be loaded from the application directory
def load_tasks(n):
    tasks = []
    
    for i in range(0,n):
        if(i == 8):
            continue
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
    currentPower = 0
    for taskFile in tasks:
        closestTask = get_closestTask(taskFile, powerPerTask)
        closestTask.currentPower = currentPower
        closestTask.startTime = 0
        closestTask.endTime = closestTask.time
        currentPower += closestTask.requiredPower
        
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
    startTime = str(task.startTime)
    endTime = str(task.endTime)
    #var = str(var)
    currentPower = str(task.currentPower)
    var = currentPower 
    return index + tab + configIndex + tab + time + tab + performance + tab + power + tab + startTime + tab + endTime + tab + var + nl

def new_empty_line(task, var):
    tab = "\t"
    nl = "\n"
    index = str(task.index)
    configIndex = str(task.configIndex)
    var = str(var)
    zero = "0"
    return index + tab + configIndex + tab + zero + tab + zero + tab + zero  + tab + zero + nl
    
def get_pace(taskFile):
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

def get_highest_config(taskFile):
    maxIn = -1
    maxTask = None
    for task in taskFile:
        if(task.configIndex >= maxIn):
            maxIn = task.configIndex
            maxTask = task
    return maxTask

def get_lowest_config(taskFile):
    lowestTask = None
    for task in taskFile:
        if(task.configIndex == 0):
            lowestTask = task
    return lowestTask

def process_group(taskGroup, var):
    buff = ""
    for task in taskGroup:
        buff += new_line(task, var)
    return buff



def pack_tasks(tasks, powerCap, current_power, startTime, longestTime):
    
    taskGroup = []
    remainingTasks = []
    tempcurrent_power = current_power
    for taskFile in tasks:
        task = get_pace(taskFile)
        tempcurrent_power += task.requiredPower
        if(tempcurrent_power <= powerCap):
            current_power = tempcurrent_power
            if(longestTime == 0 or startTime + task.time <= longestTime):
                task.startTime = startTime
                task.endTime = startTime + task.time
                taskGroup.append(task)
            else:
                remainingTasks.append(taskFile)
            
            
            #task.currentPower = current_power
        else:
            tempcurrent_power -= task.requiredPower
            #current_power -= task.requiredPower
            remainingTasks.append(taskFile)
    return taskGroup, remainingTasks, current_power

def sort_tasks(tasks):
    return sorted(tasks, key=lambda x: x.time)
    
def assign_powers(taskGroup, current_power):
    for task in taskGroup:
        task.currentPower = current_power
        current_power += task.requiredPower
    return taskGroup

def recursive_sim(tasks, current_power, powerCap, startTime, remainingTasks, longestTime, initialPowerCap, buff, prevtaskGroup, debug=False, bound = 2):
    thislongestTime = longestTime
    if(len(remainingTasks) > 0):
        if(debug):
            print("passing current power to get group:", current_power, "and longestTime bound: ",longestTime * bound)
        taskGroup, remainingTasks, current_pow = pack_tasks(tasks, powerCap, current_power, startTime, longestTime * bound)
        if(debug):
            print("initial: "+str(len(tasks))+", packed tasks: "+str(len(taskGroup)) + ", remaining: "+str(len(remainingTasks)), current_pow, current_power)
        
        if(len(taskGroup) > 0 and taskGroup != None):
            
            taskGroup = sort_tasks(taskGroup)
            taskGroup = assign_powers(taskGroup, current_power)
            if(len(prevtaskGroup) == 0):
                longestTime = 0
            else:
                longestTime = prevtaskGroup[len(prevtaskGroup)-1].endTime
            
            thislongestTime = taskGroup[len(taskGroup)-1].endTime
            if(thislongestTime > longestTime): #alternatively, do not schedule task if it is exceeding the longest time already for the first round...
                longestTime = thislongestTime
            if(debug):
                print("initial: "+str(len(tasks))+" longestTime "+str(longestTime), thislongestTime)
            buff= process_group(taskGroup, current_pow)
            if(len(remainingTasks) == 0):
                if(debug):
                    print("no remaining tasks:\n"+buff)
                return buff, initialPowerCap, [], longestTime
            previousPower = current_power
            groupCurrentPower = 0
            i = 0
            for task in taskGroup:
                newPowerCap = 0.0
                if(i == len(taskGroup) -1):
                    newPowerCap = powerCap
                else:
                    newPowerCap = task.requiredPower + previousPower
                if(groupCurrentPower == 0 and i != 0):
                    
                    for task2 in taskGroup[:i]:
                        groupCurrentPower += task2.requiredPower
                    current_power = groupCurrentPower
                    
                if(debug):
                    print("Task", task.index, "sending powercap: ", newPowerCap, "and got powercap:",powerCap, "with initial: ", initialPowerCap, "but this much power consumed: ",current_power, "with ", len(remainingTasks),"remaining tasks")
                task.currentPower = current_power
                if(len(taskGroup) > 1):
                    initialPowerCap = powerCap
                if(debug):
                    print("looping from "+str(len(taskGroup)) + " tasks. inserting " + str(len(remainingTasks)) + " remaining tasks")
                b, currentPow, remainingTasks, longestTime = recursive_sim(remainingTasks, current_power, newPowerCap, task.endTime, remainingTasks, longestTime, initialPowerCap, buff, taskGroup, debug)
                buff += b
                
                
                if(currentPow > 0):
                    current_power += task.requiredPower
                    groupCurrentPower = 0
                else:
                    
                    groupCurrentPower = task.requiredPower
                #current_power += currentPow
                #if(task != taskGroup[0]):
                
                previousPower += task.requiredPower
                i+=1
                
            if(len(remainingTasks) > 0):
                if(debug):
                    print("there are still remaining tasks. the initial power cap is: ", initialPowerCap, current_pow, "longest: ", longestTime, thislongestTime)
                if(len(prevtaskGroup) == 0):
                    b, current_pow, remainingTasks, longestTime = recursive_sim(remainingTasks, 0, initialPowerCap, longestTime, remainingTasks, 0, initialPowerCap, buff, [], debug)
                    buff += b
                return buff, current_pow, remainingTasks, longestTime
            return buff, current_power, remainingTasks, longestTime
        elif(len(remainingTasks) > 0):
            if(debug):
                print("no packed tasks, but " + str(len(remainingTasks)) + " remaining. And current power cap is: ",powerCap, "initial: ", initialPowerCap)
            
            return "", 0, remainingTasks, longestTime
        else:
            
            current_power = 0
            if(debug):
                print("not enough in task group. initial: "+str(len(tasks))+", tasks: "+str(len(taskGroup)) + ", remaining: "+str(len(remainingTasks)))
            return buff, current_power, remainingTask, longestTime
    else:
        return "", 0, [], 0
      

def david_simulator(tasks, numTasks, powerCap):
    outFileBuff = ""
    currentPower = 0
    taskGroup = []
    longestTime = 0
    groupLongestTime = 0
    packedTasks = []
    while(len(packedTasks) != len(tasks)):
        
        for taskFile in tasks:
            task = get_pace(taskFile)
            if(task in packedTasks):
                print(len(tasks), task.index,"was packed already")
                continue
            #task = get_least_energy(taskFile)
            #task = get_shortest_time(taskFile)
            #task = get_most_performing(taskFile)
            #task = get_highest_config(taskFile)
            #task = get_lowest_config(taskFile)
            
            #currentPower += task.requiredPower
            
            if(currentPower + task.requiredPower <= powerCap):
                
                task.currentPower = currentPower
                task.startTime = groupLongestTime
                task.endTime = task.startTime + task.time
                #groupLongestTime = task.endTime
                taskGroup.append(task)
                packedTasks.append(task)
                
                currentPower += task.requiredPower
                if(task.endTime >= longestTime):
                    longestTime = task.endTime  
                #print("packed.",task.index,len(packedTasks),currentPower)
            else:
                outFileBuff+= process_group(taskGroup, longestTime)
                currentPower = 0
                taskGroup = []
                groupLongestTime = longestTime
                longestTime = 0
                #print("not packed.", task.index, len(packedTasks))
                if(task.requiredPower <= powerCap):
                    taskGroup.append(task)
                    packedTasks.append(task)
                    task.currentPower = currentPower
                    task.startTime = groupLongestTime
                    task.endTime = task.startTime + task.time
                    currentPower = task.requiredPower
                    
                    longestTime = task.endTime
                    #print("packed in new task group", task.index, len(packedTasks), currentPower)
                else:
                    outFileBuff+= ""#new_empty_line(task, longestTime)
                    return ""
                
        if(len(taskGroup) > 0):
            outFileBuff += process_group(taskGroup, longestTime)
        if(len(packedTasks) == 0):
            return ""
    return outFileBuff.strip()
    
#=================================================================#
#input variables
#=================================================================#
#powerCap = 2000
#numTasks = 10

#for numTasks in range(1,28):
    #tasks = load_tasks(numTasks)
    #for powerCap in range(100, 10100, 100):
        ##name output file
        #outN = open(outDirNaive +"/"+ str(powerCap) + "-" + str(numTasks),'w')
        ##name output file
        #outD = open(outDirDavid +"/"+ str(powerCap) + "-" + str(numTasks),'w')
        
        #outN.write(naive_simulator(tasks, numTasks, powerCap))
        #outN.close()
        #outD.write(david_simulator(tasks, numTasks, powerCap)) 
        #outD.close()
        
        
            
for numTasks in range(1, 28):
#numTasks = 12
    tasks = load_tasks(numTasks)

#powerCap = 1000
    for powerCap in range(100, 6600, 100):
        print(numTasks, powerCap)
        buff, cp, var, lt = recursive_sim(tasks, 0, powerCap, 0, tasks, 0, powerCap, "", [], False)
        #print(buff)
        nt = str(numTasks)
        if(numTasks > 8):
            nt = str(numTasks - 1)
        #f = open(r"D:\Documents\Academics\Project\Project\outputFiles\recursive/"+str(powerCap)+"-"+nt,'w')
        #f.write(buff)
        #f.close()
        #outN = open(outDirNaive +"/"+ str(powerCap) + "-" + nt,'w')
        #name output file
        outD = open(outDirDavid +"/"+ str(powerCap) + "-" + nt,'w')
        
        #outN.write(naive_simulator(tasks, numTasks, powerCap))
        #outN.close()
        outD.write(david_simulator(tasks, numTasks, powerCap)) 
        outD.close()  