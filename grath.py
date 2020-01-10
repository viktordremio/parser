import csv
from graphviz import Digraph
from operator import itemgetter

data=[]
with open('output/output.csv', 'r') as f:
    reader = csv.reader(f, delimiter=";")
    next(reader)
    data = list(reader)
  
#print (data)
nodes=[]
edges=[]
data.sort(key=itemgetter(3))

for row in data:
    temp=[]
    temp.append(int(row[0]))
    #replce_str=row[2].replace("[","")
    #replce_str=replce_str.replace("]","")
    temp.append(row[1])

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
    nodes.append(temp)


dot = Digraph(comment='Parent-Child')

for node in nodes:
    dot.node(str(node[0]), str(node[1]))

for edge in edges:

    dot.edge(str(edge[1]), str(edge[0]))
#dot.format = "png"
#dot.format = 'svg'
dot.graph_attr['rankdir'] = 'LR'

dot.render('output/parent-child.gv', view=True) 
#print(nodes)