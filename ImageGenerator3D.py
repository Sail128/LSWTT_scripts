import os
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
from PIL import Image

def averageDirFiles(dirname):
    #print(dirname)
    files = os.listdir(dirname)
    
    filedata = np.genfromtxt("{}/{}".format(dirname,files[0]),delimiter=";")
    #print(filedata.shape)
    filedata = np.delete(filedata, -1, 1)
    # img = Image.fromarray(np.uint8(filedata*4),"L")
    # img.show()
    averageFile = np.empty((filedata.shape[0],filedata.shape[1], len(files)))
    # print(averageFile.shape)
    for i in range(len(files)):
        csv = files[i]
        filedata = np.genfromtxt("{}/{}".format(dirname,csv),delimiter=";")
        filedata = np.delete(filedata, -1, 1)
        #print(avergeddata)
        averageFile[:,:,i] = filedata
    #print(AverageData)
    #print(averageFile.shape)
    averageFile = np.average(averageFile, axis=2)
    #print(averageFile.shape)

    if "2D" in dirname.split("\\")[1]:
        experiment = "2D"
    else: 
        experiment = "3D"
    filename = "Results\\{}\\{}_img.png".format(experiment,"\\".join(dirname.split("\\")[2:]))
    print("saving file: {} from dir: {}".format(filename, dirname))
    #np.savetxt(filename, averageFile, delimiter=";") 
    
    #averageFile = np.log2(averageFile)
    #print(averageFile)
    xmax, xmin = np.amax(averageFile), np.amin(averageFile)
    print(xmax,xmin)
    #print(xmax, xmin)
    averageFile = (averageFile - xmin)/(xmax - xmin)
    # averageFile*=
    # averageFile +=1
    # averageFile = np.log(averageFile)
    #print(averageFile)
    xmax, xmin = np.amax(averageFile), np.amin(averageFile)
    print(xmax,xmin)
    img = Image.fromarray(np.uint8(averageFile*255),"L")
    img.save(filename)
    #img.show()
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

    resultFileList = averageDirFiles(dirlist[14])
    #resultFileList = executeParallel(dirlist)
    print(len(resultFileList))
    print(resultFileList)
    print("Finished image generating job")
    #input("press enter to exit ...")

if __name__ == "__main__":
    main()