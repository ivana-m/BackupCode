import os

#rootdir = r"D:\Documents\Academics\Project\Project\testing\newDesign\outputShortest\tasks"
rootdir = r"D:\Documents\Academics\Project\Project\testing\newDesign\outputShortest\power"
#outDirTasks = r"D:\Documents\Academics\Project\Project\testing\tasks"
#outDirPow = r"D:\Documents\Academics\Project\Project\testing\power"

tasks = 0

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if(tasks > 0):
            numTasks = file.split('-')[1].split('.')[0]
            #power = file.split('-')[0]
            dirT = os.path.join(rootdir, numTasks)
            #dirP = os.path.join(rootdir, power)
            if not os.path.exists(dirT):
                os.makedirs(dirT)
            #if not os.path.exists(dirP):
            #    os.makedirs(dirP)            
            os.rename(os.path.join(rootdir,file),os.path.join(dirT,file))
            #os.rename(os.path.join(rootdir,file),os.path.join(dirP,file))
        else:
            power = file.split('-')[0]
            dirP = os.path.join(rootdir, power)

            if not os.path.exists(dirP):
                os.makedirs(dirP)            
            
            os.rename(os.path.join(rootdir,file),os.path.join(dirP,file))            