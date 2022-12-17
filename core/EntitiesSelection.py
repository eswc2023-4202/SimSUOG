#
#  Copyright (c) 2022 - The ... Project.
#  @Author: ...
#


from core import DomainOntology
import csv


#### Random selection of prenatal entities for similarity computation #####


onto= DomainOntology.DomainOnto("ontology/suog_ontology_v3.63_test.owl")

listentities=[]

#for e in onto.getDisorders():
for e in onto.getFindings():
    strd=str(e)[26 : ]
    listentities.append(e)

randomlist=listentities[1:200]

#print(randomlist)

with open('csv/excerpt_findings.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(randomlist)

