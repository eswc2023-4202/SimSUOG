#
#  Copyright (c) 2022 - The ... Project.
#  @Author: ...
#


import core.EntitiesSimilarityComputation as es

def main():
    src='ontology/hp.owl'
    measure='sim_suog'
    inputfile='csv/hpo/excerpt_phenotypes_hpo.csv'
    outputfile='csv/hpo/sim_SUOG_HPO.csv'

    entitiessimilarity=es.EntitiesSimilarity(src, measure, inputfile, outputfile)
    entitiessimilarity.computeSimilarity()



if __name__ == "__main__":
        main()