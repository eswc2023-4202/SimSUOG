# SimSUOG (In-Use Track / Submission #4202)

We present SimSUOG, a hybrid graph-based semantic measure for the similarity of prenatal phenotypes during pregnancy utrasound.

The supplementary resources are composed of:

## Core (Python files):

* **DomainOntology**: implements a wrapper for the Domain ontology
* **OntologyGraph**: considers the ontology hirarchical graph and defines the semantic measures used in the study
* **EntitiesSelection**: selects randomly a set of entities from the domain ontology to assess their similarity
* **EntitiesSimilarityComputation**: computes the semantic similarity of the selected entities
* **ImageSimilarityComputation**: computes the similarity of the annotated images located in `csv/3.63` directory
* **PhenotypesSelectionHPO**: selects randomly a set of entities from HPO to assess their similarity

## CSV files:

It contains the CSV files used as input and generated as output.
* The annotations of images are located in `csv/3.63`
* The similarity results of phenotypes and disorders are located in `uc1` 
* The similarity results of images are located in `uc2` 
* The similarity results in HPO are located in `hpo`
* Additional results for different semantic measures are found in `other measures`


## Ontology:

In this directory, you will find the HPO ontology. Due to protection rights, unfortunately, we cannot yet publish our domain ontology.


## Experts evaluation:

The results of the experts evaluation. Three experts are involved in the evaluation process.


## Diagrams:

All the diagrams generated for the study.


## Main.py

The main file permits executing the similarity estimation of HPO terms. 
Due to the non-availability of our domain ontology, it is inaccessible to perform the image similarity computation.

