
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt

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
    show:bool=True,
    usetex:bool=True
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
        usetex {bool} -- use latex to format all text (default: {True})
    """
    plt.rc('text', usetex=usetex)
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

def getSlopeInterval(xs:list,ys:list,x_start=None, x_stop=None, interval:tuple=None):
    """returns the slope of an interval of the given data set
    
    Arguments:
        xs {list} -- list of x coordinates. Assumed to be ordered
        ys {list} -- list of y coordinates. Assumed to be ordered
    
    Keyword Arguments:
        x_start {float} -- x_value from which to start. If not defined will start at beginning of lists (default: {None})
        x_stop {float} -- x_value at which to stop. If not defined will continue until end of lists (default: {None})
        interval {tuple} -- tuple (x_start,x_stop)
    
    Returns:
        [tuple] -- tuple in the form: slope, intercept, R, P, std_err
    """

    maxindex = len(xs)
    if maxindex!=len(ys):
        print("Non equal list given")
        return 0
    if interval!=None:
        x_start,x_stop = interval

    i_start = 0
    i_stop = 0
    if x_start==None:
        x_start = -float("inf")
    if x_stop==None:
        x_stop = float("inf")
        i_stop = maxindex

    for i in range(maxindex):
        if xs[i]<x_start:
            i_start=i
        if xs[i]<x_stop:
            i_stop=i
    i_start+=1
    return stats.linregress(xs[i_start:i_stop],ys[i_start:i_stop])

def dualSlopeAnalyzer(xs:list,ys:list, x_transition:float=None, x_end:float=None,interval1:tuple=None, interval2:tuple=None):
    """analyzer for a dual sloped lift curve
        if x_transition is defined than interval will be ignored. x_end is used if defined, otherwise x_end is assumed end of dataset
        Alternatively two intervals can be defined aswell. but those can't be mixed.
    Arguments:
        xs {list} -- list of x coordinates. Assumed to be ordered
        ys {list} -- list of y coordinates. Assumed to be ordered
    
    Keyword Arguments:
        x_transition {float} -- point of transtion (default: {None})
        x_end {float} -- point to end measuring (default: {None})
        interval1 {tuple} -- (x1,x2) (default: {None})
        interval2 {tuple} -- (x3,x4) (default: {None})

    Returns:
        [tuple] -- (line1, line2) 
    """
    line1 =()
    line2=()
    if x_transition!=None:
        line1=getSlopeInterval(xs,ys,x_stop=x_transition)
        line2 = getSlopeInterval(xs,ys,x_start=x_transition,x_stop=x_end)
    else:
        if interval1!=None and interval2!=None:
            line1 = getSlopeInterval(xs,ys,interval=interval1)
            line1 = getSlopeInterval(xs,ys,interval=interval2)
        else:
            print("insufficient arguments were passed")
    return (line1,line2)

def linedataTostring(line:tuple, perRad:bool=True):
    """converts a tuple from a linear regression to a csv string
    
    Arguments:
        line {tuple} -- tuple returned from scipy.stats.linregress
    Returns:
        [str] -- csv string of a linregress line: (slope, intercept, R^2)
    """
    slope, intercept, R, P, std_err = line
    return "{},{},{}".format(slope*180/sp.pi if perRad else slope, intercept, R**2)

def main():
    visc_10 = sp.genfromtxt("visc_1000000.txt")#alpha, CL, CD, CDp, CM
    visc_5 = sp.genfromtxt("visc_500000.txt")#alpha, CL, CD, CDp, CM
    invisc_10 = sp.genfromtxt("invisc_1000000.txt")#alpha, CL, CD, CDp, CM
    invisc_5 = sp.genfromtxt("invisc_500000.txt")#alpha, CL, CD, CDp, CM
    testData = sp.genfromtxt("Group32_2D_05-12-2018\\corr_test.txt")#runNR,alpha,Cd,Cl,Cm,Cn,Ct,CDp,Clp,Re

    #Plotting Cl-alpha simulation for varying Re
    general_plotter(
        [
            (visc_10[2:,0], visc_10[2:,1], "viscid Re=1e6 M=0.185", "."),
            (visc_5[2:,0], visc_5[2:,1], "viscid Re=5e5 M=0.185", "s")
        ],
        title="$C_l-\\alpha$ viscous simulation for varying Re",
        legend=4,
        grid=True,
        xlabel="$\\alpha[\\deg]$",
        ylabel="$C_l$",
        fname="2D_Cl-alpha_sim.png",
        show=False
    )
    #Plotting Cl-alpha viscid and inviscid simulation
    general_plotter(
        [
            (visc_10[2:,0], visc_10[2:,1], "viscid Re=1e6 M=0.185", "."),
            (invisc_10[2:,0], invisc_10[2:,1], "inviscid Re=1e6 M=0.185", "s")
        ],
        title="$C_l-\\alpha$  for viscid and inviscid simulation",
        legend=4,
        grid=True,
        xlabel="$\\alpha[\\deg]$",
        ylabel="$C_l$",
        fname="2D_Cl-alpha_visc.png",
        show=False
    )
    #Plotting Cl-alpha simulation and test results for varying Re
    general_plotter(
        [
            (visc_10[2:,0], visc_10[2:,1], "viscid Re=1e6 M=0.185", "."),
            (visc_5[2:,0], visc_5[2:,1], "viscid Re=5e5 M=0.185", "s"),
            (testData[2:28,1], testData[2:28,3],"experiment Re$\\approx${:.2e}".format(sp.average(testData[2:,9])),"^")
        ],
        title="$C_l-\\alpha$  viscous simulation and experiment",
        legend=4,
        grid=True,
        xlabel="$\\alpha[\\deg]$",
        ylabel="$C_l$",
        fname="2D_Cl-alpha_sim-test.png",
        show=False
    )
    #Plotting Cl-alpha test results
    general_plotter(
        [
            (testData[2:,1], testData[2:,3],"experiment Re$\\approx${:.2e}".format(sp.average(testData[2:,9])),"^")
        ],
        title="$C_l-\\alpha$  experimental data",
        legend=4,
        grid=True,
        xlabel="$\\alpha[\\deg]$",
        ylabel="$C_l$",
        fname="2D_Cl-alpha_test.png",
        show=False
    )
    #Plotting Cl-alpha test results Hysteris
    general_plotter(
        [
            (testData[2:,1], testData[2:,3],"experiment Re$\\approx${:.2e}".format(sp.average(testData[2:,9])),"^")
        ],
        title="$C_l-\\alpha$  Hysteresis",
        legend=0,
        grid=True,
        xlabel="$\\alpha[\\deg]$",
        ylabel="$C_l$",
        fname="2D_Cl-alpha_hyst.png",
        show=False
    )
    #Plotting Cd-alpha simulation and test results for varying Re
    general_plotter(
        [
            (visc_10[2:,0], visc_10[2:,2], "viscid Re=1e6 M=0.185", "."),
            (visc_5[2:,0], visc_5[2:,2], "viscid Re=5e5 M=0.185", "s"),
            (testData[2:28,1], testData[2:28,2],"experiment Re$\\approx${:.2e}".format(sp.average(testData[2:,9])),"^")
        ],
        title="$C_d-\\alpha$ viscous simulation and experiment",
        legend=0,
        grid=True,
        xlabel="$\\alpha[\\deg]$",
        ylabel="$C_d$",
        fname="2D_Cd-alpha.png",
        show=False
    )
    #Plotting Cm-alpha simulation and test results for varying Re
    general_plotter(
        [
            (visc_10[2:,0], visc_10[2:,4], "viscid Re=1e6 M=0.185", "."),
            (visc_5[2:,0], visc_5[2:,4], "viscid Re=5e5 M=0.185", "s"),
            (testData[2:28,1], testData[2:28,4],"experiment Re$\\approx${:.2e}".format(sp.average(testData[2:,9])),"^")
        ],
        title="$C_m-\\alpha$ viscous simulation and experiment",
        legend=0,
        grid=True,
        xlabel="$\\alpha[\\deg]$",
        ylabel="$C_m$",
        fname="2D_Cm-alpha.png",
        show=False
    )
    #Plotting Cd-Cl simulation and test results for varying Re
    general_plotter(
        [
            (visc_10[2:,2], visc_10[2:,1], "viscid Re=1e6 M=0.185", "."),
            (visc_5[2:,2], visc_5[2:,1], "viscid Re=5e5 M=0.185", "s"),
            (testData[2:28,2], testData[2:28,3],"experiment Re$\\approx${:.2e}".format(sp.average(testData[2:,9])),"^")
        ],
        title="$C_l-C_d$  viscous simulation and experiment",
        legend=4,
        grid=True,
        xlabel="$C_d$",
        ylabel="$C_l$",
        fname="2D_Cl-Cd.png",
        show=False
    )


    l1_test,l2_test = dualSlopeAnalyzer(testData[2:,1], testData[2:,3], x_transition=4.8,x_end=9.0)
    l1_visc10, l2_visc10 = dualSlopeAnalyzer(visc_10[2:,0], visc_10[2:,1], x_transition=4.8,x_end=9.0)
    l1_visc5, l2_visc5 = dualSlopeAnalyzer(visc_5[2:,0], visc_5[2:,1], x_transition=4.8,x_end=9.0)
    l_invisc10 = getSlopeInterval(visc_10[2:,0],visc_10[2:,1],x_stop=9.0)
    l_invisc5 = getSlopeInterval(visc_5[2:,0],visc_5[2:,1],x_stop=9.0)
    outstr = []
    outstr.append("Data Analysis")
    outstr.append("testdata")
    outstr.append("interval,slope,intercept,R^2")
    outstr.append("(-2;4.8),{}".format(linedataTostring(l1_test)))
    outstr.append("(4.8;9),{}".format(linedataTostring(l2_test)))
    outstr.append("viscous Re=1000000")
    outstr.append("interval,slope,intercept,R^2")
    outstr.append("(-2;4.8),{}".format(linedataTostring(l1_visc10)))
    outstr.append("(4.8;9),{}".format(linedataTostring(l2_visc10)))
    outstr.append("viscous Re=500000")
    outstr.append("interval,slope,intercept,R^2")
    outstr.append("(-2;4.8),{}".format(linedataTostring(l1_visc5)))
    outstr.append("(4.8;9),{}".format(linedataTostring(l2_visc5)))
    outstr.append("inviscid Re=1000000")
    outstr.append("interval,slope,intercept,R^2")
    outstr.append("(0;9),{}".format(linedataTostring(l_invisc10)))
    outstr.append("inviscid Re=500000")
    outstr.append("interval,slope,intercept,R^2")
    outstr.append("(0;9),{}".format(linedataTostring(l_invisc5)))
    print("\n".join(outstr))

if __name__ == "__main__":
    main()