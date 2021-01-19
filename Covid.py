# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 10:39:56 2021

@author: famwe
"""

#Totalt antal gästnätter i norge, från sverige. 3.5 miljoner om varje person är i det andra
#landet 7 dagar ger det 3.5/7=0.5miljoner resenärer under ett år. Man får också räkna åt andra hållet
#Om antalet som reser över gränsen är propertioneligt mot befolkningen, reser 
#Norge med 0.25 miljoner personer per år
# alltså gränsen mellan norge till Sverige är på ett år 0.75 miljoner, 
# En normal dag blir det då ~2056 personer som reser över gränsen på semester.
#Finland 600000 nätter/7        234 resor per dag från   S->F   351
#Danmark 1340000/7  =           722 resor per dag S->D          + 722/2 = 1083
#Norge                          
import matplotlib.pyplot as plt
import random
import numpy as np
from celluloid import Camera



#Resor Swe-Nor Swe-Fin Swe-Dan
S_N=2056
S_F=351
S_D=1083

SS,ES,IS,RS=[],[],[],[]
SFL,EFL,IFL,RFL=[],[],[],[]
SDL,EDL,IDL,RDL=[],[],[],[]
SNL,ENL,INL,RNL=[],[],[],[]

DANI,FINI,NORI=0,0,0 #Infekterade och exposed i Dan,Fin,Nor


#Olika åtgärder
#Soft_lockdown=0.5 #Gym pub osv
#Total_lockdown=0.95 # Endast 
#Lockdown=0.5
#Mask=0.95
#PåNyheter=0.8
#Mask_på=
#Lockdown=
#Resor=0.05

#Befolkning
SWE,NOR,FIN,DAN =  10000000,5300000,5500000,5500000# population

#Befolkningstätheterna är olika i länderna. Därför sprids det olika snabbt

Z=1
BromsD=1.05
BromsF=0.9
BromsN=0.9



Åtgärd1=2 #Procent av befolkning
BromsÅ1=0.80

Åtgärd2=500
BromsÅ2=0.90

Åtgärd3=10
BromsÅ3=0.02

TidÅtgärd3=20

beta = 2
k=1/7      
delta=1.0 / 5.0

DANI=0
FINI=0
NORI=0
#Startvilkor
S,E,I,R=SWE-1,1,0,0
SF,EF,IF,RF=FIN,FINI,0,0
SN,EN,IN,RN=NOR,NORI,0,0
SD,ED,ID,RD=DAN,DANI,0,0

tid=np.linspace(0,99,100)

def derivSWE(S,E,I,R,N,Z,NORI,FINI,DANI):
    S,E,I,R=    S-beta*Z*S*I/N    ,    E+beta*S*Z*I/N-delta*E   ,   I+delta*E-k*I ,     R+k*I
    
    sannolikhetsmittad=((E+I)/N)
    
    if I>10000: sannolikhetsmittad=((I-E)/N)

    
    if NORI<1:
        if (random.random()<(S_N*sannolikhetsmittad)):
            NORI=1
            
            
    if FINI<1:
        if (random.random()<(S_F*(sannolikhetsmittad))):
            FINI=1
            
            
    if DANI<1:
        if (random.random()<(S_D*(sannolikhetsmittad))):
            DANI=1

    return(S,E,I,R,NORI,FINI,DANI)

def deriv(S,E,I,R,N,Z):
    S,E,I,R=    S-beta*Z*S*I/N    ,    E+beta*Z*S*I/N-delta*E   ,   I+delta*E-k*I ,     R+k*I
    return(S,E,I,R)

t=0
for i in range(len(tid)):
    if I>Åtgärd3*SWE/100 and t==0:
        Z=Z*BromsÅ3
        if t==0:
            t=i
            
    elif (i-t)>TidÅtgärd3:
        Z=1
        
        
    if I>Åtgärd1*SWE/100:
        Z=Z*BromsÅ1
        
        
    if I>Åtgärd2*SWE/100:
        Z=Z*BromsÅ2
    
    S,E,I,R,NORI,FINI,DANI=derivSWE(S,E,I,R,SWE,Z,NORI,FINI,DANI)

    SS.append(S)
    ES.append(E)
    IS.append(I)
    RS.append(R)
    
    
    if FINI>=1:
        if EF==0:
            EF=10
        SF,EF,IF,RF=deriv(SF,EF,IF,RF,FIN,BromsF)
        
        if IF>FIN*Åtgärd2/100:
            BromsF=BromsF*BromsÅ1
            
    SFL.append(SF)
    EFL.append(EF)
    IFL.append(IF)
    RFL.append(RF)

        
    if NORI>=1:
        if EN==0:
            EN=10
        SN,EN,IN,RN=deriv(SN,EN,IN,RN,NOR,BromsN)
    SNL.append(SN)
    ENL.append(EN)
    INL.append(IN)
    RNL.append(RN)
        
        
    if DANI>=1:
        if ED==0:
            ED=10
        SD,ED,ID,RD=deriv(SD,ED,ID,RD,DAN,BromsD)
    SDL.append(SD)
    EDL.append(ED)
    IDL.append(ID)
    RDL.append(RD)



Sser=[SS,ES,IS,RS]
Fser=[SFL,EFL,IFL,RFL]
Nser=[SNL,ENL,INL,RNL]
Dser=[SDL,EDL,IDL,RDL]



def plotta(SWER,NORR,FINR,DANR):
    färger=['b','y','r','g']
    labels=['Suseptible','Exposed','Infected','Recovered']
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
    for i in range(4):
        ax1.plot(tid,SWER[i],c=färger[i],alpha=0.7,linewidth=2,label=labels[i])
        ax2.plot(tid,NORR[i],c=färger[i],alpha=0.7,linewidth=2,label=labels[i])
        ax3.plot(tid,FINR[i],c=färger[i],alpha=0.7,linewidth=2,label=labels[i])
        ax4.plot(tid,DANR[i],c=färger[i],alpha=0.7,linewidth=2,label=labels[i])
    ax1.set_ylabel('SWE')
    ax2.set_ylabel('NOR')
    ax3.set_ylabel('FIN')
    ax4.set_ylabel('DAN')
#    ax1.set_xlim(20,80)
 #   ax2.set_xlim(20,80)
  #  ax3.set_xlim(20,80)
   # ax4.set_xlim(20,80)
    plt.legend()



plotta(Sser,Nser,Fser,Dser)

#fig = plt.figure()
färger=['b','y','r','g']
labels=['Suseptible','Exposed','Infected','Recovered']
#for i in range(len(Sser)):
fig,axes=plt.subplots(4)
camera = Camera(fig)
axes[0].set_title('Land1')
axes[1].set_title('Land2')
axes[2].set_title('Land3')
axes[3].set_title('Land4')

for i in range(len(SS)):
    SEEEER1=[SS[i],ES[i],IS[i],RS[i]]
    SEEEER2=[SNL[i],ENL[i],INL[i],RNL[i]]
    SEEEER3=[SDL[i],EDL[i],IDL[i],RDL[i]]
    SEEEER4=[SFL[i],EFL[i],IFL[i],RFL[i]]
    axes[0].pie(SEEEER1,colors=färger,labels=labels,labeldistance=1.2)
    axes[1].pie(SEEEER2,colors=färger,labels=labels,labeldistance=1.2)
    axes[2].pie(SEEEER3,colors=färger,labels=labels,labeldistance=1.2)
    axes[3].pie(SEEEER4,colors=färger,labels=labels,labeldistance=1.2)

    camera.snap()


#animation = camera.animate()
#animation.save('Ttest9.gif', writer='pillow',fps=5)    