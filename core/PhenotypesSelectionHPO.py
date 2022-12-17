#
#  Copyright (c) 2022 - The ... Project.
#  @Author: ...
#


from core import DomainOntology
import csv

### Random selection of abnormal phenotypes from HPO ####

onto= DomainOntology.DomainOnto("ontology/hp.owl")

listphenotypes=[]

for d in onto.getPhenotypes('HP_0000118'):#phenotypic abnormality
    print('HPO phenoptype:  ', d)
    listphenotypes.append(d)

print(len(listphenotypes))
excerpt=listphenotypes[1:200]
print(excerpt)

with open('csv/hpo/excerpt_phenotypes_hpo.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(excerpt)
