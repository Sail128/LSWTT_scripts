import matplotlib.pyplot as plt
import numpy as np

def general_plotter(
    plots, 
    title:str=None,
    xlabel:str=None,
    xlim:tuple=None,
    xinvert:bool=False,
    ylabel:str=None,
    ylim:tuple=None,
    yinvert:bool=False,
    grid:bool=False,
    legend=False, 
    fname:str=None, 
    show:bool=True
    ):
    """This function is a general plotting function.
    It sets up a plot with the given parameters.
    Compress plot setup down to one function. for more varies option use pyplot by itself

    Arguments:
        plots {list of tuples} -- [(xs,ys,label,(marker))]
    
    Keyword Arguments:
        title {str} -- title displayed above the plot (default: {None})
        xlabel {str} -- label of the x-axis (default: {None})
        xlim {tuple} -- the limit of the x-axis (default: {None})
        xinvert {bool} -- invert the x-axis (default: {False})
        ylabel {str} -- label of the y-axis(default: {None})
        ylim {tuple} -- the limit of the y-axis (default: {None})
        yinvert {bool} -- invert the y-axis (default: {False})
        grid {bool} -- turns on or off the grid (default: {False})
        legend {bool or int} -- turns on the legend if passed a value. An int maybe passed for locating the legend. This is the same as pyplot (default: {False})
        fname {str} -- filename to save an image of the plot. If passed it will try to save the file with that filename (default: {None})
        show {bool} -- Show the plot in it's own window. Set false if executing in seperate threads (default: {True})
    """
    for plot in plots:
        if len(plot) == 4:
            xs,ys,label,marker = plot
        else:
            xs,ys,label = plot
            marker="None"
        plt.plot(xs,ys,label=label,marker=marker)
    if title!=None:
        plt.title(title)
    if xlabel !=None:
        plt.xlabel(xlabel)
    if xlim!=None:
        plt.xlim(xlim)
    if xinvert:
        plt.gca().invert_xaxis()
    if ylabel!=None:
        plt.ylabel(ylabel)
    if ylim != None:
        plt.ylim(ylim)
    if yinvert:
        plt.gca().invert_yaxis()
    if grid:
        plt.grid()
    #setup legend
    if type(legend)==int:
        plt.legend(loc=legend)
    else:
        if legend:
            plt.legend(loc=0) 
    #save the figure with fname
    if fname!=None: 
        plt.savefig(fname)
    else:
        if not show:
            print("Why do you want to create a graph that you don't save or show.\nThis is utterly useless")
    if show: 
        plt.show()
    plt.close()


def plot_Cl_alpha(test_as, test_cls, calc_as, calc_cls, Re):
    plt.plot(test_as, test_cls,label="experimental",marker="^")
    plt.plot(calc_as, calc_cls,label="XFOIL prediction",marker=".")
    plt.title("Cl vs alpha for Re: {:.2e}".format(Re))
    plt.xlabel("alpha [deg]")
    plt.ylabel("Cl")
    plt.legend(loc=4)
    plt.grid()
    plt.savefig("Cl_alpha_2D.png")
    #plt.show()
    plt.close()

def plot_Cl_alpha_general(test_as, test_cls, label1, calc_as, calc_cls, label2, title, fname="Cl_alpha_xfoil_2D.png"):
    plt.plot(test_as, test_cls,label=label1,marker="^")
    plt.plot(calc_as, calc_cls,label=label2,marker=".")
    plt.title(title)
    plt.xlabel("alpha [deg]")
    plt.ylabel("Cl")
    plt.legend(loc=4)
    plt.grid()
    plt.savefig(fname)
    #plt.show()
    plt.close()

def plot_Cm_alpha(test_as, test_cms, calc_as, calc_cms, Re):
    plt.plot(test_as, test_cms,label="experimental",marker="^")
    plt.plot(calc_as, calc_cms,label="XFOIL prediction",marker=".")
    plt.title("Cm vs alpha for Re: {:.2e}".format(Re))
    plt.xlabel("alpha [deg]")
    plt.ylabel("Cm")
    plt.legend(loc=4)
    plt.grid()
    plt.savefig("Cm_alpha_2D.png")
    #plt.show()
    plt.close()

def plot_Cd_Cl(test_cds,test_cls,calc_cds, calc_cls, Re):
    plt.plot(test_cds, test_cls,label="experimental",marker="^")
    plt.plot(calc_cds, calc_cls,label="XFOIL prediction",marker=".")
    plt.title("Cl vs Cd for Re: {:.2e}".format(Re))
    plt.xlabel("Cd")
    plt.ylabel("Cl")
    plt.legend(loc=4)
    plt.grid()
    plt.savefig("Cl_Cd_2D.png")
    #plt.show()
    plt.close()


def main():
    testData = np.genfromtxt("Group32_2D_05-12-2018\\corr_test.txt")
    visc_10 = np.genfromtxt("visc_1000000.txt")
    visc_5 = np.genfromtxt("visc_500000.txt")
    invisc_10 = np.genfromtxt("invisc_1000000.txt")
    invisc_5 = np.genfromtxt("invisc_500000.txt")
    test_as = testData[2:,1]
    calc_as = visc_10[2:,0]
    calc_as10 = visc_5[2:,0]
    Re = np.average(testData[2:,9])
    Re1 = 1000000
    Re2=500000
    print(Re)
    plot_Cl_alpha(test_as[:27],testData[2:,3][:27], visc_10[2:,0], visc_10[2:,1] , Re)
    plot_Cm_alpha(test_as[:27],testData[2:,4][:27], visc_10[2:,0], visc_10[2:,4] , Re)
    plot_Cd_Cl(testData[2:,2][:27],testData[2:,3][:27], visc_10[2:,2], visc_10[2:,1] , Re)
    plot_Cl_alpha_general(
        visc_10[2:,0], visc_10[2:,1], "Re= {:.2e}".format(Re1), 
        visc_5[2:,0], visc_5[2:,1], "Re= {:.2e}".format(Re2),
        "predicted Cl vs alpha for Re={:.2e} and {:.2e}".format(Re1,Re2))

    plot_Cl_alpha_general(
        invisc_10[2:,0],invisc_10[2:,1],"inviscid Re= {:.2e}".format(Re1),
        visc_10[2:,0], visc_10[2:,1], "viscid Re= {:.2e}".format(Re1),
        "viscid vs inviscid simulation Cl-alpha",
        fname="Cl_alpha_vsic_invisc_2D.png"
    )


if __name__ == "__main__":
    main()