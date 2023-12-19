import pandas
from statsparse import *

actiontypes=["BAN","UNBAN"]

AllActions=pandas.read_csv("stats/bans.csv")

def getByDates(gen=0,y1=0,y2=0,m1=0,m2=0,tier=OU):
    if (gen==0):
        print("Just call AllActions directly you fucking retard")
        return AllActions
    elif (y1==0 and y2==0 and m1==0 and m2==0):
        return AllActions.loc[AllActions["Gen"]==gen]
    elif (y1>=2016):
        if (y2==0):
            return AllActions.loc[AllActions["Year"]==y1]
        elif (y2>y1):
            if (m2==0):
                return AllActions.loc[(AllActions["Year"]>=y1)and(AllActions["Year"]<y2)]
            else:
                return AllActions.loc[(AllActions["Year"]>=y1)and(AllActions["Month"]>=m1)or(AllActions["Year"]<y2)or(AllActions["Year"])and(AllActions["Month"]<=m2)]
    return AllActions