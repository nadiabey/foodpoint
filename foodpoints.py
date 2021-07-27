"""
Created on 11/17/2020

@author: nadia
"""

import pandas as pd
import matplotlib.pyplot as plt

dukecard = {}
trans = {}


def addtodict(dict,loc):
    if dict == dukecard:
        dict["Balance"] = 0
        dict["Spent"] = 0
    for x in loc:
        if "DukeCard" in x:
            pass
        elif x not in dict:
            dict[x] = 0
        else:
            pass
    return dict


def amounts(data):
    """
    return dollar amount in dataframe as float
    """
    usd = data['Amount']
    for x in usd:
        if isinstance(x,float):
            pass
        elif "(" in x:
            money = float(x[x.index("(")+1:x.index(")")])
            usd.replace(to_replace=x, value=money,inplace=True)
        elif "," in x:
            money = float(x[0:x.index(",")] + x[x.index(",")+1:x.index("USD")])
            usd.replace(to_replace=x,value=money,inplace=True)
        else:
            money = float(x[:x.index("USD")])
            usd.replace(to_replace=x, value=money,inplace=True)
    return data


def balances(data):
    """
    add credit to balance in dict, subtract credit from location unless dukecard
    add debit to location in dict, subtract from balance
    """
    k = amounts(data)
    for index, row in k.iterrows():
        if row.iloc[4] == "Credit":
            if "DukeCard" in row.iloc[3]:
                dukecard["Balance"] += row.iloc[5]
            else:
                dukecard["Balance"] += row.iloc[5]
                dukecard[row.iloc[3]] -= row.iloc[5]
                dukecard["Spent"] -= row.iloc[5]
        elif row.iloc[4] == "Debit":
            if "DukeCard" in row.iloc[3]:
                pass
            else:
                dukecard["Balance"] -= row.iloc[5]
                dukecard[row.iloc[3]] += row.iloc[5]
                dukecard["Spent"] += row.iloc[5]
    for d, v in dukecard.items():
        dukecard[d] = round(v,2)
    return dukecard


def count_transactions(data):
    """
    count number of transactions at location
    if datetime of subsequent transactions at same location are <2 minutes apart, return one trans
    """
    loc = data['Location']
    addtodict(trans,loc)
    for i in range(len(loc) - 2):
        current = loc[i]
        if "DukeCard" in current:
            i += 1
        else:
            trans[current] += 1
    return trans


def condense2(dict):
    final = {}
    places = {"Au Bon Pain": "Au Bon Pain", "Loop": "The Loop", "McD": "McDonald's", "Pitchfork": "Pitchfork's",
              "Pegram": "Pegram Vending", "Hollows": "Hollows Vending", "Carr": "Classroom Vending",
              "House BB": "Magnolia Vending", "Il Forno": "Il Forno", "Beyu": "Beyu Blue",
              "Marketplace": "Marketplace", "Trinity": "Trinity Cafe", "The Cafe": "Cafe",
              "Divinity": "Divinity Cafe", "Perk": "Vondy (Saladelia)", "Skillet": "Skillet",
              "Farmstead": "Farmstead", "Sprout": "Sprout", "Lobby": "Lobby Shop"}
    if dict == dukecard:
        final["Balance"] = dict["Balance"]
        final["Spent"] = dict["Spent"]
    for k,v in dict.items():
        for p,l in places.items():
            if p in k:
                if places[p] not in final:
                    final[places[p]] = 0
                    final[places[p]] += v
                else:
                    final[places[p]] += v
    ret = {key: round(val,2) for key, val in final.items()}
    return ret


def bargraph(dict):
    d = condense2(dict)
    x = [k for k,v in d.items()]
    y = [v for k,v in d.items()]
    if dict == dukecard:
        x = x[2:]
        y = y[2:]
    plt.bar(x,y)
    plt.show()

# write func to match timestamp to standardized name of place
# correct graphs so labels fit


if __name__ == '__main__':
    years = {"2019-2020": ["foodpointsfall19.csv","foodpointsspring20.csv"],
             "2020-2021": ["foodpointsfall20.csv","foodpointsspring21.csv"]}
    files = []
    frames = []
    final = pd.DataFrame({0, 0, 0})
    balance = 0
    sem = ""
    pick_year = input("Type the academic year in the format XXXX-XXXX, or type 'all': ")
    if pick_year in years.keys():
        for x in years[pick_year]:
            files.append(pd.read_csv(x))
        sem = input("fall, spring, year: ")
        if sem == "fall":
            # file = pd.read_csv(years[pick_year][0]])
            # files.append(file)
            addtodict(dukecard,files[0]['Location'])
            frames.append(files[0])
        elif sem == "spring":
            # file = pd.read_csv(years[pick_year][1])
            # files.append(file)
            addtodict(dukecard,files[0]['Location']) # add to dict to get balance
            bal = balances(files[0])
            balance = dukecard['Balance'] # get balance of fall
            dukecard.clear()
            addtodict(dukecard, files[1]['Location'])
            frames.append(files[1])
        elif sem == "year":
            for f in files:
                addtodict(dukecard,f['Location'])
                frames.append(f)

    elif pick_year == "all":
        for k in years.keys():
            for x in years[k]:
                addtodict(dukecard,pd.read_csv(x)['Location'])
                frames.append(pd.read_csv(x))

    # for f in files:
    #    addtodict(dukecard,f['Location'])
    #    frames.append(f)

    if len(frames) > 1:
        final = pd.concat(frames, ignore_index=True)
    else:
        final = frames[0]
    # df['Date/Time'] = convert_time(df['Date/Time'])
    # bal1 = condense2(balances(df1))
    # bal2 = condense2(balances(df2))
    ret = balances(final)
    if sem == "spring":
        ret['Balance'] += balance
    tra = count_transactions(final)
    print(ret, '\n', tra)
    # bargraph(dukecard)
