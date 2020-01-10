import xml.etree.ElementTree as ET
import csv

tree = ET.parse('src/2019_12-02 - Cost to Serve (Live) - DH - Local.twb')
root = tree.getroot()

for datasource in root.findall('datasources/datasource'):
    value = datasource.get('caption')
    columnId=0
    dict_calc={}
    all_calculation=[]

    if value == "customer_order_profile (ML Estimated)":
        for column in datasource.findall("column"):
            columnId=columnId+1
            c_value=column.get("name")
            c_caption=column.get("caption")
            dict_calc.update({columnId: c_value})
            dataset=[]

            for formula in column.findall("calculation"): 
                c_formula=formula.get("formula")
                amount=c_formula.count("[Calculation_")
                idx_s =[i for i in range(len(c_formula)) if c_formula.startswith("[", i)]
                idx_e =[i for i in range(len(c_formula)) if c_formula.startswith("]", i)]                
                id_calc_all=[]
                id_calc_pos=[]
                j=0

                for pos_start_all in idx_s:
                    pos_end_all=idx_e[j]
                    j=j+1
                    value_all=c_formula[pos_start_all:pos_end_all+1]
                    id_calc_all.append(value_all)
                    concat=str(pos_start_all) + "-" + str(pos_end_all)
                    id_calc_pos.append(concat)

            dataset.append(columnId)
            dataset.append(c_caption)
            dataset.append(c_value)
            dataset.append(amount)
            dataset.append(c_formula)
            dataset.append(id_calc_all)
            
            all_calculation.append(dataset)     

        final=[]

        #HEAD ROW FOR CSV
        head=[]
        head.append("id")
        head.append("caption")
        head.append("name")
        head.append("amount_parent_calculations")
        head.append("formula")
        head.append("names_of_parent")
        head.append("ids_of_parent")
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
            final.append(temp)

        with open("output/output.csv", 'w', newline='') as myfile:
            wr = csv.writer(myfile, delimiter=';')
            wr.writerows(final)              