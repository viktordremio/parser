import csv
from graphviz import Digraph
from operator import itemgetter
import textwrap

data=[]
with open('output/output.csv', 'r') as f:
    reader = csv.reader(f, delimiter=";")
    next(reader)
    data = list(reader)
  
#print (data)
nodes=[]
edges=[]
#data.sort(key=itemgetter(3))

for row in data:
    temp=[]
    temp.append(int(row[0]))
    #replce_str=row[2].replace("[","")
    #replce_str=replce_str.replace("]","")
    if row[1]=="":
        name=row[2]
    else:
        name=row[1]

    #text=("ID: " , row[0],"-",name)

    temp.append(name)
    temp.append(row[3])


    for parent in row[6].split(","):
        temp_parent=[]
        parent=parent.replace("[","")
        parent=parent.replace("]","")
        parent=parent.replace(" ","")

        if parent!="":
            parent=int(parent)
            temp_parent.append(int(row[0]))
            temp_parent.append(parent)
            edges.append(temp_parent)
    formula="no calculation"
    if row[4]!="":
        formula=row[4]
        formula=formula.replace("\n","")
        formula=formula.replace("<","&#60;")
        formula=formula.replace(">","&#62;")
        formula=formula[0:50]

          
    temp.append(formula)
    nodes.append(temp)


dot = Digraph(comment='Parent-Child')
col="black"

for node in nodes:
    if node[2]=="calculation":
        col="blue"
    else:
        col="red"
    dot.node(str(node[0]), 
    '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD>%s - %s</TD>
            
        </TR>
        <TR>
           <TD>%s</TD> 
        </TR>
        </TABLE>>''' % (str(node[0]), str(node[1]), str(node[3])), shape="box", color=col)
    #dot.attr(str(node[0]), shape='box')
for edge in edges:

    dot.edge(str(edge[1]), str(edge[0]))
dot.graph_attr['rankdir'] = 'LR'

dot.render('output/parent-child.gv', view=True) 
#print(dot.source)