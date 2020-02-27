import xml.etree.ElementTree as ET
import csv
from graph import drawGraph

# Requiered Define with Tablaeu Workbook should be analyzed
tablaeuWorkBook = ET.parse('src/2019_12-02 - Cost to Serve (Live) - DH.twb')
# Requiered Choose the Tab or Datasource from Tablaeu Workbook
tablaeuSource="customer_order_profile (ML Estimated)"

# Optional Do you wand to see only connceted Fields, when keep True?
onlyConnectedFileds=True

def parse():
    root = tablaeuWorkBook.getroot()
    for datasource in root.findall('datasources/datasource'):
        value = datasource.get('caption')
        print (value)
        columnID=0
        columnCollections={}
        all_calculation=[]
        if (value == tablaeuSource):
            for column in datasource.findall("column"):
                columnID=columnID+1
                columnName=column.get("name")
                columnCaption=column.get("caption")
                columnRole=column.get("role")
                columnCollections.update({columnID: columnName})
                dataset=[]
                typeOfColumn="field"
                idCalcColumnAll=[]

            
                if column.find("calculation")  is not None:
                    columnFormula=column.find("calculation").get("formula")
                    typeOfColumn="calculation"
                    idx_s =[i for i in range(len(columnFormula)) if columnFormula.startswith("[", i)]
                    idx_e =[i for i in range(len(columnFormula)) if columnFormula.startswith("]", i)]                
                    j=0

                    for pos_start_all in idx_s:
                        pos_end_all=idx_e[j]
                        j=j+1
                        valueAll=columnFormula[pos_start_all:pos_end_all+1]
                        idCalcColumnAll.append(valueAll)
                else:
                    columnFormula=column.find("calculation")
                
                dataset.append(columnID)
                dataset.append(columnCaption)
                dataset.append(columnName)
                dataset.append(typeOfColumn)
                dataset.append(columnFormula)
                dataset.append(idCalcColumnAll)
                dataset.append(columnRole)
                all_calculation.append(dataset)     
            final=[]

            #HEAD ROW FOR CSV
            head=[]
            head.append("id")
            head.append("caption")
            head.append("name")
            head.append("typeOfColumn_parent_calculations")
            head.append("formula")
            head.append("names_of_parent")
            head.append("ids_of_parent")
            head.append("role_of_column")
            final.append(head)
            
            for calc in all_calculation:
                temp=[]
                temp.append(calc[0])
                temp.append(calc[1])
                temp.append(calc[2])
                temp.append(calc[3])
                temp.append(calc[4])
                temp.append(calc[5])
                
                ids=[]

                for element in calc[5]:
                    dependencies=[]
                    for x, y in columnCollections.items():                 
                        if y==element:
                            dependencies.append(x)
                            break
                    ids.append(dependencies)

                temp.append(ids)
                temp.append(calc[6])
                final.append(temp)
            
            with open("output/"+tablaeuSource+".csv", 'w', newline='') as myfile:
                wr = csv.writer(myfile, delimiter=';')
                wr.writerows(final)  


if __name__== "__main__":
    parse()
    drawGraph(tablaeuSource, onlyConnectedFileds)