import numpy as np
import matplotlib.pyplot as plt

def genCpGraph(xs, ys, AoA, Re):
    xs_u, xs_b = xs[:int(len(xs)/2+1)], xs[int(len(xs)/2+1):]
    ys_u, ys_b = ys[:int(len(ys)/2+1)], ys[int(len(ys)/2+1):]

    plt.plot(xs, ys)
    plt.plot(xs_u, ys_u, label="upper")
    plt.plot(xs_b, ys_b, label="bottom")
    plt.rc('text',usetex=True)
    plt.title("$C_p$ distribution for Re={:.2e}, $\\alpha$={:.3}".format(Re, AoA))
    plt.xlabel("$x/c$")
    plt.ylabel("$C_p$")
    plt.legend()
    plt.gca().invert_yaxis()
    plt.grid()
    #plt.show()
    plt.savefig("Cp_graphs\\Cp_{:.3}_{:.2e}.png".format(AoA,Re))
    plt.close()
    tosave = np.append(np.expand_dims(xs,axis=0),[ys], axis=0).transpose()
    print(tosave.shape)
    np.savetxt("Cp_graphs\\Cp_{:.3}_{:.2e}.txt".format(AoA,Re),tosave)

def main():
    cpData = np.genfromtxt("Group32_2D_05-12-2018\\cp_test.txt")#input the relative path of the cp_test file
    length = np.size(cpData,1)
    xs = cpData[2:,0]
    xs = xs/100

    xs_u = xs[0:int(len(xs)/2)+1]
    xs_l = xs[int(len(xs)/2)+1:]
    
    #print(xs[0:int(48/2)+1])
    for i in range(1, cpData.shape[1]):
        ys = cpData[2:,i]
        AoA = cpData[1,i]
        Re = cpData[0,i]
        genCpGraph(xs,ys,AoA, Re)
        



if __name__ == "__main__":
    main()