#Useful functions and definitions for parsing showdown usage stats

STATPATH="stats/"

START_GEN7="2016-11"
GEN6_RENAME="2017-07"
START_USUM="2017-11"
START_GEN8="2019-11"
START_GEN8_DLC1="2020-06-DLC1"
START_GEN8_DLC2="2020-10-DLC2"
START_GEN9="2022-11"
START_GEN9_DLC1="2023-09-DLC1"

GEN_TO_YEAR=[
    [0],
    [1997,1998,1999],
    [2000,2001,2002],
    [2003,2004,2005,2006],
    [2007,2008,2009,2010],
    [2011,2012,2013],
    [2014,2015,2016],
    [2017,2018,2019],
    [2020,2021,2022],
    [2023,2024,2025,2026]
    ]


OU="ou"
UU="uu"
RU="ru"
NU="nu"
PU="pu"
ZU="zu"
UBER="ubers"
AG="anythinggoes"
UBERUU="ubersuu"
LC="lc"

NATDEX="nationaldex"

GENERATIONS=["nationaldex","gen1","gen2","gen3","gen4","gen5","gen6","gen7","gen8","gen9",""]

ELO_0=0
ELO_1=1500
ELO_2=1630
ELO_3=1760
ELO_2_OU=1695
ELO_3_OU=1825

def usagetocsv(filepath):
    print("Generating csv file for",filepath)
    txt=open(filepath+".txt","r")
    csv=open(filepath+".csv","w")
    csv.write("Mon,Rank,W,UW\n")
    lines=txt.readlines()
    totalbattles= int(lines[0].split("battles: ")[1].strip())
    cutoff=totalbattles/.0452
    monlines=lines[5:]
    for line in monlines:
        tokens=[splitline.strip() for splitline in line.split("|")]
        if (len(tokens)<5):
            continue
        mon=tokens[2]
        raw=int(tokens[4])
        unweighted=raw*100.0/totalbattles
        #print("Got "+mon)
        csv.write(",".join([mon,tokens[1],tokens[3].split("%")[0],str(unweighted)])+"\n")
    return filepath+".csv"

def getusagefile(year,month,gen=-1,tier=OU,elo=ELO_2_OU,seg=0):
    if (year<2016 or year==2016 and month<11):
        print("Months before the release of Sun and Moon (November 2016) are unsupported")
        return
    if (gen==-1):
        if (year>2022 or (year==2022 and month>=11)):
            gen=9
        elif (year>2019 or (year==2019 and month>=11)):
            gen=8
        elif (year>2016 or (year==2016 and month>=11)):
            gen=7
        else:
            print("WTF")
            return
    sg=""
    if (seg==2):
        sg="-H2"
    fpath=STATPATH+str(year)+"-"+str(month).zfill(2)+sg+"/"+GENERATIONS[gen]+tier+"-"+str(elo)
    csv=fpath+".csv"
    try:
        open(csv,"r")
    except FileNotFoundError:
        csv=usagetocsv(fpath)
    except Exception as e:
        print(e)
    finally:
        return csv
