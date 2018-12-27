import os
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool

def averageDirFiles(dirname):
    files = os.listdir(dirname)
    
    fileaverges = []
    for csv in files:
        filedata = np.genfromtxt("{}/{}".format(dirname,csv),delimiter=";")
        avergeddata = np.average(filedata, axis=0)
        print(avergeddata.shape[0])
        avergeddata = avergeddata[~np.isnan(avergeddata)]
        #print(avergeddata)
        fileaverges.append(avergeddata)
    #print(AverageData)
    datapointaverage = np.average(np.array(fileaverges), axis=0)
    totalaverage = np.average(datapointaverage)
    datapointaverage = datapointaverage[datapointaverage>totalaverage]

    if "2D" in dirname.split("\\")[1]:
        experiment = "2D"
    else: 
        experiment = "3D"
    filename = "Results\\{}\\{}.csv".format(experiment,"\\".join(dirname.split("\\")[2:]))
    print("saving file: {} form dir: {}".format(filename, dirname))
    np.savetxt(filename, datapointaverage, delimiter=";")
    return filename

def executeParallel(dirnames, threads = 8):
    pool = ThreadPool(threads)
    result = pool.map(averageDirFiles,dirnames)
    pool.close()
    pool.join()
    return result

def main():
    dirlist = []
    for root, dirs, files in os.walk("."):
        for dirname in dirs:
            if "A" in dirname:
                dirlist.append("{}\\{}".format(root, dirname))
    print(len(dirlist))

    #resultFileList = averageDirFiles(dirlist[0])
    resultFileList = executeParallel(dirlist)
    print(len(resultFileList))
    print(resultFileList)
    print("Finished data averaging job")
    input("press key to exit ...")

if __name__ == "__main__":
    main()