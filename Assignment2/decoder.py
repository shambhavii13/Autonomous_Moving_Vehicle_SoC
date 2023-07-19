import matplotlib.pyplot as plt
import sys
from copy import deepcopy
import numpy as np
import re
path=sys.argv[2]
f=open(path, 'r')
f=f.readlines()
numState=0
Actions=['N','E','S','W']
states=[]
for i in range(len(f)):
    for j in range(len(f[0])):
        if(f[i][j]=='0'or f[i][j]=='2' or f[i][j]=='3'):
            numState=numState+1
            states.append([i,j])
        if(f[i][j]=='2'):
            start=numState-1
            startState=[i,j]
        if(f[i][j]=='3'):
            end=numState-1
            endState=[i,j]
path=sys.argv[4]
g=open(path, 'r')
g=g.readlines()

policy=[]
state=startState.copy()
stateIndex=start
for i in range(len(g)):
    policy.append(int(g[i].split()[1][0]))
actiontaken=[]
# actiontaken.append(Actions[policy[start]])
while(state!=endState):
    stateIndex=states.index(state)
    actiontaken.append(Actions[policy[stateIndex]])
    if(policy[stateIndex]==0):
        state=[state[0]-1,state[1]]
    elif(policy[stateIndex]==1):
        state=[state[0],state[1]+2]
    elif(policy[stateIndex]==2):
        state=[state[0]+1,state[1]]
    elif(policy[stateIndex]==3):
        state=[state[0],state[1]-2]
print (*actiontaken, sep=" ")
