#
#  Copyright (c) 2022 - The ... Project.
#  @Author: ...
#

from abc import abstractmethod, ABCMeta
import networkx as nx
from core.DomainOntology import DomainOnto
import numpy as np


class OntologyTransform:

    __metaclass__ = ABCMeta

    @abstractmethod
    def transform(self):
        """return nodes, labels, and edges"""
        pass


class DomainOntologyTransform(OntologyTransform):

    """This class transforms owl ontology into hirarchical graph: nodes and edges"""


    def __init__(self,src):
     self.ontology= DomainOnto(src)
     self._root=self.ontology._root

    def transform(self):
        nodes = { n for n in self.ontology.listclass}
        labels = tuple([self.ontology.labelClassOf(value) for i, value in enumerate(self.ontology.listclass)])
        edges = []
        for i, node in enumerate(nodes):
            children = self.ontology.subClassesOf(node)
            children = [child for child in children if child in nodes]
            for child in children:
              edges.append((node, child))

        return nodes, labels, edges


class Taxonomy(object):

    def __init__(self, onto):

        self._nodes, self._labels, self._edges = onto.transform()
        self._node2id = {value: i for i, value in enumerate(self._nodes)}
        self._root=onto._root
        self._taxonomy = nx.DiGraph()
        self._hyponyms = {}
        self._hypernyms = {}
        self.leavesMax={}
        self.children={}
        self.build_graph()


    def build_graph(self):

        parents, children = zip(*self._edges)
        parents_set = set(parents)
        children_set = set(children)
        self.children=children_set

        not_children = []
        not_parent = []

        #parents that are not in children set
        for p in parents_set:
            if p not in children_set:
                not_children.append(p)

        # children that are not in parent set
        for p in children_set:
            if p not in parents_set:
                not_parent.append(p)
        self.leavesMax=not_parent
        self._taxonomy.add_nodes_from(self._nodes)

        # add taxonomical edges
        for parent, child in self._edges:
            self._taxonomy.add_edge(parent, child)

        # hyponyms and hypernyms
        for parent, child in self._edges:
            self._hyponyms.setdefault(parent,[]).append(child)

        for parent, child in self._edges:
            self._hypernyms.setdefault(child, []).append(parent)


    def root_children(self):
        return self.hyponyms(self._root)

    def is_directed(self):
        return self._taxonomy.is_directed()

    def max_leaves(self):
        return self.leavesMax.__len__()

    def hyponyms(self, node):
        return self._hyponyms[node] if node in self._hyponyms else []

    def hypernyms(self, node):
        return self._hypernyms[node] if node in self._hypernyms else []

    def is_parent(self,c1,c2):
        if(c1 in self.hypernyms(c2)):
            return True
        return False

    def shortest_path_length(self, node1, node2):
        length=0
        if(nx.has_path(self._taxonomy,node1,node2)):
            length=len(nx.shortest_path(self._taxonomy, node1, node2))
        #print(nx.shortest_path(self._taxonomy, node1, node2))
        return length

    def depth(self, node):
        return self.shortest_path_length(self._root, node)

    def max_depth(self, onto):
        depths=[]
        for c in onto.nodes:
           # print(c,self._root,self.shortest_path_length(c, self._root))
            depths.append(self.shortest_path_length(c, self._root))
        return max(depths)

    def lca(self,c1,c2):
        return nx.lowest_common_ancestor(self._taxonomy,c1,c2)

    def leaves(self,c):
        l=[]
        for h in self.hyponyms(c):
             if(h in self.leavesMax):
                l.append(h)
        return l

    def IC(self,x):

        """IC is computed using Sanchez's equation"""

        ic= -np.log((((self.leaves(x).__len__()) / (self.hypernyms(x).__len__()+1)) + 1) / (self.max_leaves() + 1))
        return ic

    def common_ancestors(self,c1,c2):
        listca=[]
        ac1=nx.ancestors(self._taxonomy,c1)
        ac2=nx.ancestors(self._taxonomy,c2)
        for a in ac1:
            if a in ac2:
                listca.append(a)
        return listca

    def siblings(self, c):
        sib = []
        for parent in self.hypernyms(c):
            for child in self.hyponyms(parent):
                if child != c:
                    sib.append(child)
        return sib


    def isparentsibling(self,c1,c2):
        p1=self.hypernyms(c1)
        p2=self.hypernyms(c2)
        for p in p1:
            for px in p2:
                if(self.issibling(p,px)):
                    return True
        return False

    def issibling(self,c1,c2):
        sib=self.siblings(c1)
        if(c2 in sib):
            return True
        return  False

    def issupersibling(self,c1,c2):
        p1=self.hypernyms(c1)
        for p in p1:
            if(self.issibling(p,c2)):
                return True
        return False

    def issuborsuperclassof(self,c1,c2):

        if(c1 in list(self._taxonomy.successors(c2)) or c2 in list(self._taxonomy.successors(c1))
        or c1 in list(self._taxonomy.predecessors(c2)) or c2 in list(self._taxonomy.successors(c1))):
         print("successorssss")

         return True

        return False



    def ca(self,c1,c2):

        return self.common_ancestors(c1,c2)


    def sim_suog(self,c1,c2):

       """For Sim_suog, the ontology graph is directed,  (line 51) self._taxonomy = nx.DiGraph()"""

       if(c1==c2):
           sim=1
       else:
        dist1 = self.shortest_path_length(self.lca(c1, c2), c1)
        dist2 = self.shortest_path_length(self.lca(c1, c2), c2)
        dist=(dist1+dist2)/2
        print('distance: ', dist1,dist2)
        print('lca: ',self.lca(c1,c2))

        ic = self.IC(self.lca(c1, c2))
        #print('IC: ',ic)
      # if(self.issuborsuperclassof(c1,c2)==True) :
       #     sim = np.abs(np.round((np.log((ic) / ((1 + 2*dist)))), 2))
       #else:
        sim = np.abs(np.round((np.log((ic) / (1 + dist))), 2))

       return sim


    def sim_suog_t(self,c1,c2):

       """sim_suog_t is a customized (beta) version of sim_suog for technical elements"""

       dist1 = self.shortest_path_length(self.lca(c1, c2), c1)
       dist2 = self.shortest_path_length(self.lca(c1, c2), c2)
       dist=(dist1+dist2)/2
       ic = self.IC(self.lca(c1, c2))
       if (self.issuborsuperclassof(c1, c2) == True or self.issibling(c1, c2) == True):

          sim = np.abs(np.round(np.log(((ic)/(1+dist)) / (self.ca(c1, c2).__len__())), 2))
       else:
          sim = np.abs(np.round(np.log(((ic) / (1 + dist)) / (self.ca(c1, c2).__len__()/2)), 2))

       return sim


    def sim_suog_anatomicalFinding(self, c1, c2):

       """sim_suog_anatomicalFinding is a customized (temporary) version of sim_suog for anatomical findings"""

       dist1 = self.shortest_path_length(self.lca(c1, c2), c1)
       dist2 = self.shortest_path_length(self.lca(c1, c2), c2)
       dist=(dist1+dist2)/2
       ic = self.IC(self.lca(c1, c2))
       sim = np.abs(np.round(np.log((ic)/(1+dist)/ (self.ca(c1, c2).__len__()))/2, 2))

       return sim




    def mica(self, c1,c2):
        listca=self.common_ancestors(c1,c2)
        root=self._root
        #listca.remove(root)
        print('common ancestors: ', listca, c1,c2)
        listic=[]
        listic2=[]
        for l in listca:
            ic=self.IC(l)
            print(l,ic)
            listic.append(ic)
            listic2.append(l)
        maxic=max(listic)
        index=listic.index(maxic)
        mica=listic2[index]

        return mica


    ################ graph-based semantic measures  #####################

    def sim_resnik(self,c1,c2):

        """For Sim_resnik, the ontology graph is directed,  (line 51) self._taxonomy = nx.DiGraph()"""
        sim=self.IC(self.mica(c1,c2))
        print('MICA (',c1,'-',c2,'): ',self.mica(c1,c2))

        return np.round(sim,2)


    def sim_lin(self,c1,c2):

        """For Sim_lin, the ontology graph is directed,  (line 51) self._taxonomy = nx.DiGraph()"""

        sim=np.round(((2*self.sim_resnik(c1,c2))/(self.IC(c1)+self.IC(c2))),2)
        #print('sim_LIN result:',sim)

        return sim


    def sim_ic(self, c1,c2):

        """For Sim_ic, the ontology graph is directed,  (line 51) self._taxonomy = nx.DiGraph()"""

        sim=self.sim_lin(c1,c2)*(1-(1/(1+self.sim_resnik(c1,c2))))
        print('sim_lin: ',self.sim_lin(c1,c2),"- sim_resnik: ", self.sim_resnik(c1,c2))

        return sim


    def sim_rada(self, c1, c2):

        """For Sim_rada, the ontology graph is not directed,  (line 51) self._taxonomy = nx.Graph()"""
        sim=np.round(1.0 / (self.shortest_path_length(c1, c2)),2)

        return sim