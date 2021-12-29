#Author: Samuel(Jong Shen) Lee 

#For this challenge, I used the Knuth's 5-Step approach. From Wikipedia:
#Create the set S of 1296 possible codes (1111, 1112 ... 6665, 6666)
#Start with initial guess 1122 (Knuth gives examples showing that this algorithm using other first guesses such as 1123, 1234 does not win in five tries on every code)
#Play the guess to get a response of coloured and white pegs.
#If the response is four colored pegs, the game is won, the algorithm terminates.
#Otherwise, remove from S any code that would not give the same response if it (the guess) were the code.

#Due to the time constraint with each guess, the minimax technique is not used, instead opting for random guessing. 
#For level 4, the amount of permutations took a longer time than allowed.
#Therefore, the same 5-step approach is used to narrow down the correct range of weapons based on combinations rather than permutations.
#The code is not perfect, but it gets through all the levels the majority of the time. 

import requests, json, sys, random, itertools
if sys.version_info < (3,0):
  sys.exit('Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.')
email = 'jongshenlee@gmail.com' # Change this!
r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email':email})
r.json()
# > {'Auth-Token': 'AUTH_TOKEN'}
headers = r.json()
headers['Content-Type'] = 'application/json'
z = requests.post('https://mastermind.praetorian.com/reset/', headers=headers)
PATH = 'https://mastermind.praetorian.com/level/'
maxRounds = 0


####API Related Functions####
    
#Submits a post request with a guess
def PostGuess(i, level):
    r = requests.post(PATH+level, data=json.dumps({'guess':i}), headers=headers)
    print(r.json())
    return r.json()

#Submits a get request to get game information
def interacting(level):
    # Interacting with the game
    i = requests.get(PATH+level, headers=headers)
    print(i.json())
    return i

#Reads json file for number of weapons
def getWeapons(i):
    Glad = i.json()
    return Glad['numWeapons']

#Reads json file for number of rounds/rounds left
def getRounds(i):
    Glad = i.json()
    if 'numRounds' in Glad:
       return Glad['numRounds']
    if 'roundsLeft' in Glad:
        return Glad['roundsLeft']

#Gets resulting hash at the end of the game
def getHash():
    i = requests.get('https://mastermind.praetorian.com/hash/', headers=headers)
    Glad = i.json()
    return Glad['Hash']

#Gets number of gladiators
def getGlad(i):
    Glad = i.json()
    return Glad['numGladiators']

#Generate list of possible numWeapons
def getPosSol(i):
    possible_weapons = list(range(getWeapons(i)))
    return possible_weapons

#Generate all possible permutations 
def getAllPossible(i, WepRange):
    out = []
    for x in list(itertools.permutations(WepRange, getGlad(i))):
        out.append(tuple_to_list(x))
    return out

#Reads the response after a guess
def getResponse(i):
     Glad = i
     if 'response' in Glad:
        return Glad['response']
     if 'message' in Glad:
         return Glad['message']
     if 'hash' in Glad:
         return Glad['hash']
     if 'roundsLeft' in Glad:
        return Glad['roundsLeft']

#Converts from a tuple to a list
def tuple_to_list(t):
    to_list = []
    for x in t:
        to_list.append(x)
    return to_list

#Compares the guess and gets a response. 
#Then, we remove all permutations from set S that does not yield the same response when compared to the guess.
def CompareGuess(guess,possible,response):
    new_set=[]
    for x in possible:
        tempResponse=[0,0]
        for y in range(len(x)):
            for z in range(len(guess)):
                if (x[y] == guess[z]):
                    tempResponse[0]=tempResponse[0] + 1
                    if(y==z):
                        tempResponse[1]=tempResponse[1] + 1
                    #else:
                        #tempResponse[0]=tempResponse[0] + 1
        if tempResponse == response:
           new_set.append(x)
    return new_set



####Functions specific to Level 4####

#Lvl 4: Generates all possible cominations
def Lvl4getAllPossible(i, level, WepRange):
    out = []
    for x in list(itertools.combinations(WepRange, getGlad(i))):
        out.append(tuple_to_list(x))
    return out

#Compares the guess and gets a response. 
#Then, we remove all combinations from set S that does not yield the same response when compared to the guess.
def Lvl4CompareGuess(guess,possible,response):
    new_set=[]
    for x in possible:
        tempResponse=[0,0]
        for y in range(len(x)):
            for z in range(len(guess)):
                if (x[y] == guess[z]):
                    tempResponse[0]=tempResponse[0] + 1
                    #else:
                        #tempResponse[0]=tempResponse[0] + 1
        if tempResponse[0] == response[0]:
           new_set.append(x)
    return new_set

#Based on the combinations remaining, we get a list of all possible weapons left. 
#The amount of weapons would be greatly reduces.
def lvl4RemainWeapons(possible):
    remain = []
    for x in possible:
        for y in x:
            if y not in remain:
                remain.append(y)
    return remain

#Main Function
def main(lev):
    print('Level: '+str(lev))
    level = str(lev) + '/'
    i = interacting(level)
    possible = []
    remainwep = getPosSol(i)
    global maxRounds
    if (lev == 4): #For Level 4, we use level 4 specific function to solve.
        possible = Lvl4getAllPossible(i, level, remainwep)
        guess = random.choice(possible)
        response = getResponse(PostGuess(guess, level))
        newSet = Lvl4CompareGuess(guess,possible,response)
        remainwep = lvl4RemainWeapons(newSet)
        print(guess)
        while (len(remainwep) > 10):
            guess = random.choice(newSet)
            print(guess)
            response = getResponse(PostGuess(guess, level))
            newSet = Lvl4CompareGuess(guess,newSet,response)
            remainwep = lvl4RemainWeapons(newSet)
        possible = getAllPossible(i, remainwep)
        guess = random.choice(possible)
        #print(getResponse(PostGuess(guess)))
        response = getResponse(PostGuess(guess, level))
        newSet = CompareGuess(guess,possible,response)
        while (response != 'Onto the next level'):
            guess = random.choice(newSet)
            print(guess)
            response = getResponse(PostGuess(guess, level))
            newSet = CompareGuess(guess,newSet,response)
    
    else:
        possible = getAllPossible(i, remainwep)
        guess = random.choice(possible)
        print(guess)
        response = getResponse(PostGuess(guess, level))
        newSet = CompareGuess(guess,possible,response)
        if(getRounds(i) == 1): #Allows for multiple rounds in level 5
            while (response != 'Onto the next level'):
                guess = random.choice(newSet)
                print(guess)
                response = getResponse(PostGuess(guess, level))
                newSet = CompareGuess(guess,newSet,response)
        else:
            if (maxRounds == 0):
                maxRounds = getRounds(i)
            currentRound = maxRounds
            while (maxRounds == currentRound and response != 'Onto the next level'):
                guess = random.choice(newSet)
                print(guess)
                response = getResponse(PostGuess(guess, level))
                if(type(response)==int):
                    currentRound = response
                newSet = CompareGuess(guess,newSet,response)
                print(maxRounds)
                print(currentRound)
            maxRounds = maxRounds - 1
    if (getRounds(i) == 1 or response == 'Onto the next level'):
        main(lev + 1)
        maxRounds = 0
    else:
        main(lev)

main(1)
