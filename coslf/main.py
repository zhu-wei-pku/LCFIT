#!/usr/bin/env python

from dataio import *
from lslft_recon import *
import cmd_parse as cmdp
import cfg_parse as cfgp

def main():
    '''Given the position of transit to window (given by tran,tran[0]=ts, tran[1]=te) and do a better fit for the base line\n
	  Only use when reprocess the selected lightcurves, apply for a short baseline with one deep known transit\n
	  It is a useful thing to do before the kepfit_simple.sh
	  Warning: the output file does not containing the full information of the inputfile, only 2 columns with BJD and detrended flux. The replaceflag is default off to prevent unwantted replace of files. '''
    
    options = cmdp.ltf_parse()
    infileflag = options.infileflag
    outfileflag = options.outfileflag
    inpathflag = options.inpathflag
    noplot=options.noplot
    cfgfile = options.cfg
    uflag = options.uflag
    infile = 'test.txt'
    outfile = 'test_recon.txt'
    
    if(infileflag):
        infile = cfgp.ltf_parse(cfgfile,'infile')
    else:
        infile = options.infile

    if(inpathflag):
        inpath = cfgp.ltf_parse(cfgfile,'inpath')
    else:
        inpath = options.inpath
    if(outfileflag):
        outfile = cfgp.ltf_parse(cfgfile,'outfile')
    else:
        outfile = options.outfile 
    
    coljd = 1; colmag = 2 
    tmin=1.0
    if(uflag):
        coljd = int(cfgp.ltf_parse(cfgfile,'coljd'))
        colmag = int(cfgp.ltf_parse(cfgfile,'colmag'))
        tmin = float(cfgp.ltf_parse(cfgfile,'tmin'))
         
    period = float(cfgp.ltf_parse(cfgfile,'period'))
    epoch = float(cfgp.ltf_parse(cfgfile,'epoch'))
    Tdur = float(cfgp.ltf_parse(cfgfile,'tdur'))
    
    time=[]
    mag=[]
    q = Tdur/period/24.
    readcolumn(time,coljd,infile);time=np.array(time)
    readcolumn(mag,colmag,infile);mag=np.array(mag)
    #print len(time),len(mag),max(time),min(time)
    intran = gentran(time,period,epoch,q)
    #dip = np.mean(mag[intran])-np.mean(mag[-intran])
    #dip = 0.00775
  
    #print np.mean(mag),np.mean(mag[intran]),np.mean(mag[-intran]),dip
    
    n=round((max(time)-min(time))/tmin)

    dflux=lssubrecon(time,mag,intran,n=n,noplot=noplot)
    dflux=dflux+(min(mag)-np.median(dflux))
    
    fout=open(outfile,mode='w')
    for i in range(len(time)):
        line='%10.6f %10.6f\n' % (time[i],dflux[i])
        fout.write(line)
    fout.close()
    
    return	
	
if __name__=='__main__':
    main()
