# SimSUOG (In-Use Track / Submission #4202)

We present SimSUOG, a hybrid graph-based semantic measure for the similarity of prenatal phenotypes during pregnancy utrasound.

The supplementary resources are composed of:

## Core (Python files):

* **DomainOntology**: implements a wrapper for the Domain ontology.
* **OntologyGraph**: transforms the owl ontology into hirarchical graph composed of nodes and edges
* **EntitiesSelection**: selects randomly a set of entities from the domain ontology to assess their similarity
* **EntitiesSimilarityComputation**: computes the semantic similarity of the selected entities
* **ImageSimilarityComputation**: computes the similarity of the annotated images located in `csv/3.63` directory
* **PhenotypesSelectionHPO**: selects randomly a set of entities from HPO to assess their similarity

## CSV files:

It contains the CSV files used as input and generated as output.
* The annotations of images are located in `csv/3.63`
* The similarity results of phenotypes and disorders are located in `uc1` 
* The similarity results of images are located in `uc2` 


## Ontology:


## Experts evaluation:


## Diagrams:




