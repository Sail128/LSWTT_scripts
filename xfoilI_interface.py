import subprocess as sp
from os import walk
from numpy import arange
import grapher
from time import sleep


def xfoilProcess(infile, alfas=[0.0], output="Polar", iterr=9, Re=1000000, Mach=0.0, cpalfa=0.0):
    # setup log files for output
    logfile = open("log_{}.log".format(infile.split(".")[0]), "w")
    errorlogfile = open("log_{}.errorlog".format(infile.split(".")[0]), "w")

    startupinfo = sp.STARTUPINFO()
    startupinfo.dwFlags |= sp.STARTF_USESHOWWINDOW
    ps = sp.Popen(['xfoil.exe'],
                  stdin=sp.PIPE,
                  stdout=logfile,
                  stderr=errorlogfile,
                  startupinfo=startupinfo,
                  encoding='utf8'
                  )

    def command(cmd):
        print(cmd)
        ps.stdin.write(cmd+'\n')
        #psout = []
        # while True:
        #    line = ps.stdout.readline()
        #    psout.append(line)
        #    print(line)
        #    if line == '' and ps.poll() != None:
        #        break
        # print(''.join(psout))

    command("NORM")
    command("LOAD {}".format(infile))
    command("MDES")  # open airfoil design
    command("FILT")  # smooth variations in the airfoil file
    command("EXEC")  # execute smoothing
    command("")  # get back to main menu
    command("PANE")  # generate airfoil panels for calculations
    command("OPER")  # open operations
    command("ITER {}".format(iterr))  # set number of itterations
    command("Re {}".format(Re))  # set reynolds
    command("Mach {}".format(Mach))  # set mach
    #command("VISC {}".format(Re))  # set viscous
    # setup finished
    # calculate polar or cp
    if output == "Polar":
        command("PACC")  # open polar file
        # give the file a name
        command("Polar_{}_{}_{}.txt".format(infile.split(".")[0], Re, Mach))
        command("")  # skip dumpfile
        for alfa in alfas:
            sleep(0.01)
            # command("INIT")
            command("ALFA {}".format(alfa))
    if output == "Cp":
        #command("INIT")
        command("ALFA {}".format(cpalfa))
        command("CPWR Cp\\Cp_{}_{}.txt".format(infile.split(".")[0],cpalfa))
    else:
        pass

    command("PACC")  # close polar file
    #command("VISC")  # reset environment
    command("")  # exit to main menu
    command("QUIT")  # quit the program

    # ps.terminate()

    logfile.close()
    errorlogfile.close()


def generatePolarFiles():
    alfas = arange(-2.0, 18.5, 0.25).tolist()
    xfoilProcess("airfoil.dat", alfas=alfas, output="Polar", cpalfa=1.0, Mach=0.185, Re=500000)
    # for a in alfas:
    #     xfoilProcess("airfoil.dat", alfas=alfas, output="Cp", cpalfa=a, Mach=0.185)


def main():
    generatePolarFiles()
    #grapher.GeneratePolars(files=["Polar_airfoil.dat_1000000_0.185"])
    #f= "K-3_BL576_int06.dat"
    #alfas = arange(-10.0, 20.0, 0.25).tolist()
    #xfoilProcess("airfoils/{}".format(f), Re=10000000 ,alfas=alfas, output="Polar", cpalfa=0.0)


if __name__ == '__main__':
    main()
