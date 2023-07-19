import matplotlib.pyplot as plt
import sys
from copy import deepcopy
import numpy as np
import re
path=sys.argv[2]
f=open(path, 'r')
f=f.readlines()
numState=0
numActions=4
states=[]
mdptype="episodic"
discount=0.9
transitions=[]
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
for i in range(len(states)):
    state=states[i]
    possibleNeighbours=[[state[0]-1,state[1]],[state[0],state[1]+2],[state[0]+1,state[1]],[state[0],state[1]-2]]
    for j in range(numActions):
        # print(possibleNeighbours[j])
        # print(endState)
        # print(end)
        if(possibleNeighbours[j]==endState):
            transitions.append((i,j,end,1.0,1.0))
        elif(possibleNeighbours[j] in states):
            transitions.append((i,j,states.index(possibleNeighbours[j]),-0.5,1.0))
        else:
            transitions.append((i,j,i,-1.0,1.0))
print("numStates",numState)
print("numActions",numActions)
print("start",start)
print("end",end)
for i in transitions:
    print("transition",i[0],i[1],i[2],i[3],i[4])
print("mdptype",mdptype)
print("discount",discount)




                  

