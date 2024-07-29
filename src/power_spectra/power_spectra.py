import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
import scipy.signal as signal
import sys
import os

filename = os.path.join(os.pardir, 'data', 'raw', 'sysSim_1_randomO.csv')
sysm = pd.read_csv(filename)
n = int((len(sysm.columns)-2)/9)
t = sysm['Time']
filenum = str(sys.argv[1]).zfill(3)
output = 'sysSim_' + filenum +'randomO.pdf'
raster = True
with PdfPages(output) as pdf:
    print(len(sysm.columns))
    for i in range(n-1):
        fig,ax = plt.subplots(figsize=(16,12))
        #plt.figure(figsize=(16,12))
        ax.set_title('Probability of Pair: P'+str(i+1)+'-P'+str(i+2),fontsize=30)
        m_inc = np.arccos(np.cos(sysm["Planet "+str(i+1)+" inclination"])*np.cos(sysm["Planet "+str(i+2)+" inclination"])+np.sin(sysm["Planet "+str(i+1)+" inclination"])*np.sin(sysm["Planet "+str(i+2)+" inclination"])*np.cos(sysm["Planet "+str(i+1)+" Omega"]-sysm["Planet "+str(i+2)+" Omega"]))
        #m_inc = m_inc/np.mean(m_inc)
        p_mean = np.ones(len(t))*np.mean(sysm["N pairs:"+str(i+1)+"-"+str(i+2)])
        p_median = np.ones(len(t))*np.median(sysm["N pairs:"+str(i+1)+"-"+str(i+2)])
        
        lns1= ax.scatter(sysm['Time'],sysm["N pairs:"+str(i+1)+"-"+str(i+2)],label='Pair Probability',color='blue',s=2,rasterized=raster)
        ax2=ax.twinx()
        lns2 = ax2.scatter(sysm['Time'],m_inc/np.pi*180,color='red',s=2,alpha=0.25,rasterized=raster,label='Mutual Inc')
        #plt.scatter(sysm['Time'],m_inc*np.mean(sysm["N pairs:"+str(i+1)+"-"+str(i+2)]),label='Mutual Inclination',alpha=0.25)
        lns3 = ax.scatter(t,p_mean,label='Mean',c='g',s=0.1,alpha=0.5,rasterized=raster)
        lns4 = ax.scatter(t,p_median,label='Median',c='m',s=0.1,alpha=0.5,rasterized=raster)
	
        #ax.legend()
        ax.set_yscale('log')
        ax.set_xlabel('Time (Myr)',fontsize = 24)
        ax.set_ylabel('Probability', fontsize = 24)

        ax2.set_ylabel('Mutual Inc (Deg)', fontsize = 24)
        #lns = lns1+lns2+lns3+lns4
        #labs = [l.get_label() for l in lns]
        #ax.legend(lns, labs, loc=0)
        fig.legend(loc="upper right")
        pdf.savefig(fig)
        plt.close()
    plt.figure(figsize=(16,12))
    plt.title('Probability of # of Planets',fontsize=30)
    for i in range(n):
        plt.scatter(sysm['Time'],sysm[str(i+1)+" Planets"],label=str(i+1)+' P',s=1,rasterized=raster)
    plt.rc('legend',fontsize=14)
    #plt3.rc('title',fontsize=20)
    #plt.rc('xlabel', fontsize=20)
    #plt.rc('ylabel',fontsize=20)
    plt.legend()
    plt.yscale('log')
    plt.xlabel('Time (Myr)',fontsize = 24)
    plt.ylabel('Probability', fontsize = 24)
    pdf.savefig()
    plt.close()
    G = 6.67e-11
    for i in range(n):
        
        fig,ax = plt.subplots(2,2,figsize=(16,12))
        msun = sysm['Stellar mass'].to_numpy()
        mp = sysm['Planet '+str(i+1)+' mass'].to_numpy()
        ap = sysm['Planet '+str(i+1)+' semi maj'].to_numpy()
        period = np.sqrt(ap**3*4*np.pi**2/G/(msun+mp))
        p_day = str(round(np.mean(period)/60/60/24,2))
        fig.suptitle('Planet '+str(i+1)+': '+p_day+' Day Period', fontsize=30)
        ax[0,0].scatter(sysm['Time'],sysm["Planet "+str(i+1)+" inclination"]*180/np.pi,label='P'+str(i+1)+' Inc',s=0.5,rasterized=raster)
        #ax[0,0].legend()
        ax[0,0].set_title('Inclination')
        ax[0,0].set_xlabel('Time (Myr)')
        ax[0,0].set_ylabel('Inc (deg)')

        ax[1,1].scatter(sysm['Time'],sysm["Planet "+str(i+1)+" omega"]*180/np.pi,label='P'+str(i+1)+' $\omega$',s=0.5,rasterized=raster)
        #ax[0,1].legend()
        ax[1,1].set_title('$\omega$')
        ax[1,1].set_xlabel('Time (Myr)')
        ax[1,1].set_ylabel('$\omega$')

        ax[0,1].scatter(sysm['Time'],sysm["Planet "+str(i+1)+" Omega"]*180/np.pi,label='P'+str(i+1)+' $\Omega$',s=0.5,rasterized=raster)
        #ax[1,0].legend()
        ax[0,1].set_title('$\Omega$')
        ax[0,1].set_xlabel('Time (Myr)')
        ax[0,1].set_ylabel('$\Omega$ (deg)')

        ax[1,0].scatter(sysm['Time'],sysm["Planet "+str(i+1)+" ecc"],label='P'+str(i+1)+' Ecc',s=0.5,rasterized=raster)

        #ax[1,1].legend()
        ax[1,0].set_title('Ecc')
        ax[1,0].set_xlabel('Time (Myr)')
        ax[1,0].set_ylabel('Ecc')
    
        pdf.savefig(fig)
        plt.close()

        
        fig,ax = plt.subplots(2,2,figsize=(16,12))
        msun = sysm['Stellar mass'].to_numpy()
        mp = sysm['Planet '+str(i+1)+' mass'].to_numpy()
        ap = sysm['Planet '+str(i+1)+' semi maj'].to_numpy()
        period = np.sqrt(ap**3*4*np.pi**2/G/(msun+mp))
        p_day = str(round(np.mean(period)/60/60/24,2))
        fig.suptitle('Planet '+str(i+1)+': '+p_day+' Day Period (Log-Time)', fontsize=30)
        ax[0,0].scatter(sysm['Time'],sysm["Planet "+str(i+1)+" inclination"]*180/np.pi,label='P'+str(i+1)+' Inc',s=0.5,rasterized=raster)
        #ax[0,0].legend()
        ax[0,0].set_title('Inclination')
        ax[0,0].set_xlabel('Time (Myr)')
        ax[0,0].set_xlim(1e2,1e5)
        ax[0,1].set_xlim(1e2,1e5)
        ax[1,0].set_xlim(1e2,1e5)
        ax[1,1].set_xlim(1e2,1e5)

	
        ax[0,0].set_ylabel('Inc (deg)')
        ax[0,0].set_xscale('log')
        ax[1,1].scatter(sysm['Time'],sysm["Planet "+str(i+1)+" omega"]*180/np.pi,label='P'+str(i+1)+' $\omega$',s=0.5,rasterized=raster)
        #ax[0,1].legend()
	
        ax[1,1].set_title('$\omega$')
        ax[1,1].set_xlabel('Time (Myr)')
        ax[1,1].set_ylabel('$\omega$')
        
        ax[1,1].set_xscale('log')
        ax[0,1].scatter(sysm['Time'],sysm["Planet "+str(i+1)+" Omega"]*180/np.pi,label='P'+str(i+1)+' $\Omega$',s=0.5,rasterized=raster)
        #ax[1,0].legend()
        ax[0,1].set_title('$\Omega$')
        ax[0,1].set_xlabel('Time (Myr)')
        ax[0,1].set_ylabel('$\Omega$ (deg)')
        ax[0,1].set_xscale('log')

        ax[1,0].scatter(sysm['Time'],sysm["Planet "+str(i+1)+" ecc"],label='P'+str(i+1)+' Ecc',s=0.5,rasterized=raster)

        #ax[1,1].legend()
        ax[1,0].set_title('Ecc')
        ax[1,0].set_xlabel('Time (Myr)')
        ax[1,0].set_ylabel('Ecc')
        ax[1,0].set_xscale('log')
    
        pdf.savefig(fig)
        plt.close()


        h = np.array(sysm["Planet "+str(i+1)+" ecc"]*np.sin(sysm["Planet "+str(i+1)+" Omega"]+sysm["Planet "+str(i+1)+" omega"]))
        k = np.array(sysm["Planet "+str(i+1)+" ecc"]*np.cos(sysm["Planet "+str(i+1)+" Omega"]+sysm["Planet "+str(i+1)+" omega"]))
        p = np.array(np.sin(sysm["Planet "+str(i+1)+" inclination"])*np.sin(sysm["Planet "+str(i+1)+" Omega"]))
        q = np.array(np.sin(sysm["Planet "+str(i+1)+" inclination"])*np.cos(sysm["Planet "+str(i+1)+" Omega"]))
        hfft = np.abs(np.fft.rfft(h))
        kfft = np.abs(np.fft.rfft(k))
        pfft = np.abs(np.fft.rfft(p))
        qfft = np.abs(np.fft.rfft(q))

        hmaxes = signal.find_peaks(hfft, height=np.max(hfft)*0.1,distance=10)[0]
        kmaxes = signal.find_peaks(kfft, height=np.max(kfft)*0.1,distance=10)[0]
        pmaxes = signal.find_peaks(pfft, height=np.max(pfft)*0.1,distance=10)[0]
        qmaxes = signal.find_peaks(qfft, height=np.max(qfft)*0.1,distance=10)[0]

        freq = np.fft.rfftfreq(len(h),d=sysm['Time'][1])
        fig,ax = plt.subplots(2,2,figsize=(16,12))
        
        fig.suptitle('Planet '+str(i+1)+' Equinoctial Angles', fontsize=20)
        alp = 0
        ax[0,0].plot(1/freq,hfft,label='P'+str(i+1)+' H vector',rasterized=raster)
        ax[0,0].vlines(1/freq[hmaxes], 0, np.max(hfft), linestyles ="dashed", colors ="k",alpha=alp)
        ax[0,0].set_xscale('log')
        ax[0,0].set_title('H vector')
        ax[0,0].set_xlabel('Period (years)')
        ax[0,0].set_ylabel('H vector')
        
        ax[0,1].plot(1/freq,kfft,label='P'+str(i+1)+' K vector',rasterized=raster)
        ax[0,1].vlines(1/freq[kmaxes], 0, np.max(kfft), linestyles ="dashed", colors ="k",alpha=alp)
        ax[0,1].set_xscale('log')
        ax[0,1].set_title('K vector')
        ax[0,1].set_xlabel('Period (years)')
        ax[0,1].set_ylabel('K vector')
        
        ax[1,0].plot(1/freq,pfft,label='P'+str(i+1)+' P vector',rasterized=raster)
        ax[1,0].vlines(1/freq[pmaxes], 0, np.max(pfft), linestyles ="dashed", colors ="k",alpha=alp)
        ax[1,0].set_xscale('log')
        ax[1,0].set_title('P vector')
        ax[1,0].set_xlabel('Period (years)')
        ax[1,0].set_ylabel('P vector')
        
        ax[1,1].plot(1/freq,qfft,label='P'+str(i+1)+' Q vector',rasterized=raster)
        ax[1,1].vlines(1/freq[qmaxes], 0, np.max(qfft), linestyles ="dashed", colors ="k",alpha=alp)
        ax[1,1].set_xscale('log')
        ax[1,1].set_title('Q vector')
        ax[1,1].set_xlabel('Period (years)')
        ax[1,1].set_ylabel('Q vector')

        ax[0,0].grid(which='both',alpha=0.25)
        ax[0,1].grid(which='both',alpha=0.25)
        ax[1,0].grid(which='both',alpha=0.25)
        ax[1,1].grid(which='both',alpha=0.25)
    #print(fig)
        pdf.savefig(fig)
        plt.close()