import matplotlib.pyplot as plt
import sys
from copy import deepcopy
import numpy as np
import re
from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
#value iteration
path=sys.argv[2]
f=open(path, 'r')
f=f.readlines()
num_states=int(f[0].split()[1])
num_actions=int(f[1].split()[1])
start_state=int(f[2].split()[1])
end_states=f[3].split()[1:len(f[3].split())]
end_states=[int(i) for i in end_states]
l=4
# P=[[[0 for _ in range(num_states)] for _ in range(num_actions)] for _ in range(num_states)]
P=np.zeros((num_states,num_actions,num_states))
# R=[[[0 for _ in range(num_states)] for _ in range(num_actions)] for _ in range(num_states)]
R=np.zeros((num_states,num_actions,num_states))
while(f[l].split()[0]=='transition'):
    #print(f[i].split())
    i=int(f[l].split()[1])
    j=int(f[l].split()[2])
    k=int(f[l].split()[3])
    R[i,j,k]=float(f[l].split()[4])
    P[i,j,k]=float(f[l].split()[5])
    l=l+1
mdtype=f[l].split()[1]
discount=float(f[l+1].split()[1])

if(sys.argv[4]=='vi'):
    # V_function=[0 for _ in range(num_states)]
    V_function=np.zeros((num_states))
    # policy=[0 for _ in range(num_states)]
    policy=np.zeros((num_states))
    V_function_new=np.zeros((num_states))
    epsilon=1E-11
    diff=1
    while(diff>epsilon):
        term2=np.dot(P,V_function)*discount
        # term1=[[0 for _ in range(num_actions)] for _ in range(num_states)]
        term1=np.zeros((num_states,num_actions))
        #term1=np.tensordot(P,R,)
        for i in range(num_states):
            for j in range(num_actions):
                term1[i,j]=np.dot(P[i,j,:],R[i,j,:])
        term=term1+term2

        policy=np.argmax(term,axis=1)
        V_function_new=np.amax(term, axis=1)
        diff=np.amax(abs(V_function_new-V_function),axis=0)
        V_function=V_function_new.copy()
    for i in range(num_states):
        print(V_function[i],policy[i])

    # print(re.sub(r' *\n *', '\n',np.array_str(np.c_[V_function, policy]).replace('[', '').replace(']', '').strip()))  # Regular expression operations



elif(sys.argv[4]=='hpi'):
    #Policy iteration
    V_function=[0.0 for _ in range(num_states)]
    policy=[0 for _ in range(num_states)]
    policy_new=[0 for _ in range(num_states)]
    V_function_new=[0.0 for _ in range(num_states)]
    epsilon=1E-11
    diff=1
    while True:
        term2=np.dot(P,V_function)*discount
        term1=[[0 for _ in range(num_actions)] for _ in range(num_states)]
        for i in range(num_states):
            for j in range(num_actions):                
                term1[i][j]=np.dot(P[i][j],R[i][j])
        term=term1+term2
        for s in range(num_states):
            V_function_new[s]=term[s][policy[s]]
        
        V_function_new=np.array(V_function_new)
        diff=np.amax(abs(V_function_new-V_function),axis=0)
        V_function=V_function_new.copy()
        policy_new=np.argmax(term,axis=1)
        if((policy == policy_new).all()) and (diff < epsilon):
            break
        policy=policy_new.copy()
    for i in range(num_states):
        print(V_function[i],policy[i])

elif(sys.argv[4]=='lp'):   
    model = LpProblem(name="problem", sense=LpMinimize)#model
    var=LpVariable.dict("V_fn",range(num_states))#num_states variables for value function of eevry state
    V = np.zeros((num_states), dtype = LpVariable)
    for i in range(num_states):
        V[i] = var[i]
    term2=np.dot(P,V)*discount
    # term1=[[0 for _ in range(num_actions)] for _ in range(num_states)]
    term1=np.zeros((num_states,num_actions))
    #term1=np.tensordot(P,R,)
    for i in range(num_states):
        for j in range(num_actions):
            term1[i,j]=np.dot(P[i,j,:],R[i,j,:])
    term=term1+term2
    for i in range(num_states):
        for j in range(num_actions):
            lowerBound = term[i,j]
            model += var[i] >= lowerBound
    model.solve()
    V = np.zeros((num_states))
    for i in range(num_states):
        V[i] = var[i].varValue
    for i in range(num_states):
        print(V[i],policy[i])