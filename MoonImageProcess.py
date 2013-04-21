# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 16:26:33 2013

@author: Edmund
"""
import os
import pdb
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def main():
    """ Process moon images
    Call from commandline as: 
    /path/to/python /path/to/MoonImageProcesser.py lon0,lat0,lon1,lat1,sat1,sat2
    e.g.
    /path/to/python /path/to/MoonImageProcesser.py 1.2, 2.3,3.5,5.0,Apollo,Apollo14
    """
    scriptname,lon0,lat0,lon1,lat1,sat1,sat2=sys.argv[:] #Read some stuff in
    #For now, immediately overwrite with some dummy data
    scriptname,lon0,lat0,lon1,lat1,sat1,sat2="Yada.py","1.0","4.0","3.3","5.4","Apollo","Chandrayaan"
    origimagepath="C:\Users\Edmund\Desktop"
    saveimagepath="C:\Users\Edmund\Desktop"
    image1name="MoonPic.tif"
    image2name="MoonPicCrater.tif"
    image1outname="image1.png" #What the output files will be saved as
    image2outname="image2.png"
    histooutname="histo.png"
    #image2name="MoonPicCrater.tif")
    #image2name="MoonPicDarkerCrater.tif")
    image1Big=read_image(os.path.join(origimagepath,image1name))
    image2Big=read_image(os.path.join(origimagepath,image2name))
    
    #Insert code to cut down to size here
    image1=image1Big
    image2=image2Big
    
    plot_image(image1,os.path.join(saveimagepath,"image1.png"))
    plot_image(image2,os.path.join(saveimagepath,"image2.png"))
    #What are the differences?
    plot_image(image2-image1,os.path.join(saveimagepath,"image_subtract.png"),
               subtracting=True)
    
    #Do PDFs first: most important to get loaded earlu
    #Doing ylab & savestr separately as "#" not OK in saved figure's pathname!
    for normed,pdfraw_ylab,pdfraw_savestr in zip([1,0],
                                                 ["PDF","#"],
                                                 ["PDF","raw"]):
        n1, xbins, xbincenters=get_histo(image1,normed=normed)
        n2,dum,dum=get_histo(image2,normed=normed)
        #Comparison first: most important to get loaded early
        filey="histo_{}_compare.png".format(pdfraw_savestr)
        compare_histo(n1=n1,n2=n2,xbins=xbins,
                      ylab="{}, {} {}".format(sat1, sat2, pdfraw_ylab),
                      outfigpathfile=os.path.join(saveimagepath,filey))
        #Subtraction next: Also interesting
        filey="histo_{}_subtract.png".format(pdfraw_savestr)
        compare_histo(n1=n2-n1,xbins=xbins,comparetwo=False,#Don't want colours!
                      ylab="{} - {} {}".format(sat1,sat2, pdfraw_ylab),
                      outfigpathfile=os.path.join(saveimagepath,filey))
        #Individual sat histos next: Less interesting
        for sat,n1in,n2in,savenamey in zip([sat1,sat2],
                                            [n1,None],
                                            [None,n2],
                                            ["image1","image2"]): #Sat-agnostic names for save purposes
            filey="histo_{}_{}.png".format(pdfraw_savestr,savenamey)
            compare_histo(n1=n1in,n2=n2in,xbins=xbins,
                          ylab="{} {}".format(sat,pdfraw_ylab),
                          outfigpathfile=os.path.join(saveimagepath,filey))
    #pdb.set_trace()

def compare_histo(n1=None,n2=None,xbins=None,ylab="",comparetwo=True, outfigpathfile=None):
    if comparetwo: #If you're doing a comparison, want colours to identify source...
        n1col,n2col="r","b"
    else:#...Otherwise you want sth which is sat agnostic - e.g if you're passing in n1_new=n2-n1
        n1col,n2col="k","k"
    xleft=xbins[:-1]#Don't need right-most edge, as bin only needs left edge
    plt.figure()    
    for n,col in zip([n1,n2],[n1col,n2col]):
        if n is not None:
            plt.bar(xleft,n,width=1,color=col,edgecolor=col,alpha=0.5,linewidth=0)
    plt.xlim([0,255])
    yminny=plt.ylim() #Find the minimum y limit
    if yminny<0:
        plt.axhline(y=0,color="purple",ls=":") #Make it obvious where y=0 is
    plt.xlabel("Pixel value")
    plt.ylabel(ylab)  
    if outfigpathfile:   
        plt.savefig(outfigpathfile,edgecolor=None)
    else:
        plt.show()
    
def get_histo(imagey,normed=1):
    xbins=np.arange(0,257,1) #Go from 0 to 256, inclusive
    xbins=xbins-0.5 #This sorts out bin edges, from -0.5 to 0.5 (for 0) to 245.5 to 255.5 (for 255)
    xbincenters = 0.5*(xbins[1:]+xbins[:-1])
    flatimg=imagey.flatten()
    nufig=plt.figure()    
    n, bins, patches = plt.hist(flatimg,xbins, normed=normed, facecolor='green',edgecolor='none', alpha=0.75)
    plt.close()
    return n, xbins, xbincenters 
    #pdb.set_trace()
    
def read_image(imagepathfile):
    """Very basic function to read an image and return the data"""
    image_matrix=plt.imread(imagepathfile)
    return image_matrix

def plot_image(imagey,outfigpathfile=None,subtracting=False):
    """Very basic function to plot an image"""
    #imagey=np.random.random_integers(0,255,[500,800])
    if not subtracting: #Standard moon images
        cmap=mpl.cm.Greys_r #Goes from black to white
        vmin,vmax=0,255
    else:
        cmap=mpl.cm.seismic #Goes from blue to red: new craters (white) -> red
        vmin,vmax=-255,255 #Absolute max/min values
        
        
    plt.figure()
    aa=plt.imshow(imagey,cmap=cmap,vmin=vmin,vmax=vmax)
    #Turn off ticks, the edge, and fill entire figure
    #ax = mpl.axes.Axes(plt.gcf(),[0,0,1,1],yticks=[],xticks=[],frame_on=False)
    #plt.gcf().delaxes(plt.gca())
    #plt.gcf().add_axes(ax)    
    
    if outfigpathfile:   
        plt.savefig(outfigpathfile,edgecolor=None)
    else:
        plt.show()
    #pdb.set_trace()
    #pdb.set_trace()
    #moonfig=plt.figure()
    #plt.imshow(imagey,cmap=mpl.cm.Greys)
    #texty={"lon0":lon0,"lat0":lat0,"lon1":lon1,"lat1":lat1,"sat1":sat1,"sat2":sat2}
    #textstr="lon0={lon0}, lat0={lat0}, lon1={lon1},lat1={lat1}, sat1={sat1}, sat2={sat2}".format(**texty)
    #plt.text(100,200,textstr,color="r")
    #plt.savefig(figsavepath)
    
def gimme_subsection(inputimage,inputcoords,subsectioncoords):
    pass
    

if __name__=="__main__":
    main()
