#Parses smogon usage stats

import pandas

def analyzefile(fname):
    file=open(fname,"r")
    write=open(fname+".csv","w")
    lines=file.readlines()[0:305]
    allmons=pandas.DataFrame(columns=["Rank","Mon","Raw","Real"])
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
        real=int(tokens[6])
        usage=raw*1.0/totalbattles
        #print("Got "+mon)
        allmons.loc[len(allmons.index)]=[rank,mon,raw,real]
        write.write(",".join([mon,tokens[1],str(usage)])+"\n")
    return allmons
    
def __main__():
    
    d2=analyzefile("stats/2023-09-DLC1/gen9ou-1695.txt")
    d1=analyzefile("stats/2023-10/gen9ou-1695.txt")
    d3=pandas.DataFrame(columns=["Mon","FellBelow100","RoseAbove100","Diff"])
    # for idx, entry1 in d1.iterrows():
    #     mon=entry1["Mon"]
    #     entry2=d2.loc[d2["Mon"]==mon]
    #     if (len(entry2)<1):
    #         d3.loc[len(d3.index)]=[mon,True,False,-100]
    #         continue
    #     diff=int(entry1["Rank"])-int(entry2["Rank"])
    #     rose=diff>100-int(entry1["Rank"])
    #     d3.loc[len(d3.index)]=[mon,False,rose,diff]
    print(d3)



__main__()
