# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:08:45 2013

@author: sunalliance

He - Desde el principio. Lo que estoy probando aca es si es posible
hacer los nodos como "abac" y despues convertirlos a numeros. 

Este es la ultima version del He
"""


from __future__ import division
from math import sqrt
import networkx as nx
import numpy as np
import collections
from string import maketrans #This I'm going to use to translate xyz, jkl


def he(years, n, s1, s2, sigma1, sigma2, rho, r):
    
    if n==0:
        return 0

    n=n*years
    rate = (1/(1+r))**(1/n)
    mu1=mu2=r
    
    #This are the formulae for the Asset 1
    x = 1 + mu1/n + sigma1*sqrt(3)/sqrt(2*n)
    y = 1 + mu1/n
    z = 1 + mu1 /n - sigma1*sqrt(3)/sqrt(2*n)
    
    #This are the formulae for the Asset 2
    j = 1 + mu2 /n + sigma2*rho*sqrt(3)/sqrt(2*n) + sigma2*sqrt(1-rho**2)/sqrt(2*n)
    k = 1 + mu2 /n - sigma2*sqrt(1-rho**2)*2/sqrt(2*n)
    l = 1 + mu2 /n - sigma2*rho*sqrt(3)/sqrt(2*n) + sigma2*sqrt(1-rho**2)/sqrt(2*n)

    constantes =['x','y','z']

    values_s1={'a':1,'x':x,'y':y,'z':z}
    values_s2={'a':1,'j':j,'k':k,'l':l}
    
    #this is used to translate between x->j , y->k, j->l 
    intab="axyz"; outtab="ajkl"


    G=nx.DiGraph() #I initiate the graph

    current_step_nodes=[]
    previous_step_nodes=[]
    total=0
    
    for step in range(0,n+1):
        #print "step -> {0}".format(step)
        previous_step_nodes = current_step_nodes
        #print "previous_step_nodes -> {0}".format(previous_step_nodes)
        if not current_step_nodes: #If there is no current nodes the is a 
            current_step_nodes = ['a']
            G.add_nodes_from(current_step_nodes)
        else:                
            current_step_nodes =[''.join(sorted(i + j)) for i in current_step_nodes for j in constantes]
            total = total + len(current_step_nodes)
            G.add_nodes_from(current_step_nodes)
            print len(G.nodes())
        
        print 'total = ' + str(total)
        #print "len current_step_nodes -> {0}".format(len(current_step_nodes))

        cu = current_step_nodes
        pr = previous_step_nodes
        
        i=0
        print 'Se agrega periodo = ' + str(i)
        while len(cu)>2:
            print 'len pr =' + str(len(pr))
            for nta in pr:
                G.add_edge(nta,cu[0])
                G.add_edge(nta,cu[1])
                G.add_edge(nta,cu[2])
                cu = cu[3::]
            i=i+1
            print 'Se agrega periodo = ' + str(i)
    



    #print "\n the tree is complete "
    print len(G.nodes())
    #print "\n Assign the values for both assets"
    # Now that the tree is complete. 
    # We assign the values to s1,s2,etc. This is very fast because is a dictionary
    for ns1 in G.nodes():
        #This is for the first asset
        val_s1 = '*'.join(list(ns1)) #this turns 'az' into 'a*z'
        products = eval(val_s1, globals(), values_s1) #this turns 'a*z' into a number
        G.node[ns1]['s1']=products
        
        #For the second asset
        val_s2 = '*'.join(ns1.translate(maketrans(intab, outtab)))
        products = eval(val_s2, globals(), values_s2)
        G.node[ns1]['s2']=products
        #I want to set the 'value' to zero here for all the nodes:
        G.node[ns1]['value']=0

           

    #set(current_step_nodes) this returns the leafs NO duplicates

    #This sets the values for the final nodes 
    for leafs in set(current_step_nodes):
        G.node[leafs]['value']=max(s1*G.node[leafs]['s1']-s2*G.node[leafs]['s2'],0)

    #total is the number of nodes. I can do G.nodes() but I'm going to drop them from
    #the list in the backward induction, so I want a copy of the nodes
    #print "Complete /n"
    #print "Start Backward Induction"

    total = G.nodes()
    #First, remove the leafs because I need to start from the previous nodes in the 
    # backward induction process. There are n steps + 0 = n+1
    total = [w for w in total if len(w) != n+1]

    # I do this reversed to start 3-2-1-0
    for i in reversed(xrange(n+1)):
        #print 'backward induction step -> {0}'.format(i)
        if i==0: #If 0 we brake, because remember 0 is [].
            break
        else:
            #nodes_in_i gets me the nodes in the time step i
            # the key is that is equal to the number of letters
            nodes_in_i = [w for w in total if len(w) == i]
            for node in nodes_in_i:
                for succ in G.successors(node):
                    #This calculates the value
                    G.node[node]['value']=G.node[node]['value']+G.node[succ]['value']
                G.node[node]['value'] = 1/3 * rate * G.node[node]['value']
    
    #print "End of Backward Induction /n"
    #Remember ['a'] is the root. 
    #print '\n The price of the option is {0}'.format(G.node['a']['value'])
    





    return G.node['a']['value']


    
def main(): 
 
    s1 = 200; s2=250
    sigma1= 0.3; sigma2= 0.2
    r=0.10; rho=0.75
    years = 1
    n=15
    print he(years, n, s1, s2, sigma1, sigma2, rho, r)


if __name__=='__main__':
    main()


