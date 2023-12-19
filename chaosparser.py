# Parse chaos json files

import pandas
import json
import numpy
import matplotlib.pyplot as plotlib

def usagetocsv(fname):
    file=open(fname,"r")
    write=open(fname+".csv","w")
    lines=file.readlines()[0:305]
    allmons=pandas.DataFrame(columns=["Rank","Mon","Weighted","Unweighted"])
    totalbattles= int(lines[0].split("battles: ")[1].strip())
    print("Total battles:",totalbattles)
    cutoff=totalbattles/.0452
    monlines=lines[5:]
    for line in monlines:
        tokens=[splitline.strip() for splitline in line.split("|")]
        if (len(tokens)<5):
            print(line+"<--- COULD NOT PARSE THESE STATS\n")
            continue
        rank=int(tokens[1])
        mon=tokens[2]
        raw=int(tokens[4])
        weighted=float(tokens[3].split("%")[0])
        unweighted=raw*100.0/totalbattles
        #print("Got "+mon)
        allmons.loc[len(allmons.index)]=[rank,mon,weighted,unweighted]
        write.write(",".join([mon,tokens[1],tokens[3].split("%")[0],str(unweighted)])+"\n")
    allmons.set_index("Mon",inplace=True)
    return allmons

def analyzecommonteammates(fname, mon):
    file=open(fname)
    alldata=json.load(file)
    header=alldata['info']
    print("Analyzing data from ",header["cutoff"]," ELO in ",header["metagame"]," across ",header["number of battles"],"battles")
    teammatedata=alldata["data"][mon]["Teammates"]
    #teamseries=[[key, teammatedata[key]] for key in teammatedata]
    #teamdf=pandas.DataFrame(teamseries)
    teamdf=pandas.DataFrame.from_dict(teammatedata,orient='index')
    teamdf.columns=["Usage"]
    return teamdf

def comparecommonteammates(f1, f2, pkmn, cutoff):
    df1=analyzecommonteammates(f1,pkmn)
    df2=analyzecommonteammates(f2,pkmn)
    top1=df1.nlargest(cutoff,"Usage")
    top2=df2.nlargest(cutoff,"Usage")
    topmons=set()
    for mon in top1.index.values:
        topmons.add(mon)
    for mon in top2.index.values:
        topmons.add(mon)
    topd={}
    for mon in topmons:
        if (not (mon in df1.index.values)):
            topd[mon]={"Usage1":0,"Usage2":df2.at[mon,"Usage"]}
        elif (not (mon in df2.index.values)):
            topd[mon]={"Usage1":df1.at[mon,"Usage"],"Usage2":0}
        else:
            topd[mon]={"Usage1":df1.at[mon,"Usage"],"Usage2":df2.at[mon,"Usage"]}
    topdf=pandas.DataFrame.from_dict(topd,orient='index')
    topdf["Mon"]=topdf.index
    p1=topdf.plot(kind='scatter',title='Teammates for '+pkmn,x="Mon", y="Usage1",color='r',rot=90,label="Usage for September")
    p2=topdf.plot(kind='scatter',x="Mon", y="Usage2",color='b',ax=p1,label="Usage for October")
    p1.set_xticklabels(labels=topdf["Mon"], rotation=90, size=10)
    p1.set_ylabel("Usage")

    plotlib.show()
    
    return topdf

def compareusage(usage1:pandas.DataFrame,usage2:pandas.DataFrame,mon:str):
    if (not (mon in usage1.index.values)):
        print(mon,"not found in this month")
        return "X","X"
    if (not (mon in usage2.index.values)):
        print(mon,"not found in this month")
        return "X","X"
    uw1=usage1.at[mon,"Unweighted"]
    uw2=usage2.at[mon,"Unweighted"]
    w1=usage1.at[mon,"Weighted"]
    w2=usage2.at[mon,"Weighted"]
    diffw=w1-w2
    diffuw=uw1-uw2
    print(mon,diffw)
    return diffw,diffuw

def compareintroduction(before,after,achaos,mon):
    usagebefore=usagetocsv(before)
    usageafter=usagetocsv(after)
    teammates=analyzecommonteammates(achaos,mon).nlargest(50,"Usage")
    wdiffs={}
    uwdiffs={}
    for teammate in teammates.index.values:
        wdiffs[teammate],uwdiffs[teammate]=compareusage(usagebefore,usageafter,teammate)
    teammates.insert(len(teammates.columns),"WDiff",wdiffs)
    teammates.insert(len(teammates.columns),"UWDiff",uwdiffs)
    print(teammates)

compareintroduction("stats/2023-10/gen9ou-1695.txt","stats/2023-08/gen9ou-1695.txt","stats/2023-10/chaos/gen9ou-1695.json","Gliscor")

#kingteammates=comparecommonteammates("stats/2023-10/chaos/gen9ou-1695.json", "stats/2023-09-DLC1/chaos/gen9ou-1695.json","Kingambit", 20)

