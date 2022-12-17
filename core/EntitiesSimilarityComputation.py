#
#  Copyright (c) 2022 - The ... Project.
#  @Author: ...
#

from core import OntologyGraph, DomainOntology
import csv


class EntitiesSimilarity(object):

   """this class implements computing the semantic similarity of biomedical entities (prenatal phenotypes, abnormal phenotypes, etc.)"""

   def __init__(self, src, measure, inputfile, outputfile):

    self.onto= DomainOntology.DomainOnto(src)
    self.og = OntologyGraph.DomainOntologyTransform(src)
    self.tax= OntologyGraph.Taxonomy(self.og)
    self.similaritymeasure=measure
    self.entities=inputfile
    self.similarityresults=outputfile


   def computeSimilarity(self):

    listentities=[]
    listp1=[]
    listlabel=['x']

    with open(self.entities, "r") as f:
     reader = csv.reader(f, delimiter=',')
     for row in reader:
        listentities=row

    for d in listentities:
     #label=self.onto.get_Label_hpo(d[4:])
     #listlabel.append((label))
     #print(label)
     searchd=self.onto.search_one_hpo(d[4:])
     print(searchd)
     listp1.append(searchd)


    previous=[]
    with open(self.similarityresults, 'w', newline='', encoding="utf-8") as file:
     writer = csv.writer(file, delimiter=',')
     #writer.writerow(listlabel)
     for d1 in listp1:
      indexd=listp1.index(d1)
      #d1label=listlabel[indexd+1]
      similarityresult=[]
      #similarityresult.append(d1label)
      for d2 in listp1:
         if (previous.__contains__(tuple((d1, d2))) == False and
                 previous.__contains__(tuple((d2, d1))) == False):

             previous.append(tuple((d1, d2)))
             similaritydegree=self.tax.sim_suog(d1,d2)
             print(d1,d2,similaritydegree)
             similarityresult.append(similaritydegree)
             writer.writerow((d1,d2,similaritydegree))

