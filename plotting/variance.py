import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import re
import sys, os
import numpy as np

long_taps = np.array([1, 0.1, -1.87, 3.02, -1.435, 0.49])


def percentage (m):
    return np.sqrt(m[1::2,:])/ np.absolute(m[0::2,:])


def calculte(filename):
    finder = re.compile("\[|-?\d+\.\d*[eE]?[-+]?\d*|\]")
    result = []
    temp = []
    with open(os.path.join(os.path.dirname(__file__), filename)) as datafile:
        for row in datafile:
            hit = finder.findall(row)
            if "[" in hit:
                hit.remove("[")
                temp = hit
                if "]" in hit:
                    temp.remove("]")
                    result.append(map(lambda x: float(x), temp))
            elif "]" in hit:
                hit.remove("]")
                temp += hit
                result.append(map(lambda x: float(x), temp))
            else:
                temp += hit

    #return percentage(np.array(result))
    return np.array(result)

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(int(100 * y))

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

def plottingcx5(m, filename):
    xlen = range(len(m))
    plt.plot(xlen, m[:,0], "-.", label=r'$C_{3y}(-2,0)$')
    plt.plot(xlen, m[:,1], "--", label=r'$C_{3y}(-1,0)$')
    plt.plot(xlen, m[:,2], "-", label=r'$C_{3y}(0,0)$')
    plt.plot(xlen, m[:,3], ":", label=r'$C_{3y}(1,0)$')
    plt.plot(xlen, m[:,4], "o", label=r'$C_{3y}(2,0)$')
    
    plt.ylim((0,1))
    plt.xlabel(r"Length of signal $(10^4)$")
    plt.ylabel("Proportion of standard deviation and expectation")
    formatter = FuncFormatter(to_percent)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.legend(loc=0, ncol=2)
    plt.savefig(filename, fmt='pdf')

def plottingcx11(m, filename):
    xlen = range(len(m))
    ax = plt.gca()
    plt.plot(xlen, m[:,0], ":", label=r'$C_{3y}(-5,0)$')
    plt.plot(xlen, m[:,1], "--", label=r'$C_{3y}(-4,0)$')
    plt.plot(xlen, m[:,2], "-.", label=r'$C_{3y}(-3,0)$')
    plt.plot(xlen, m[:,3], "o", label=r'$C_{3y}(-2,0)$')
    plt.plot(xlen, m[:,4], "^", label=r'$C_{3y}(-1,0)$')
    plt.plot(xlen, m[:,5], "-", label=r'$C_{3y}(0,0)$')
    plt.plot(xlen, m[:,6], "<", label=r'$C_{3y}(1,0)$')
    plt.plot(xlen, m[:,7], ">", label=r'$C_{3y}(2,0)$')
    plt.plot(xlen, m[:,8], "s", label=r'$C_{3y}(3,0)$')
    plt.plot(xlen, m[:,9], "p", label=r'$C_{3y}(4,0)$')
    plt.plot(xlen, m[:,10], "*", label=r'$C_{3y}(5,0)$')

    plt.ylim((0,1.5))
    plt.xlabel(r"Length of signal $(10^4)$")
    plt.ylabel("Proportion of standard deviation and expectation")
    formatter = FuncFormatter(to_percent)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.legend(loc=0, ncol=2)
    plt.savefig(filename, fmt='pdf')
    plt.show()

def plotting_long(ma, filename):
    m = percentage(ma)
    xlen = range(len(m))
    ax = plt.gca()
    plt.plot(xlen, m[:,1], "-", label=r'$tap_1$')
    plt.plot(xlen, m[:,2], "--", label=r'$tap_2$')
    plt.plot(xlen, m[:,3], "o", label=r'$tap_3$')
    plt.plot(xlen, m[:,4], "^", label=r'$tap_4$')
    plt.plot(xlen, m[:,5], "-.", label=r'$tap_5$')

    plt.ylim((0,10))
    plt.xlabel(r"Length of signal $(10^4)$")
    plt.ylabel("Proportion of standard deviation and expectation")
    formatter = FuncFormatter(to_percent)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.legend(loc=0, ncol=2)
    plt.savefig(filename, fmt='pdf')
    plt.show()

def plotting_short(ma, filename):
    m = percentage(ma)
    xlen = range(len(m))
    ax = plt.gca()
    plt.plot(xlen, m[:,1], "-", label=r'$tap_1$')
    plt.plot(xlen, m[:,2], "--", label=r'$tap_2$')

    plt.ylim((0,7))
    plt.xlabel(r"Length of signal $(10^4)$")
    plt.ylabel("Proportion of standard deviation and expectation")
    formatter = FuncFormatter(to_percent)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.legend(loc=0, ncol=2)
    plt.savefig("convergence_ma4_short_cumulant_pcs1123.pdf", fmt='pdf')
    plt.show()


if __name__ == "__main__":
    filename = "convergence_cx3_long_cumulant_pcs123.txt"
    result = calculte(filename)

    filename = filename[:-4]
    matcher = re.compile("long|short|cx|ma")
    matched = matcher.findall(filename)
    if "long" in matched and "cx" in matched:
        plottingcx11(percentage(result), filename)
    elif "short" in matched and "cx" in matched:
        plottingcx5(percentage(result), filename)
    else:
        print "You might need to add more plotting functions..."



