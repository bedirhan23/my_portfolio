import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
"""
x = range(0, 10)
y = range(0, 20, 2)

print("x: {} \ny: {}". format(x,y))
x_y = list(zip(x,y))
print("zipped: {}".format(x_y))

df = pd.DataFrame(data= x_y, columns=['x', 'y'])
print(df)"""

critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                               'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,\
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
          'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                           'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0},
          'Ali': {'Just My Luck': 1.0, 'You, Me and Dupree': 2.0, 'The Night Listener': 4.5, 'Superman Returns': 1.0,
                   'Snakes on a Plane': 4.5}}

#for key, val in critics.items():
#    print(key)

def sim_distance(prefs, person1, person2):
    si = {}

    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum([pow( prefs[person1][item] - prefs[person2][item], 2) for item in si])
    oklid = math.sqrt(sum_of_squares)
    print(oklid)
    print(1/(1+oklid))


#sim_distance(critics, 'Mick LaSalle', 'Toby')
print("a")


def sim_pearson(prefs, person1, person2):
    si = {}

    for item in prefs[person1]:
        if item in prefs[person2]: si[item] = 1


    if len(si) == 0 : return 0

    n = len(si)
    # Sums of all the preferences
    sum1 = sum([prefs[person1][it] for it in si])
    sum2 = sum([prefs[person2][it] for it in si])

    # Sums of the squares
    sum1Sq = sum([pow(prefs[person1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[person2][it], 2) for it in si])

    # sum of the products
    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])

    #Calculate r (pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = math.sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) /n))

    if den == 0 : return  0

    r = num/den
    return  r

#sim_pearson(critics, 'Mick LaSalle','Toby')

def topMatches (prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]


    scores.sort()
    #scores.reverse()
    return  scores[0:n]

#topMatches(critics, 'Toby')

tamListe = {item for sublist in [list(x.keys()) for x in critics.values()] for item in sublist}
#print("Tum filmler: ", tamListe)
#print("Toby: ", list(critics['Toby'].keys()))

def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    rankings = []
    totalToplam = {}
    simSumToplam = {}
    filmIsimleri = []
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        sim = sim_pearson(prefs, person, other)

        #if sim <= 0 :
         #   continue
        for item in prefs[other]:
           # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

        #rankings = (total / simSums[item], item)
        
        for total in totals.items():
            if total[0] in filmIsimleri: 
                ar = 0
            else:
                filmIsimleri.append(total[0])
            totalToplam[total[0]] = totalToplam.get(total[0],float(0.0)) + (total[1] / simSums[total[0]])
            print(str(totalToplam.get(total[0], float(0.0))))
            simSumToplam[total[0]] = simSumToplam.get(total[0], 0) + 1
            print("Total 0: "+total[0]+" Total 1: "+str(total[1])+"  Simsums total 0:  "+str(simSums[total[0]])+" Sonuc: "+str(float(total[1] / simSums[total[0]])))

    for i in range(len(filmIsimleri)):
        print("Film : " + filmIsimleri[i] + " totaltoplam: " + str(totalToplam[filmIsimleri[i]]) + " simSumToplam: " + str(simSumToplam[filmIsimleri[i]]))
        rankings.append([filmIsimleri[i], totalToplam[filmIsimleri[i]] / float(simSumToplam[filmIsimleri[i]])])


    rankings.sort()
    rankings.reverse()
    return rankings

x = getRecommendations(critics,'Toby')

print(x)