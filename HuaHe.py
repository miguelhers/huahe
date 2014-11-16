# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 13:08:45 2013

@author: Miguel Herschberg

He - This implementation of the He tree works the following way:
    'a' = root of the tree
    'ax, ay, az' = second step
    'axx, axy,axz, axy,ayy,ayz, axz,ayz,azz = third step

Note that every item in the list must be sorted alphabetically because I want
Networkx to recognize say 'axy' and 'ayx' as the same node.

At each step in the graph, I use two arrays to hold the current step nodes and
the previous step nodes. For example:
    
    previous_step = [ax, ay, az]    
    current_step = [axx, axy, axz,  axy, ayy, ayz,  axz,ayz,azz]

To add the nodes/edges to the tree, I do a for loop which does:

for node in previous_step:
    add the nodes/edges [(ax, axx), (ax, axy), (ax, axz)] to the graph
    pop these 3 elements from current_step: current_step = current_step[3::]

Once the tree is built, G.node[node]['s1'] stores the information for the 
first asset and similarly  G.node[node]['s2'] for the second asset. 

For every node G.node[node]['s1'] is calculated doing:
    
    string('axy') -> string('a*x*y') -> float(a*x*y) = G.node['axy']['s1'] 

The backward induction is done recursively by changing each node's value:
G.node[node]['value']

"""


from __future__ import division
from math import sqrt
import networkx as nx
# This is used to translate xyz to jkl for the second asset
from string import maketrans 


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

        while len(cu)>2:
            print 'len pr =' + str(len(pr))
            for nta in pr:
                G.add_edge(nta,cu[0])
                G.add_edge(nta,cu[1])
                G.add_edge(nta,cu[2])
                cu = cu[3::]

    
    #print "\n the tree is complete "
    print len(G.nodes())
    #print "\n Assign the values for both assets"
    # Now that the tree is complete. We assign the values to s1,s2,etc. 
    for ns1 in G.nodes():
        #This is for the first asset
        val_s1 = '*'.join(list(ns1)) #this turns 'az' into 'a*z'
        #turns 'a*z' into a number
        products = eval(val_s1, globals(), values_s1) 
        G.node[ns1]['s1']=products
        
        #For the second asset
        val_s2 = '*'.join(ns1.translate(maketrans(intab, outtab)))
        products = eval(val_s2, globals(), values_s2)
        G.node[ns1]['s2']=products
        #I want to set the 'value' to zero here for all the nodes:
        G.node[ns1]['value']=0



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


