#Tier Shift Analysis

from statsparse import *

import pandas

from sklearn.linear_model import Perceptron
from sklearn import svm

import matplotlib.pyplot as plotlib

import datetime
from calendar import monthrange
import numpy

#import tieringactions

def parseallusage(gen,tier=OU,year=0,month=0,months=0):
    allusage=pandas.DataFrame(columns=["Mon"])
    allusage.set_index("Mon")
    years=[]
    mons=set()
    if (year==0):
        years=GEN_TO_YEAR[gen]
    else:
        years=[year]
    if (months==0):
        months=len(years)*12
    monthspassed=0
    stopit=False

    for y in range(years[0],years[0]+months//12+1):
        if (stopit):
            break
        for m in range(1,13):
            if (monthspassed==months):
                stopit=True
                break
            monthspassed+=1
            usage=pandas.read_csv(getusagefile(y,m,gen,tier),index_col="Mon")
            usage[pandas.to_numeric(usage["W"],errors="coerce").notnull()]
            #print(usage)
            mons.union(set(usage.index))
            allusage=pandas.merge(left=allusage,right=usage["W"].rename(datetime.date(y,m,monthrange(y,m)[1]),inplace=True),on="Mon",how="outer")
    #allusage.fillna(0,inplace=True)
    allusage.set_index("Mon",inplace=True)
    #print(allusage)
    return allusage

def findBans(gen,tier="",year=0):
    AllActions=pandas.read_csv("stats/bans.csv")
    if (year==0):
        years=GEN_TO_YEAR[gen]
    else:
        years=[year]
    if (len(tier)>0 and tier in AllActions["Tier"].values):
        return AllActions.loc[(AllActions["Gen"]==gen) & (AllActions["Tier"]==tier) & (AllActions["Year"].isin(years))]
    else:
        return AllActions.loc[AllActions["Gen"]==gen & AllActions["Year"].isin(years)]


def testuublmons():
    usage=parseallusage(8,year=2021,months=18)
    bans=findBans(gen=8,tier=UU)
    uublusage=usage.loc[usage.index.isin(bans["Subject"].values)]
    #uublusage=uublusage.sort_values(datetime.date(2021,1,31),ascending=False)
    #p1=uublusage.plot(kind="line",yticks=range(40))
    """banlines={date:subject+" "+verdict+"ED" for date, subject, verdict in zip(plotbans["Date"],plotbans["Subject"],plotbans["Verdict"])}
    texty=35
    textoffset=10
    for ban in banlines:
        print(ban)
        plotlib.axvline(x=ban,label=banlines[ban])
        plotlib.text(ban,texty,banlines[ban],rotation=60)
        texty-=textoffset
        if (texty<20):
            texty+=20
    plotlib.axhline(y=4.52,color="black",linestyle="--",label="OU Cutoff")

    plotlib.show()"""

def test():
    usage=parseallusage(8,year=2021).sort_values("2021-01",ascending=False)
    bans=findBans(8)
    salamence=usage.iloc[:30].transpose()
    p1=salamence.plot(kind="line",yticks=range(50))
    plotlib.axhline(y=4.52,color="black",linestyle="--")
    plotlib.show()

def testquarterlyshiftcorrelation():
    usage=parseallusage(8,year=2021,months=18)
    bans=findBans(8,OU)
    bans=bans.loc[bans["Year"]>2020]
    top50=usage.loc[~usage.index.isin(bans["Subject"])]
    top50.columns=(pandas.to_datetime(top50.columns))


    """p1=top50.transpose().plot(kind="line",yticks=range(0,51,2))
    plotlib.axvline(x=datetime.datetime(2021,4,1))
    plotlib.axvline(x=datetime.datetime(2021,7,1))
    plotlib.axvline(x=datetime.datetime(2021,10,1))
    plotlib.axvline(x=datetime.datetime(2022,1,1))
    plotlib.axvline(x=datetime.datetime(2022,4,1))"""
    #plotbans=bans.loc[bans["Year"]>2020]
    """ print(plotbans)
    banlines={date:subject+" "+verdict+"NED" for date, subject, verdict in zip(plotbans["Date"],plotbans["Subject"],plotbans["Verdict"])}
    texty=40
    textoffset=10
    for ban in banlines:
        print(ban)
        plotlib.axvline(x=ban,label=banlines[ban],linestyle="--")
        plotlib.text(ban,texty,banlines[ban],rotation=60)
        texty-=textoffset
        textoffset*=-1 """
    top50q=top50.T.resample("Q",offset='30 days',convention="end").mean().T
    #print(top50q)
    dq=pandas.date_range('2021-01-01','2022-07-01',freq="Q")
    #top50q.transpose().plot(kind="line",yticks=range(0,51,2))
    deltatop50=top50.diff(1,1)
    deltatop50q=top50q.diff(1,1).map(lambda x:1 if x>0 else 0)
    isouq=top50q.map(lambda x:1 if x>=4.52 else 0).shift(1,axis="columns",fill_value=0)
    dec20usage=pandas.read_csv(getusagefile(2020,12,8,OU,seg=2),index_col="Mon")
    dec20ou=dec20usage.loc[dec20usage["W"]>=4.52].index
    for mon in dec20ou:
        isouq.at[mon,"2021-03-31"]=1
    isouq=isouq.convert_dtypes()
    #print(isouq[:10])
    isou=isouq.transpose().resample(rule="M",convention="end").bfill().transpose()
    dec20uu=pandas.read_csv(getusagefile(2020,12,8,UU,seg=2,elo=ELO_2),index_col="Mon")
    #I hate pandas so much why can't i just use fucking excel
    """isou['2021-01-31']=isou['2021-03-31']
    isou['2021-02-28']=isou['2021-01-31']
    isou=isou[sorted(isou.columns)]
    roseou=isou.diff(3,1).fillna(0)
    #print(top50q.iloc[:10])
    #print("Is OU:")
    #print(isou.iloc[30:50])
    roseou['2021-01-31']=isou['2021-01-31']
    for mon in roseou.index:
        if mon in dec20uu.index and roseou.at[mon,'2021-01-31']==1:
            roseou.at[mon,"2021-01-31"]=0
        
        roseou.at[mon,"2021-05-31"]=0
        roseou.at[mon,"2021-06-30"]=0
        roseou.at[mon,"2021-08-31"]=0
        roseou.at[mon,"2021-09-30"]=0
        roseou.at[mon,"2021-10-31"]=0
        roseou.at[mon,"2021-12-31"]=0
        roseou.at[mon,"2022-02-28"]=0
        roseou.at[mon,"2022-03-31"]=0
        roseou.at[mon,"2022-05-31"]=0
        roseou.at[mon,"2022-06-30"]=0
    #roseou.loc[~roseou.index.isin(dec20uu),['2021-01-31']].replace(1,0)
    fellou=roseou.map(lambda x:1 if x<0 else 0)
    #fellou.loc[~fellou.index.isin(dec20uu),['2021-01-31']].replace(0,1)
    for mon in roseou.index:
        if (not mon in dec20uu.index) and fellou.at[mon,'2021-01-31']==0:
            fellou.at[mon,"2021-01-31"]=1
        fellou.at[mon,"2021-05-31"]=0
        fellou.at[mon,"2021-06-30"]=0
        fellou.at[mon,"2021-08-31"]=0
        fellou.at[mon,"2021-09-30"]=0
        fellou.at[mon,"2021-10-31"]=0
        fellou.at[mon,"2021-12-31"]=0
        fellou.at[mon,"2022-02-28"]=0
        fellou.at[mon,"2022-03-31"]=0
        fellou.at[mon,"2022-05-31"]=0
        fellou.at[mon,"2022-06-30"]=0"""
    roseou=roseou.map(lambda x:1 if x>0 else 0)
    #print("Rose to OU:")
    #print(roseou.iloc[30:50])
    #print(fellou.iloc[30:50])
    learner=svm.SVC()
    learner.set_params()
    risers=[]
    i=0
    rose=[]
    didnotrise=[]
    for idx, row in roseou.iterrows():
        for num in row:
            if (num>0):
                risers.append(idx)
    
    for riser in risers:
        row=roseou.loc[roseou.index==riser].values[0]
        print(riser, row)
        delta=deltatop50.loc[deltatop50.index==riser].values
        for j in range(len(delta)):
            if (row[j]==1):
                rose.append(delta[j])
            else:
                didnotrise.append(delta[j])
    print(rose)
    print(didnotrise)
    """banlines={date:verdict+" "+subject for date, subject, verdict in zip(bans["Date"],bans["Subject"],bans["Verdict"])}
    
    dmonths=pandas.date_range('2021-01-01','2022-07-01',freq="M")
    p1.set_xticks(dmonths,minor=True)
    p1.set_axisbelow(True)
    p1.legend(loc="upper left",ncol=5)
    p1.grid(True,which="both")
    plotlib.axhline(y=4.52,color="grey",linestyle="--")
    ymax=p1.get_ybound()[1]
    
    texty=7
    for ban in banlines:
        linecolor="red"
        if (banlines[ban][0]=="U"):
            linecolor="blue"
        plotlib.axvline(x=ban,ymax=texty/ymax,label=banlines[ban],color=linecolor)
        plotlib.text(ban,texty,banlines[ban])
        texty-=0.5
        if (texty<5):
            texty=7"""

    """banlines={date:subject+" "+verdict+"NED" for date, subject, verdict in zip(bans["Date"],bans["Subject"],bans["Verdict"])
              if pandas.to_datetime(date).date()>=datetime.date(2021,1,1) and pandas.to_datetime(date).date()<datetime.date(2022,6,30)}
    for ban in banlines:
        plotlib.axvline(x=ban,label=banlines[ban],linestyle="--")
        plotlib.text(ban,texty,banlines[ban],rotation=60)
        texty-=textoffset
        textoffset*=-1"""

    #print(deltatop50)
    """p1.set_xticks(dq)
    p1.set_xticks(top50.columns,minor=True)"""

    #plotlib.show()
    return

def testuublcorrelation():
    usage=parseallusage(8,year=2021,months=18)
    bans=findBans(8,OU)
    top50=usage.loc[~usage.index.isin(bans["Subject"])].iloc[:100]
    top50.columns=(pandas.to_datetime(top50.columns))
    top50q=top50.resample("Q",axis=1,offset='30 days',convention="end").mean()
    #print(top50q)
    dq=pandas.date_range('2021-01-01','2022-07-01',freq="Q")
    #top50q.transpose().plot(kind="line",yticks=range(0,51,2))
    """deltatop50=top50.diff(1,1)
    deltatop50q=top50q.diff(1,1).map(lambda x:1 if x>0 else 0)
    isou=top50q.map(lambda x:1 if x>=4.52 else 0)"""

    
    uubans=findBans(8,UU)
    uublusage=usage.loc[usage.index.isin(uubans["Subject"].values)]
    uubanhist={subject:{"bans":[],"unbans":[]} for subject in uublusage.index}
    isuubl={}
    for subject in uublusage.index:
        hist=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        for idx, row in uubans.loc[uubans["Subject"]==subject].iterrows():
            if (row["Verdict"]=="BAN"):
                uubanhist[subject]["bans"].append(datetime.date(row["Year"],row["Month"],monthrange(row["Year"],row["Month"])[1]))
                if (row["Year"]<=2020):
                    hist[0]=1
            elif (row["Verdict"]=="UNBAN"):
                uubanhist[subject]["unbans"].append(datetime.date(row["Year"],row["Month"],monthrange(row["Year"],row["Month"])[1]))
                if (row["Year"]<=2020):
                    hist[0]=0
        m=0
        for d in uublusage.columns:
            for u in uubanhist[subject]["unbans"]:
                if d==u:
                    hist[m]=1
                    if m<17: hist[m+1]=0
            for b in uubanhist[subject]["bans"]:
                if d==b:
                    hist[m]=0
                    if m<17: hist[m+1]=1
            m+=1
        if hist[0]==-1:
            hist[0]=0
        for i in range(17):
            if hist[i+1]==-1:
                hist[i+1]=hist[i]
        isuubl[subject]=hist
    uubl=pandas.DataFrame.from_dict(data=isuubl,columns=uublusage.columns,orient="index")
    #deltauubl=uublusage.diff(1,1)
    print(uubl)
    #print(deltauubl)

    banlines={date:verdict+" "+subject for date, subject, verdict in zip(uubans["Date"],uubans["Subject"],uubans["Verdict"])
              if pandas.to_datetime(date).date()>=datetime.date(2021,1,1) and pandas.to_datetime(date).date()<datetime.date(2022,6,30)}
    
    uublrelevtimepd=[banlines[ban].split(" ")[1] for ban in banlines]
    uubltoplot=uublusage.loc[uublusage.index.isin(uublrelevtimepd)]
    p1=uubltoplot.transpose().plot(kind="line",xticks=dq)
    dmonths=pandas.date_range('2021-01-01','2022-07-01',freq="M")
    p1.set_xticks(dmonths,minor=True)
    p1.set_axisbelow(True)
    p1.legend(loc="upper left",ncol=5)
    p1.grid(True,which="both")
    plotlib.axhline(y=4.52,color="grey",linestyle="--")
    ymax=p1.get_ybound()[1]
    
    texty=7
    for ban in banlines:
        linecolor="red"
        if (banlines[ban][0]=="U"):
            linecolor="blue"
        plotlib.axvline(x=ban,ymax=texty/ymax,label=banlines[ban],color=linecolor)
        plotlib.text(ban,texty,banlines[ban])
        texty-=0.5
        if (texty<5):
            texty=7

    """banlines={date:subject+" "+verdict+"NED" for date, subject, verdict in zip(bans["Date"],bans["Subject"],bans["Verdict"])
              if pandas.to_datetime(date).date()>=datetime.date(2021,1,1) and pandas.to_datetime(date).date()<datetime.date(2022,6,30)}
    for ban in banlines:
        plotlib.axvline(x=ban,label=banlines[ban],linestyle="--")
        plotlib.text(ban,texty,banlines[ban],rotation=60)
        texty-=textoffset
        textoffset*=-1"""

    #print(deltatop50)
    """p1.set_xticks(dq)
    p1.set_xticks(top50.columns,minor=True)"""

    plotlib.show()
    return

testuublcorrelation()
