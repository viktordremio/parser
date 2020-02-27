# Parser of Tableau Workbook XML and vizualize as a graph of all calculated fields

1. Define in parser.py, where Tablaeu workbook is located by parameter tablaeuWorkBook = ET.parse('path/Tablaeu.twb')
2. Define in parser.py, which Dashboard of Tablaeu workbook should be analyzed by parameter tablaeuSource="name of Dashbaord"
3. Use xdot to visualize the gv file
4. Use https://github.com/hbmartin/graphviz2drawio to convert dot gv to xml and import to draw.io
