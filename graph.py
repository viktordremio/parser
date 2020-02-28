import csv
from graphviz import Digraph


#__package__ = ".package"
def drawGraph(tablaeuSource, onlyConnectedFileds):
    graphType=onlyConnectedFileds #no unconnceted fields
    single=True #single parent

    data=[]
    with open('output/'+tablaeuSource+'.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        data = list(reader)

    nodes=[]
    edges=[]


    for row in data:
        temp=[]
        temp.append(int(row[0]))
        if row[1]=="":
            name=row[2]
        else:
            name=row[1]

        temp.append(name)
        temp.append(row[3])
        
        single=True
        if(single==True):
            setParent=set()
            for parent in row[6].split(","):
                parent=parent.replace("[","")
                parent=parent.replace("]","")
                parent=parent.replace(" ","")
                setParent.add(parent)
            parents=setParent
        else:
            parents=row[6].split(",")
        
        

        for parent in parents:
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
            formula=formula.replace("<","&#60;")
            formula=formula.replace(">","&#62;")
            formula=formula.replace("\n"," ")
            formula=formula.replace("'"," ")
            formula=formula.replace(","," ")
            formula=formula.replace("'"," ")
            formula=formula.replace(","," ")
            formulaTemp=[]
            formulaTemp=formula.split(" ")
            
            n = 10
            ret = ''
            #print(len(formulaTemp))
            for i in range(0, len(formulaTemp), n):
                
                ret =ret+ str(formulaTemp[i:i+n]) +'<br/>'

                #print(ret)
            formula=ret
            #print('\n')
            formula=formula.replace("'","")
            formula=formula.replace(",","")
            formula=formula.replace("[","")
            formula=formula.replace("]","")
            print(formula)   
        temp.append(str(formula))
        #temp.insert(3, formula)
        #print(temp[3])
        nodes.append(temp)


    dot = Digraph(comment='Parent-Child')
    col="black"

    setOfEdges=set()

    for edge in edges:
        setOfEdges.add(edge[1])

    newNode=[]

    for node in nodes:
        
        if node[0] in setOfEdges:
            newNode.append(node)
        else:
            if (node[3]!="no calculation"):
                newNode.append(node)
    if (graphType==False):
        newNode=nodes


    for node in newNode:
       
        formula=str(node[3]).replace("'"," ")
        formula=formula.replace(","," ")
        formula=formula.replace(" ","")
        #print('\n')
        #print(node[3])
        if node[2]=="calculation":
            col="blue"
        else:
            col="green"
            
        dot.node(str(node[0]), 
        '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <TR>
                <TD>%s - %s</TD>
            </TR>
            <TR>
            <TD>%s</TD> 
            </TR>
            </TABLE>>''' % (str(node[0]), str(node[1]), formula), 
            shape="box", color=col)

    for edge in edges:
        dot.edge(str(edge[1]), str(edge[0]))

    dot.graph_attr['rankdir'] = 'LR'
    dot.graph_attr["pad"]="1"
    dot.graph_attr["nodesep"]="0.5"
    dot.graph_attr["ranksep"]="5"

    dot.render('output/'+tablaeuSource+'.gv', view=True) 

    # Extract gv 
    file = open("output/"+tablaeuSource+".gv", "w")
    file.write(dot.source)
    file.close