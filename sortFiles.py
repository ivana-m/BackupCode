import os
from operator import itemgetter

appDir = r"D:\Documents\Academics\Project\Project\applications"

sortByColumn = 2
#for i in os.listdir(appDir):
i = 4
app = open(appDir+"/"+str(i),'r')
print(appDir+"/"+str(i))
appSorted = open(r"D:\Documents\Academics\Project\Project\project_data\applications_power_ordered"+"\\"+str(i), 'w')
lines = []
for line in app:
    line = line.strip()
    if(len(line) > 0):
        splitLine = []
        splitLine.append(int(line.split('\t')[0]))
        splitLine.append(float(line.split('\t')[1]))
        splitLine.append(float(line.split('\t')[2]))
        #print(splitLine)
        lines.append(splitLine)
lines.sort(key=itemgetter(sortByColumn))
buff=""
for el in lines:
    buff+=str(el[0])+"\t"+str(el[1])+"\t"+str(el[2])+"\n"
    #appSorted.write('{0}\n'.format(' '.join(el)))
print(buff)
appSorted.write(buff)
app.close()
appSorted.close()
    

