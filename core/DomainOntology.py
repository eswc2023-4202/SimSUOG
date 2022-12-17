#
#  Copyright (c) 2022 - The ... Project.
#  @Author: ...
#


from owlready2 import *

class DomainOnto(object):
    """this class implements a wrapper for the Domain ontology"""

    def __init__(self, src):

      self.onto = owlready2.get_ontology(src).load()
      self.classes = [s for s in self.onto.classes()]
      rootiri = 'http://purl.obolibrary.org/obo/HP_0000001'
      self.listclass=list(self.onto.classes())
      self.ontology=self.onto
      root = self.onto.search_one(iri=rootiri)
      self._root = root

    def is_a(self,c):
        return c.is_a

    def getInstances(self,c):
        list=c.instances()
        return list

    def search_one(self,c):
        return self.ontology.search_one(iri='*#'+c)

    def search(self, c):
        return self.ontology.search_one(iri=c)

    def search_label(self, c):
        return self.ontology.search_one(prefLabel='*'+c)

    def ancestorsOf(self,c):
        return c.ancestors()

    def subClassesOf(self,c):
        return list(c.subclasses())

    def descendantOf(self,c):
        return list(c.descendants())

    def getNote(self,c):
        return c.note

    def get_Label(self,irid):
        entity = self.ontology.search_one(iri='*#'+irid)
        return entity.prefLabel.en[0]

    def get_AltLabel(self,irid):
        return irid.altLabel

    def get_def(self,irid):
        return irid.UMLS

    def getDisorders(self):
        disorder_top = self.ontology.search(iri='*#FM0004*')

        return disorder_top[0].descendants()

    def getFindings(self):
        finding_top = self.ontology.search(iri='*#FM0001*')
        return finding_top[0].descendants()

    def descendants(self,c):
        return c.descendants()

    def labelClassOf(self,c):
       return c.label

    def prefLabelClassOf(self,c):
       return c.prefLabel

######## HPO #############

    def getPhenotypes(self, iri):
        finding_top = self.ontology.search(iri='*' + iri)
        print(finding_top[0].descendants())
        return finding_top[0].descendants()

    def get_Label_hpo(self,irid):
        entity = self.ontology.search_one(iri='*'+irid)
        return entity.label[0]

    def search_one_hpo(self, c):
        return self.ontology.search_one(iri='*' + c)