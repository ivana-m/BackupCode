import os
import io

rootdir = r"D:\Documents\Academics\Project\Project\mod_data"

outDirPath = "C:\\Users\\Ivana\\Documents\\Academics\\Grad\\proc_data"

powerColumn = 5

#fileList = ""
countFiles = 0

#outFileList = open("filesByIndex.txt", 'w')



for subdir, dirs, files in os.walk(rootdir):
    #if(len(subdir.split("\\")) > 1):
        #fileList += str(countFiles) + "\t" + subdir.split("\\")[1] + "\r\n"
    
    for file in files:
        outFileName = ""
        if(len(subdir.split("\\")) > 1):
            outFileName += subdir.split("\\")[1]
        outFile = open(r"D:\Documents\Academics\Project\Project\applications"+"\\"+str(countFiles-1), 'w')
        #outConfigFile = open('C:/Users/Ivana/Documents/Academics/Grad/config_index/'+"config_index_" + outFileName + ".txt", 'w')
        f = open(os.path.join(subdir, file), 'r')
        buff=""
        count = 0
        mappingBuff = ""
        #print(os.path.join(subdir,file))
        for l in f:
            l = l.strip()
            line = l.split()
            if(len(line) > 3):
                numCores = str(line[0])
                freq = str(line[1])
                memC = str(line[2])
                perf = str(line[3])
                energy = float(line[len(line)-1])
                p = 0.0
                if(len(line) > 7 or outFileName == "nn"):
                    power = str(line[powerColumn + 1])
                    p = float(line[powerColumn + 1])
                else:
                    power = str(line[powerColumn])
                    p = float(line[powerColumn])
                
                time = str(energy/p)
                mappingBuff+=str(count)+"\t"+numCores+"\t"+freq+"\t"+memC+"\n"
                buff+=str(count)+"\t"+perf+"\t"+power+"\t"+time+"\n"
                count+=1
        #outConfigFile.write(mappingBuff)
        #outConfigFile.close()
        outFile.write(buff)
        outFile.close()
    countFiles += 1    
#print(fileList)

#with open(os.path.join(outDirPath, outFileList), 'wb') as temp_file:
#outFileList.write(fileList)

#outFileList.close()