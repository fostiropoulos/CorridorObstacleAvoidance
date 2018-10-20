from scipy import interpolate
from scipy import signal
from scipy.signal import find_peaks
import numpy as np
import peakutils
import sys
import warnings
warnings.simplefilter("ignore")

class find_clearance:
    """
    Finds the roots with the polynomial for each y intercept.

    @yToFind y-intercept
    @y y values for the polynomial
    @x x values for the polynomial
    """
    @staticmethod
    def findYIntercepts(yToFind, y,x):
        yreduced = np.array(y) - yToFind
        freduced = interpolate.UnivariateSpline(x, yreduced, s=0)
        return freduced.roots()
    """
    Sums the width of every pair of points

    @points the list of points of the y intercept with the binomial for which to calculate their gap.

    """
    @staticmethod
    def sumPointPairWidths(points):
        # Need at least 2 binomials or 4 points to compare their clearance
        assert len(points)>=4
        widthSum=0

        points=points[1:]
        points=points[:-1]
        for pointTuple in zip(points[::2], points[1::2]):
            widthSum+=(pointTuple[1]-pointTuple[0])
        return widthSum
    """
    Checks if a peak array is inside a potential solution space

    @points list that is even numbered and contains the intercepting pairs of y with the binomials
    @peaks the list of peak points for each binomial. maxima for that binomial
    """
    @staticmethod
    def isPeakInWidthPair(points, peaks):
        assert len(points)%2==0
        assert len(points)/2==len(peaks)

        #peaks are ordered and points to map them 1 to 1
        points=sorted(points)
        peaks=sorted(peaks)
        for idx,pointTuple in enumerate(zip(points[::2], points[1::2])):
            if not (peaks[idx]>pointTuple[0] and pointTuple[1]>peaks[idx]):
                return False
        return True


    """
    Avoid using signal to calculate clearance distance because the distance of the person is already off from what was described.
    Hence I pre-calculate it, less robust but can expand for a generic scenario

    @x number of pixels to an estimation of distance for the clearance problem ONLY
    """
    @staticmethod
    def calculatePerspectiveDistance(x):
        coeff=0.02272727272
        return coeff*x
    """
    Given the path of an image, print the clearance and to left or right side.

    @img path to the image file
    """
    @staticmethod
    def calculate(img):
        data=np.loadtxt(img)

        humanMaxDistance=4
        humanMinDistance=3
        tmp=(data>humanMinDistance)
        tmp1=(data<humanMaxDistance)
        dataContrasted=np.logical_and(tmp,tmp1).astype(int)

        #Convert to a signal for easier processing
        x=dataContrasted.sum(axis=0)[:]
        #Find peaks of the signal
        peaks, _ = find_peaks(x)

        xFiltered=signal.savgol_filter(x, 19, 4)
        cb = np.array(xFiltered)

        indexes = peakutils.indexes(cb, thres=0.02/max(cb), min_dist=10)
        try:
            peaks=sorted(zip(xFiltered[indexes],indexes),key=lambda a : a[0], reverse=True)[:3]
        except:
            print("Obstacle could not be detected. Human either too close to the wall, or at a different distance than the one specified.")
            return;
        # peaks of filtered signal
        peaks = [xFiltered[1] for xFiltered in peaks]




        # Store the problem space solutions
        widthSums=[]
        # Search for all Y-intercepts to find the ones that belong to the problem space (e.g. the ones that consider left wall, human and right wall)
        #left and right wall
        walls=2
        #one obstacle the human
        obstacle=1
        # Binomial from the signal interpolate since objects are considered infentely tall and 2d from bird's eye perspective
        polynomial=2
        for i in np.linspace(0,len(x),len(x)):
            #find intercepts on the original signal for higher accuracy
            intercepts=find_clearance.findYIntercepts(i,x,range(0,len(x)))
            # Try to reduce problem space by only checking the intercepts for which there is a binomial for each obstacle
            # Check if the peak belongs to the problem space.
            if(len(intercepts)==(walls*polynomial+obstacle*polynomial) and find_clearance.isPeakInWidthPair(intercepts, peaks) ):
                widthSums.append({"sum":find_clearance.sumPointPairWidths(intercepts),"y":i,"x":intercepts})

        #get the intercept from the problem space that minimizes the clearance (Worst case scenario for clearance)
        if(len(widthSums)==0):
            print("Obstacles detected but probably not wall-human-wall or human is not in the right distance.")
            return
        intercepts=sorted(widthSums,key=lambda a : a["sum"], )[:1][0]["x"]


        # D1 is difference between where the human starts and the left wall ends
        d1=find_clearance.calculatePerspectiveDistance(intercepts[2]-intercepts[1])

        # D2 is difference between where the human ends and the left wall starts
        d2=find_clearance.calculatePerspectiveDistance(intercepts[4]-intercepts[3])

        if(d1>d2):
            print("left %fm"%d1)
        else:
            print("right %fm"%d2)
if __name__ == "__main__":
    if(len(sys.argv)<2):
        print("Not enough arguments")
    else:
        find_clearance.calculate(sys.argv[1])
