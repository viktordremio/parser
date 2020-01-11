import xml.etree.ElementTree as ET
import csv

tree = ET.parse('src/2019_12-02 - Cost to Serve (Live) - DH - Local.twb')
root = tree.getroot()

for datasource in root.findall('datasources/datasource'):
    value = datasource.get('caption')
    c_ID=0
    dict_calc={}
    all_calculation=[]
    
    if value == "customer_order_profile (ML Estimated)":
        for column in datasource.findall("column"):
            c_ID=c_ID+1
            c_name=column.get("name")
            c_caption=column.get("caption")
            c_role=column.get("role")
            dict_calc.update({c_ID: c_name})
            dataset=[]
            type_of_column="field"
            id_calc_all=[]

           
            if column.find("calculation")  is not None:
                c_formula=column.find("calculation").get("formula")
                #print(column.find("calculation").get("formula"))
                type_of_column="calculation"
                idx_s =[i for i in range(len(c_formula)) if c_formula.startswith("[", i)]
                idx_e =[i for i in range(len(c_formula)) if c_formula.startswith("]", i)]                
                
                j=0

                for pos_start_all in idx_s:
                    pos_end_all=idx_e[j]
                    j=j+1
                    value_all=c_formula[pos_start_all:pos_end_all+1]
                    id_calc_all.append(value_all)
            else:
                c_formula=column.find("calculation")
                #print(column.find("calculation"))
            
            dataset.append(c_ID)
            dataset.append(c_caption)
            dataset.append(c_name)
            dataset.append(type_of_column)
            dataset.append(c_formula)
            dataset.append(id_calc_all)
            dataset.append(c_role)
            #print(dataset)
            all_calculation.append(dataset)     

        final=[]

        #HEAD ROW FOR CSV
        head=[]
        head.append("id")
        head.append("caption")
        head.append("name")
        head.append("type_of_column_parent_calculations")
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
                for x, y in dict_calc.items():                 
                    if y==element:
                        dependencies.append(x)
                        break
                ids.append(dependencies)

            temp.append(ids)
            temp.append(calc[6])
            final.append(temp)
        
        with open("output/output.csv", 'w', newline='') as myfile:
            wr = csv.writer(myfile, delimiter=';')
            wr.writerows(final)              