import os
import numpy as np
import matplotlib.pyplot as plt

def genGraph(filename):
    Tdata = np.genfromtxt(filename)
    Tdata = np.flip(Tdata,0)
    Tdata_thres = Tdata[Tdata>=22.0]
    if len(Tdata_thres)<=100:
        Tdata_thres = Tdata[Tdata>=19.0]
    xs = np.arange(0.0,1.0000000, 1/len(Tdata_thres))
    xs = xs[:len(Tdata_thres)]
    plt.plot(xs, Tdata_thres)
    plt.xlim(0.0,1.0)
    plt.grid()
    plt.xlabel("x/c")
    plt.ylabel("T [C]")
    plt.title("T over the chord for angle: {}".format(filename.split("\\")[-1][1:-4]))
    # plt.show()
    plt.savefig("{}_graph.png".format(filename[:-4]))
    plt.close()

def main():
    fs = []
    for root, dirs, files in os.walk("Results\\2D\\Up"):
        files = list(filter(lambda x: x.endswith(".csv"), files))
        fs.extend([root+ "\\"+ f for f in files])
    for f in fs:
        genGraph(f)
    # genGraph(fs[2])
    print("finished")

if __name__ == "__main__":
    main()