import numpy as np
import pandas as pd
import matplotlib as mpl
import pylab as pl
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats


def read(filepath):
	with open('%s'%filepath) as f:
		lines = f.read().splitlines()
	newlines = [line.split() for line in lines]
	return newlines

def readchar(filepath):
	with open('%s'%filepath) as f:
		lines = f.read().splitlines()
	newlines = [list(line) for line in lines]
	return newlines

def plot1D(fig,row,column,num,x,y,yerr,title,color,ymin,ymax,legend=None,yticklabel=None):
    #row, column and num is subplot number. y and yerr is input value and errorbar. xtick and title and color are default input. if you want to change the ylabel like swap the y axis, please input ytick instead of adjusting ymin and ymax. if you want to put a legend, please input [legendname, x, y]
    ytick = np.arange(ymin,ymax+0.001,(ymax-ymin)/4.)
    ax = fig.add_subplot(row,column,num)
    if legend is not None:
        if isinstance(legend, list):
            label, xl, yl = legend
            ax.plot(x,y,'-',linewidth=5,c=color,label=label)
            ax.legend(bbox_to_anchor=(xl,yl),numpoints=1,borderaxespad=0.)
        else:
            print("legend should be a list including name and x, y position")
    else:
        ax.plot(x,y,'-',linewidth=5,c=color)
    ax.errorbar(x,y,yerr=yerr,c=color,capsize=0,elinewidth=0,fmt=' ')
    ax.set_title(title, fontsize=20)
    ax.set_xlim(-1,len(x))
    #ax.set_xticks(x)
    #ax.set_xticklabels(xticklabel)
    ax.set_ylim(ymin,ymax)
    ax.set_yticks(ytick)
    if yticklabel is not None:
        ax.set_yticklabels(yticklabel)

def plot2D(fig,row,column,num,x,y,title,xlabel,ylabel,color,xmin,xmax,ymin,ymax,legend=None,xticklabel=None,yticklabel=None):
    #row, column and num is subplot number. x and y is input value. title and color are default input. if you want to change the x/ystick like swap the x/y axis, please input x/ytick instead of adjusting x/ymin and x/ymax. if you want to put a legend, please input [legendname, x, y]
    ax = fig.add_subplot(row,column,num)
    xtick = np.arange(xmin,xmax+0.001,(xmax-xmin)/4.)
    ytick = np.arange(ymin,ymax+0.001,(ymax-ymin)/4.)
    if legend is not None:
        if isinstance(legend, list):
            label, xl, yl = legend
            ax.plot(x,y,'o',c=color,label=label,alpha=0.5)
            ax.legend(bbox_to_anchor=(xl,yl),numpoints=1)
        else:
            print("legend should be a list including name and x, y position")
    else:
        ax.plot(x,y,'o',c=color,alpha=0.5)
    ax.set_title(title, fontsize=20)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_xlim(xmin,xmax)
    ax.set_xticks(xtick)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_ylim(ymin,ymax)
    ax.set_yticks(ytick)
    if xticklabel is not None:
        ax.set_xticklabels(xticklabel)
    if yticklabel is not None:
        ax.set_yticklabels(yticklabel)

def hist1D(fig,row,column,num,array,binwidth,title,color,xmin,xmax,ymax,legend=None,alpha=None):
    #row, column and num is subplot number. array is input distribution. title and color are default input. same thing as xmin xmax ymax. if you want to put a legend, please input [legendname, x, y]
    ax = fig.add_subplot(row,column,num)
    bins = np.arange(xmin,xmax,binwidth)
    xtick = np.arange(xmin,xmax+0.001,(xmax-xmin)/4.)
    ytick = np.arange(0,ymax+0.001,ymax/5.)
    if legend is not None:
        if isinstance(legend, list):
            label, xl, yl = legend
            if alpha is None:
                hist, bins, p = ax.hist(array,bins=bins,normed=1,facecolor=color,alpha=0.7,label=label) 
            else:
                hist, bins, p = ax.hist(array,bins=bins,normed=1,facecolor=color,alpha=alpha,label=label) 
            ax.legend(bbox_to_anchor=(xl,yl),numpoints=1)
        else:
            print("legend should be a list including name and x, y position")
    else:
        if alpha is None:
            hist, bins, p = ax.hist(array,bins=bins,normed=1,facecolor=color,alpha=0.7) 
        else:
            hist, bins, p = ax.hist(array,bins=bins,normed=1,facecolor=color,alpha=alpha) 
    for item in p:  #sum of the height to be one
        item.set_height(item.get_height()/sum(hist))
    ax.set_title(title,fontsize=16)
    ax.set_xticks(xtick)
    ax.set_xlim(xmin,xmax)
    ax.set_yticks(ytick)
    ax.set_ylim(0,ymax)

def hist2D(fig,row,column,num,array1,array2,binwidth1,binwidth2,vmax,title,xlabel,ylabel,xmin,xmax,ymin,ymax,colorbar=False):
    #row, column and num is subplot number. array is input distribution. title is default input. same thing as xmin xmax ymin ymax. vmax is the height of the distribution.
    ax = fig.add_subplot(row,column,num)
    bins = [np.arange(xmin,xmax+binwidth1,binwidth1),np.arange(ymin,ymax+binwidth2,binwidth2)]
    xtick = np.arange(xmin,xmax+0.001,(xmax-xmin)/4.)
    ytick = np.arange(ymin,ymax+0.001,(ymax-ymin)/4.)
    H, x, y = np.histogram2d(array1, array2, bins=bins, normed=1)
    H = np.rot90(H)
    H = np.flipud(H)
    Hmasked = np.ma.masked_where(H==0,H)
    pcm = ax.pcolor(x,y,Hmasked,norm=colors.Normalize(vmin=0,vmax=vmax))
    if colorbar == True:
        drawclb(fig,ax,pcm,'full')
    ax.set_title(title,fontsize=16)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_xticks(xtick)
    ax.set_xlim(xmin,xmax)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_yticks(ytick)
    ax.set_ylim(ymin,ymax)

def phist2D(fig,row,column,num,array1,array2,binwidth1,binwidth2,vmax,title,rmin,rmax,rticks,rlabel,xlabel=None,xticklabels=False,lyax=False,colorbar=False):
    #this polar plot is from -180 to 180. row, column and num is subplot number. array is input distribution. array1 is in the polar axis, array2 is in the radial axis. binwidth1 is [rad/s] in polar axis. binwidth2 is [degree] in radial axis. title is default input. vmax is the height of the distribution. also input yticks and ylabel but the yticklabel is set []. you can input left y axes (lyax) to show ylabel and yticklabel in the left [].
    ax = fig.add_subplot(row,column,num,projection='polar')
    bins = [np.arange(-np.pi,np.pi+binwidth1,binwidth1),np.arange(rmin,rmax+binwidth2,binwidth2)]
    H, x, y = np.histogram2d(array1, array2, bins=bins, normed=1)
    H = np.rot90(H)
    H = np.flipud(H)
    Hmasked = np.ma.masked_where(H==0,H)
    pcm = ax.pcolor(x,y,Hmasked,norm=colors.Normalize(vmin=0,vmax=vmax))
    if colorbar is True:
        drawclb(fig,ax,pcm,'half')
    if xlabel is not None:
        ax.set_xlabel(xlabel,fontsize=16)
        ax.xaxis.set_label_coords(0,0)
    ax.set_xticks(np.pi/180.*np.linspace(180,-180,8,endpoint=False))
    ax.set_xticklabels([])
    if xticklabels is True:
        ax.set_xticklabels([180,135,90,45,0,-45,-90,-135])
    ax.set_yticks(rticks)
    ax.set_yticklabels([])
    if lyax is True:
        drawlyax(fig,ax,rticks,rlabel) 
    ax.set_title(title)
    ax.grid(True)

def phist3D(fig,row,column,num,r,phi,theta,title,colorbar=False):
    theta0 = np.linspace(0, np.pi, 61)
    phi0 = np.linspace(0, 2*np.pi, 121)
    theta0, phi0 = np.meshgrid(theta0, phi0)
    # The Cartesian coordinates of the unit sphere
    x = np.sin(theta0) * np.cos(phi0)
    y = np.sin(theta0) * np.sin(phi0)
    z = np.cos(theta0)
    # Set the aspect ratio to 1 so our sphere looks spherical
    ax = fig.add_subplot(row,column,num, projection='3d')
    ax.patch.set_facecolor('none')
    ax.plot_surface(x, y, z, rstride=10, cstride=10, linewidth=2, color='gray', alpha=0.1, antialiased=True)
    # Label the axis
    ax.quiver(1.5,0,0,3.5,0,0,length=2,linewidth=2,color='black',arrow_length_ratio=0.07)
    ax.quiver(0,1.5,0,0,3.5,0,length=2,linewidth=2,color='black',arrow_length_ratio=0.07)
    ax.quiver(0,0,1.5,0,0,3.5,length=2,linewidth=2,color='black',arrow_length_ratio=0.07)
    xx = r*np.sin(theta)*np.cos(phi)
    yy = r*np.sin(theta)*np.sin(phi)
    zz = 2*r*np.cos(theta)
    xyz = np.vstack([xx,yy,zz])
    kde = stats.gaussian_kde(xyz)
    density = kde(xyz)
    density = density/max(density)
    colmap = cm.ScalarMappable(cmap=cm.jet)
    colmap.set_array(density)
    ax.scatter(xx, yy, zz, c=cm.jet(density/max(density)*3), marker='o', s=50, alpha=0.5)
    if colorbar == True:
        cb = fig.colorbar(colmap)
    # Turn off the axis planes
    ax.set_axis_off()
    ax.set_xlim3d(-1,1)
    ax.set_ylim3d(-1,1)
    ax.set_zlim3d(-1,1)
    ax.set_title(title)

#change range of -360~-180 --> 0~180 and 180~360 --> -180~0
def restr(number):
    if number > 180:
        number = number - 360
    elif number < -180:
        number = number + 360
    return number



#================== Public Function ============================================

def drawclb(fig,ax,pcm,length):
    #Draw colorbar. Need to input axes and pcm (pcolor)
    box = ax.get_position()
    if length == 'half':
        cbaxes = fig.add_axes([box.xmax,0.5*(box.ymin+box.ymax),box.width/50,box.height*0.5])
    elif length == 'full':
        cbaxes = fig.add_axes([box.xmax+box.width/50,box.ymin,box.width/50,box.height])
    clb = pl.colorbar(pcm,cax=cbaxes)
    clb.set_label('population', labelpad=-40, y=1.2 , rotation=0)

def drawlyax(fig,ax,yticks,ylabel):
    #Draw left axis. Need to input axes.
    box = ax.get_position()
    axl = fig.add_axes([box.xmin/1.5,0.5*(box.ymin+box.ymax),box.width/50,box.height*0.5],axisbg=None)
    axl.spines['top'].set_visible(False)
    axl.spines['right'].set_visible(False)
    axl.spines['bottom'].set_visible(False)
    axl.yaxis.set_ticks_position('both')
    axl.xaxis.set_ticks_position('none')
    axl.set_xticklabels([])
    axl.set_yticks(yticks)
    axl.set_ylabel(ylabel, rotation=90)

#================== Global Variable ============================================
myfont = mpl.font_manager.FontProperties()
myfont.set_family('sans-serif')

subplotnum = [[1,1,1,1,1],[2,1,2,1,2],[3,1,3,1,3],[4,2,2,1,2],[5,2,3,1,3],[6,2,3,1,3],[7,3,3,1,3],[8,3,3,1,3],[9,3,3,1,3],[10,3,4,1,4],[11,3,4,1,4],[12,3,4,1,4],[13,4,4,1,4],[14,4,4,1,4],[15,4,4,1,4],[16,4,4,1,4],[17,4,5,1,5],[18,4,5,1,5],[19,4,5,1,5],[20,4,5,1,5]]
