import matplotlib.pyplot as plt #use for drawing
import matplotlib.patches as patches #use for drawing
import os
from operator import itemgetter



#location of all the output files to be drawn
directoryN = r"D:\Documents\Academics\Project\Project\outputFiles\newDesign\withTime\naive"
directoryD = r"D:\Documents\Academics\Project\Project\outputFiles\newDesign\withTime\david"
directoryR = r"D:\Documents\Academics\Project\Project\outputFiles\recursive"



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''DRAWING HELPER FUNCTIONS'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#use this at the very beginning
def init_figure():
    plt.ioff()
    fig = plt.figure(figsize=(17,15),dpi=60) #values obtained by handtweaking, but might be subject to change. size works well for 26 applications at once. For a smaller image, just remove the arguments and use:
    #fig = plt.figure() #instead
    return fig


#draws rectangle
#inputs: ax - suplot object [read below for how to get subplot]
# x, y - lower left corner of rectangle
# w - width of rectangle
# h - height of rectangle
def add_rectangle(ax, x, y, w, h):
    ax.add_patch(
        patches.Rectangle(
            (x,y), w, h,
            )
        )

#adds text anywhere on subplot
#inputs: ax - subplot object
# text - text to be rendered as string
# x, y - lower left corner of beginning of text
# fontsize
def add_label(ax, text, x, y, fontsize):
    ax.text(x,y,text,fontsize=fontsize)

#set the range of the whole plot if necessary, passing in the plot object.
#this is not essential, the plot will autoscale, but in case you need specific boundaries use it
def set_axis_range(xmin, xmax, ymin, ymax, plt):
    plt.axis((0,xmax,0,ymax))

#if you want to save the output of the figure as an image, use this at the very end
def save_figure(fig, fileName):
    fig.savefig(fileName+'.png', dpi='figure', bbox_inches='tight') 
    plt.close() #close plot - prevents plot from displaying. Use if generating many plots at once 
    
    
'''
To draw rectangles, we need a subplot. Add it like this:

ax = fig.add_suplot(111)

If you want two plots in the same figure, one below the other, then add them like so:

ax1 = fig.add_suplot(211) #2 rows, 1 column, top position
ax2 = fig.add_suplot(212) #2 rows, 1 column, bottom position

If we want them to share the same xrange, then do this:

ax2 = fig.add_subplot(212, sharex = ax1)

'''
'''
To draw red lines, use:

plt.plot([0,xmax],[ymax,ymax], 'r')
or
ax.axhline(y = ymax, c = 'r', linewidth=1, zorder=5)

Primary colors are the first character, but black is 'k'. Gray can be specified as a number, for example '0.75' would be a gray color.
'''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''END OF DRAWING HELPER FUNCTIONS'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''HELPER FUNCTIONS'''
'''these functions help either process some data, or they return some parameters
that can be drawn later, but are not responsible for drawing anything'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#this is only needed for labeling things, and it currently most useful in the naive version
#get translations of indeces 0-1023 to configuration indeces (#coresIndex, freqIndex, #mem_controllerIndex)
def get_configIndex_mapping(path):
    iConfig = {}
    ic = open(path, 'r')
    for line in ic:
        line = line.strip()
        line = line.split('\t')
        if(len(line) == 4 ):
            iConfig[line[0]] = "( "+line[1]+", "+line[2]+", "+line[3] + " )"
    ic.close()
    return iConfig

#get translations of application/task index to actual application/task name (only needed for labeling things, and currently most useful in naive version)   
def get_appIndex_mapping(path):
    iApp = {}
    ia = open(path, 'r')
    for line in ia:
        line = line.strip()
        line = line.split('\t')
        if(len(line) == 2 ):    
            iApp[line[0]] = line[1]
    ia.close()
    return iApp

#these are needed for correct labeling
iConfig = get_configIndex_mapping(r"D:\Documents\Academics\Project\Project\project_data\config_index.txt")
iApp = get_appIndex_mapping(r"D:\Documents\Academics\Project\Project\project_data\applicationsByIndex.txt")  

#return an array of arrays, containing the individual columns of each row from a file
def getLines(file):
    lines = []
    for line in file:
        line = line.strip()
        line = line.split('\t')
        lines.append(line)
    return lines


#find best and worst performance, and highest and lowest power consumed from all tasks
#this is useful for setting the xrange of the plot
def get_boundaries(lines, powerCap):
    shortestTime = 1000000
    longestTime = -1
    maxPow = -1
    minPow = powerCap
    for l in lines:
        t = float(l[2])
        p = float(l[4])
        if(t <= shortestTime):
            shortestTime = t
        if(t >= longestTime):
            longestTime = t
        if(p >= maxPow):
            maxPow = p
        if(p <= minPow):
            minPow = p
    return shortestTime, longestTime, maxPow, minPow

#this is only useful for David's heuristic
#returns the x coordinates of each task group until it reaches the power cap
def get_xbounds(lines):
    currentX = 0
    maxX = 0
    xcoords = []
    ycoords = []
    xbounds = []
    currentY = 0
    previousX = 0
    for line in lines:
        x = float(line[5])
        y = float(line[4])
        if(x != currentX):
            previousX += currentX
            currentX = x
            xbounds.append(currentX+previousX)
            maxX += currentX
            currentY = 0
        xcoords.append(previousX)
        ycoords.append(currentY)
        currentY += y
    return xcoords, ycoords, xbounds, maxX
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''END OF HELPER FUNCTIONS'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''






def dsply(file, fig, powerCap, row, col, pos, ax):
    f = open(file, 'r')
    lines = getLines(f)
    position = row*100+col*10+pos
    ax = fig.add_subplot(position, sharex = ax)
    for line in lines:
        w = float(line[6]) - float(line[5])
        h = float(line[4])
        x = float(line[5])
        y = float(line[7])
        add_rectangle(ax, x, y, w, h)
        plt.plot([x, x],[0,powerCap], '1') 
    ax.axhline(y = powerCap, c = 'r', linewidth=1, zorder=5)
    
    f.close()
    return    
    
def dsplyN(file, fig, powerCap, row, col, pos):
    f = open(file, 'r')
    lines = getLines(f)
    
    position = row*100+col*10+pos
    ax = fig.add_subplot(position)
    for line in lines:
        w = float(line[6]) - float(line[5])
        h = float(line[4])
        x = float(line[5])
        y = float(line[7])
        add_rectangle(ax, x, y, w, h)
    ax.axhline(y = powerCap, c = 'r', linewidth=1, zorder=5)
    
    f.close()
    return ax

def displayRecursive(file, powerCap, numApps, fig, axN):
    font = 12 #fontsize for the labels
    f = open(file, 'r')
    lines = getLines(f)
    ax = fig.add_subplot(313, sharex = axN)
    for line in lines:
        w = float(line[6]) - float(line[5])
        h = float(line[4])
        x = float(line[5])
        y = float(line[7])
        add_rectangle(ax, x, y, w, h)
    ax.axhline(y = powerCap, c = 'r', linewidth=1, zorder=5)
    f.close()
    return

def displayDavid(file, powerCap, numApps, fig, axN):  
    font = 12 #fontsize for the labels
    f = open(file, 'r')
    lines = getLines(f)
    #lines = sort_lines_by_perf(lines)
    #print(lines)
    if(len(lines) == 0):
        print("no results for "+file)
        return
    xcoords, ycoords, xbounds, xmax = get_xbounds(lines)
    ymax = powerCap
    ax = fig.add_subplot(312, sharex = axN)
    coord = 0
    for line in lines:

        w = float(line[2])
        h = float(line[4])
        
        add_rectangle(ax, xcoords[coord], ycoords[coord], w, h)
        text = " "+iApp[line[0]]+"\n "+iConfig[line[1]]
     
        #plt.plot([0,xmax],[y,y], '0.75') #draw horizontal line to indicate power per task
        #add_label(ax, text, xmax, ycoords[coord], font)
        coord += 1
    
    ax.axhline(y = ymax, c = 'r', linewidth=1, zorder=5)
    for x in xbounds:
        plt.plot([x,x],[0,ymax], '0.75')        
    f.close()
    return    

def displayNaive(file,powerCap, numApps, fig):  
    font = 12 #fontsize for the labels
    offset = powerCap/numApps
    f = open(file, 'r')
    lines = getLines(f)
    if(len(lines) == 0):
        print("no results for "+file)
        return
    maxPerf, minPerf, maxPow, minPow = get_boundaries(lines, powerCap)
    xmax = minPerf #largest x is determined by the slowest, or least performing task
    ymax = powerCap
    x = 0
    y = 0
    ax = fig.add_subplot(311)
    previousY = 0
    for line in lines:
        w = 0
        h = 0
        if(line[2] == '0.0' and line[3] == '0.0'):
            text = " "+iApp[line[0]]+"\n insufficient pow"
        else:
            w = float(line[2])
            h = float(line[4])
            add_rectangle(ax, x, y, w, h)
            text = " "+iApp[line[0]]+"\n "+iConfig[line[1]]
     
        #plt.plot([0,xmax],[y,y], '0.75') #draw horizontal line to indicate power per task
        add_label(ax, text, xmax, y, font)
        previousY = h
        y+=previousY 
        
    #plt.plot([0,xmax],[ymax,ymax], 'r')
    ax.axhline(y = ymax, c = 'r', linewidth=1, zorder=5)       
    f.close()
    return ax

  

def display(dirN, dirD, dirR, powerCap, numTasks):
    fig = init_figure()
    file = str(powerCap)+"-"+str(numTasks)
    ax = dsplyN(os.path.join(dirN, file), fig, powerCap, 3, 1, 1)
    dsply(os.path.join(dirD, file), fig, powerCap, 3, 1, 2, ax)
    dsply(os.path.join(dirR, file), fig, powerCap, 3, 1, 3, ax)
    save_figure(fig, file)
    

for numTasks in range(1,27):
    for powerCap in range(100, 6600, 100):
        
        display(directoryN, directoryD, directoryR, powerCap, numTasks)