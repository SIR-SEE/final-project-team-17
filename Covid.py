# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import random
import numpy as np
#from celluloid import Camera   # Ta bort om du vill se animationen 


#Animation. Om du någon vill testa skriv in "pip install celluloid" i consolen först och ta bort kommentaren framför import Camera och den i slutet.
#Onödig
def animera(Land1,Land2,Land3,Land4):
    L1=[]
    L2=[]
    L3=[]
    L4=[]
    färger=['b','y','r','g']
    labels=['Suseptible','Exposed','Infected','Recovered']
    fig,axes=plt.subplots(4)
    camera = Camera(fig)
    axes[0].set_title('Land1')
    axes[1].set_title('Land2')
    axes[2].set_title('Land3')
    axes[3].set_title('Land4')
    
    for i in range(len(Land1[1])):
        L1=Land1[0][i],Land1[1][i],Land1[2][i],Land1[3][i]
        L2=Land2[0][i],Land2[1][i],Land2[2][i],Land2[3][i]
        L3=Land3[0][i],Land3[1][i],Land3[2][i],Land3[3][i]
        L4=Land4[0][i],Land4[1][i],Land4[2][i],Land4[3][i]
        axes[0].pie(L1,colors=färger,labels=labels,labeldistance=1.2)
        axes[1].pie(L2,colors=färger,labels=labels,labeldistance=1.2)
        axes[2].pie(L3,colors=färger,labels=labels,labeldistance=1.2)
        axes[3].pie(L4,colors=färger,labels=labels,labeldistance=1.2)
        camera.snap()
    animation = camera.animate()
    animation.save('Snurrr.gif', writer='pillow',fps=5)    

#Deriv räknar ut på samma sätt som i SIR modellen vi fick Men den har en extra term Z som bromsar smittspridningen(Kommer från broms)
def deriv(S,E,I,R,N,Z):
    S,E,I,R=    S-beta*Z*S*I/N    ,    E+beta*Z*S*I/N-delta*E   ,   I+delta*E-k*I ,     R+k*I
    return(S,E,I,R)

#Samma som deriv men för första landet, eftersom den även räknar med sannolikheten att någon infekterad/exposed reser
def derivSWE(S,E,I,R,N,Z,Land3I,Land2I,Land4I):
    S,E,I,R=    S-beta*Z*S*I/N    ,    E+beta*S*Z*I/N-delta*E   ,   I+delta*E-k*I ,     R+k*I
    
    
    sannolikhetsmittad=((E+I)/N)
    if I>10000: sannolikhetsmittad=((E-I)/N) #När 10000 personer införs gränskontroll. Folk som är infekterade kan inte längre resa igenom


    if Land3I<1:
        if (random.random()<    1-(1-sannolikhetsmittad)**Land1_2):
            Land3I=1
            
            
    if Land2I<1:
        if (random.random()<    1  -(1-sannolikhetsmittad)**   Land1_3):
            Land2I=1
        
    if Land4I<1:
        if (random.random() <   1-(  1-sannolikhetsmittad)**   Land1_4):
            Land4I=1

    return(S,E,I,R,Land3I,Land2I,Land4I)


#Avgör vilka åtgärder som ska tas, Åtgärd 1, 2 eller 3. 3 är tidsbegränsad.
def broms(I,Åtgärd1,Åtgärd2,Åtgärd3,lockdowntid,Lockdown,BromsÅ1,BromsÅ2,BromsÅ3):

        Broms=1
        
        if I>Åtgärd1:
            Broms=Broms*BromsÅ1
            
        if I>Åtgärd2:
            Broms=Broms*BromsÅ2
            
        if I>Åtgärd3: 
            Lockdown=True
            
        if Lockdown==True and lockdowntid>0:
            lockdowntid+=-1
            Broms=Broms*BromsÅ3
        Broms=Broms*random.random()*2  #Random.random ger ett slumpat värde mellan 0 och 1. Ger ett roligare utseende på S och E
        return(Broms,Lockdown,lockdowntid)


def plotta(SWER,NORR,FINR,DANR): #Plottar
    färger=['b','y','r','g']
    labels=['Suseptible','Exposed','Infected','Recovered']
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
    for i in range(4):
        ax1.plot(tid,SWER[i],c=färger[i],alpha=0.7,linewidth=2,label=labels[i])
        ax2.plot(tid,NORR[i],c=färger[i],alpha=0.7,linewidth=2,label=labels[i])
        ax3.plot(tid,FINR[i],c=färger[i],alpha=0.7,linewidth=2,label=labels[i])
        ax4.plot(tid,DANR[i],c=färger[i],alpha=0.7,linewidth=2,label=labels[i])
    ax1.set_ylabel('Land1')
    ax2.set_ylabel('Land2')
    ax3.set_ylabel('Land3')
    ax4.set_ylabel('Land4')
    plt.xlabel("Tid")
    ax1.set_title("SEIR_Model Grupp 17")
    plt.legend()


#Smittspridning
beta = 2    #Hur många en smittad smittar varje dag i en helt frisk befolkning
k=1/7       #Hur lång tid smittan varar 
delta=1.0 / 5.0     #Hur lång tid det tar att gå från att bli Exposed till Infected

tid=np.linspace(0,149,150)


#Åtgärd 1, något litet som man börjar med tidig. Tex mask, Hur många ska vara infekterade för att man ska börja använda mask och hur stor effekt har masken
#Eller bara att man börjar stanna hemma om man har symptom
Åtgärd1=100000
BromsÅ1=0.80    #Effekt (0.6 motsvarar 40% minskning)

#Något lite större, T.ex alkoholförbud, stängda skolor, stängda gym osv.
Åtgärd2=300000 #Hur många infekterade föratt det ska börja
BromsÅ2=0.50 

#Lockdownen, hur många ska vara infekterade för att den ska börja och hur stor effekt den ska ha
Åtgärd3=1000000
BromsÅ3=0.05



Land1,Land2,Land3,Land4 =  10000000,53000000,20000000,10000000# population


#Hur länga lockdownen är i olika länderna Ä
#Ändra gärna
Lockdown1,Lockdown2,Lockdown3,Lockdown4=False,False,False,False
lockdowntid1=10
lockdowntid2=10
lockdowntid3=10
lockdowntid4=10

#Resor Över gränserna
# Hur många personer som reser över gränsen varje dag mellan de olika länderna
Land1_2=3000   
Land1_3=3500
Land1_4=1000




Land2I,Land3I,Land4I=0,0,0 #Infekterade




#Startvilkor och listor
S,E,I,R=Land1-1,1,0,0       # En smittad i land1 och inga i resterande länder
SF,EF,IF,RF=Land2,Land2I,0,0
SN,EN,IN,RN=Land3,Land3I,0,0 
SD,ED,ID,RD=Land4,0,0,0
S1,E1,I1,R1=[],[],[],[] #Listor
S2,E2,I2,R2=[],[],[],[] #Mer listor
S3,E3,I3,R3=[],[],[],[] #Ännu mer listor
S4,E4,I4,R4=[],[],[],[] #...du förstår nog



for i in range(len(tid)):  #Loopar deriv och broms
    
    Z,Lockdown1,lockdowntid1=broms(I,Åtgärd1,Åtgärd2,Åtgärd3,lockdowntid1,Lockdown1,BromsÅ1,BromsÅ2,BromsÅ3)
    S,E,I,R,Land3I,Land2I,Land4I=derivSWE(S,E,I,R,Land1,Z,Land3I,Land2I,Land4I)

    S1.append(S)
    E1.append(E)
    I1.append(I)
    R1.append(R)
    
    #Har en smittad person kommit över gränsen börjar smittspridningen i ett annat land med 5 personer.
    if Land2I>=1: 
        if EF==0:
            EF=5
            
        X,Lockdown2,lockdowntid2=broms(IF,Åtgärd1,Åtgärd2,Åtgärd3,lockdowntid2,Lockdown2,BromsÅ1,BromsÅ2,BromsÅ3)
        
        SF,EF,IF,RF=deriv(SF,EF,IF,RF,Land2,X)
        
            
    S2.append(SF)
    E2.append(EF)
    I2.append(IF)
    R2.append(RF)

        
    if Land3I>=1:
        if EN==0:
            EN=5
        Y,Lockdown3,lockdowntid3=broms(IN,Åtgärd1,Åtgärd2,Åtgärd3,lockdowntid3,Lockdown3,BromsÅ1,BromsÅ2,BromsÅ3)
        SN,EN,IN,RN=deriv(SN,EN,IN,RN,Land3,Y)
        
    S4.append(SN)
    E4.append(EN)
    I4.append(IN)
    R4.append(RN)
        
    if Land4I>=1:
        if ED==0:
            ED=5
        Å,Lockdown4,lockdowntid4=broms(ID,Åtgärd1,Åtgärd2,Åtgärd3,lockdowntid4,Lockdown4,BromsÅ1,BromsÅ2,BromsÅ3)
        SD,ED,ID,RD=deriv(SD,ED,ID,RD,Land4,Å)
    S3.append(SD)
    E3.append(ED)
    I3.append(ID)
    R3.append(RD)



SEIR1=[S1,E1,I1,R1]
SEIR2=[S2,E2,I2,R2]
SEIR3=[S3,E3,I3,R3]
SEIR4=[S4,E4,I4,R4]



plotta(SEIR1,SEIR2,SEIR3,SEIR4)


#animera(SEIR1, SEIR2, SEIR3, SEIR4)
 
 
 #I nuläget är modellen bara bra för att få en intuitiv förståelse för hur en smitta sprids. Men det kan vara värdefullt för att förstå hur mycket man behöver begräsa smittspridningen för att samhället ska klara sig bra
 #Framförallt kan det vara bra 
 
 
 #Sätt att förbättra modellen på skulle kunna vara att, t.ex: 
 #lägga till ett dödstal. Detta dödstalet skulle kunna öka om antalet infekterade kommer över ett visst tal som kan simulera intensivvårdens maxkapacitet. (Högre dödlighet för alla över kapaciteten.)
 #Införa lockdowns för olika länderna på ett annat sätt. T.ex om 1% av befolkningen är sjuka istället för vad den är nu
 #En chans till att det kommer en ny mutation och att folk förlorar immunitet
 #Länderna kanske är ihopblandade i nuläget ¯\_(ツ)_/¯ 
 #Förbättra gränserna
 #Lägga till fler länder och så att det går att bestämma antalet länder. (Kanske svårt)
 #Göra antalet lockdowns och andra åtgärder fler och även där göra det möjligt att reglera hur många och hur lång tid de verkar.
 #Försöka göra modellen mer verklighetstrogen genom att korrigera siffror 
