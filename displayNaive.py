import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

#location of all the output files to be drawn
directory = r"D:\Documents\Academics\Project\Project\outputFiles\naive"

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


def getLines(file):
    lines = []
    for line in file:
        line = line.strip()
        line = line.split('\t')
        if(len(line) == 4):
            lines.append(line)
    return lines


#find best and worst performance, and highest and lowest power consumed from all tasks
def get_boundaries(lines, powerCap):
    maxPerf = 1000000
    minPerf = -1
    maxPow = -1
    minPow = powerCap
    for l in lines:
        s = float(l[2])
        p = float(l[3])
        if(s <= maxPerf):
            maxPerf = s
        if(s >= minPerf):
            minPerf = s
        if(p >= maxPow):
            maxPow = p
        if(p <= minPow):
            minPow = p
    return maxPerf, minPerf, maxPow, minPow

def add_rectangle(ax, x, y, w, h):
    ax.add_patch(
        patches.Rectangle(
            (x,y), w, h,
            )
        )
     
def add_label(ax, text, x, y, fontsize):
    ax.text(x,y,text,fontsize=fontsize)

def draw(xmax, ymax, fileName, ax, plt, fig):
    plt.axis((0,xmax,0,ymax))
    plt.show()
    fig.savefig(fileName+'.png', dpi='figure', bbox_inches='tight')

def main(directory):
    #these are needed for correct labeling
    iConfig = get_configIndex_mapping(r"D:\Documents\Academics\Project\Project\project_data\config_index.txt")
    iApp = get_appIndex_mapping(r"D:\Documents\Academics\Project\Project\project_data\applicationsByIndex.txt")    
    font = 12 #fontsize for the labels
    
    for (subdir, dirs, files) in os.walk(directory):
        for file in files:
            print(file)
            powerCap = float(file.split('-')[0])
            if(powerCap != 1100.0):
                break
            numApps = float(file.split('-')[1])
            offset = powerCap/numApps#1/numApps #this only works for naive
            f = open(os.path.join(subdir, file), 'r')
            lines = getLines(f)
            if(len(lines) == 0):
                print("no results for "+file)
                continue
            maxPerf, minPerf, maxPow, minPow = get_boundaries(lines, powerCap)
            xmax = minPerf #largest x is determined by the slowest, or least performing task
            ymax = powerCap
            x = 0
            y = 0
            fig = plt.figure(figsize=(17,15),dpi=60) #values obtained by handtweaking, but might be subject to change. size works well for 26 applications at once. For a smaller image, just remove the arguments: plt.figure()
            ax = fig.add_subplot(111)
            for line in lines:
                w = 0
                if(line[2] == '0' and line[3] == '0'):
                    text = " "+iApp[line[0]]+"\n insufficient pow"
                else:
                    w = norm(float(line[2]),maxPerf,minPerf)
                    h = norm(float(line[3]),0,powerCap)
                    add_rectangle(ax, x, y, w, h)
                    text = " "+iApp[line[0]]+"\n "+iConfig[line[1]]
             
                plt.plot([0,xmax],[y,y], '0.75') #draw horizontal line to indicate power per task
                add_label(ax, text, x+w, y, font)
                
                y+=offset #TODO y will be updated differently depending on algorithm 
            draw(xmax, powerCap, file, ax, plt, fig)        
            f.close()
    return 

def norm(pt, min, max):
    return pt
    #return (pt - min)/(max-min)
    
main(directory)