#
#  Copyright (c) 2022 - The ... Project.
#  @Author: ...
#

#
#
from core import OntologyGraph, DomainOntology
import numpy as np
import csv
import time
from datetime import date


####### Computing the similarity of annotated images ######

src="ontology/suog_ontology_v3.63_test.owl"
onto= DomainOntology.DomainOnto(src)
og = OntologyGraph.DomainOntologyTransform(src)
tax= OntologyGraph.Taxonomy(og)

listimages=[]
imagesdict2={}
imagesid=[]
previous=[]

file='csv/3.63/annotations_complete_test_1.csv'

with open(file, mode='r') as infile:
    reader = csv.reader(infile)
    for r in reader:
        print(r)
        listimages.append(r)

for i in listimages:
 #print(i)
 #print(i[1],i[2])
 test=str(i[0])[25:]
 imageid=str(i[1])[25:]
 print('image id:', imageid)

 #imageid2=imageid
 imagesid.append(imageid)
 imagesdict2[imageid] = {}
 imagesdict2[imageid]['test'] = (i[0]).split(',')
 imagesdict2[imageid]['findings'] = (i[2]).split(',')
 imagesdict2[imageid]['disorders'] = (i[3]).split(',')
 imagesdict2[imageid]['modes'] = (i[4]).split(',')
 imagesdict2[imageid]['routes'] = (i[5]).split(',')
 imagesdict2[imageid]['views'] = (i[6]).split(',')

for i in imagesdict2.items():
 print((i[1]['findings']))

imagesim = []

similarity = 0
simfindings = 0
simdisorders = 0
simroutes=0
simviews=0
simmodes=0
simtech = 0


measurex='lin'
counter1=0
counter2=0
today = date.today()
d=str(today)

with open('csv/3.63/results/similarity_images_'+measurex+'_Testing_MEAN_3.63_'+d+'.csv', 'w', newline='', encoding="utf-8") as file:
    start = time.time()
    measure=tax.sim_ic

    writer = csv.writer(file, delimiter=',')
    writer.writerow(["Ultrasound Study 1","Image ID 1","Annotations 1","Ultrasound Study 2","Image ID 2","Annotations 2","SimFindings","SimDisorders","SimRoutes","SimModes",
                     "SimViews","Similarity MEAN","Ultrasound Image1","Ultrasound Image 2"])
    for image1 in imagesdict2.items():

        imagesim = []
        imageid1 = image1[0]
        test1=image1[1]['test']
        print('imageid1',imageid1)
        counter1+=1
        counter2=0
       # imagesim.append(imageid1)

        for image2 in imagesdict2.items():

          imageid2 = image2[0]
          test2 = image2[1]['test']

          #print('imageid2', imageid2)
         # print('previous:', previous)
          #print('>>>>>>>>>>>>>>>>>>>>>>>>>>Similarity computation of:', tuple((imageid1,imageid2)))
          if(previous.__contains__(tuple((imageid1,imageid2)))==False and
                  previous.__contains__(tuple((imageid2,imageid1)))==False):


            if (imageid1 == imageid2):
                similarity = 1
                #imagesim.append((imageid1,imageid2,1))
                #previous.append((imageid1,imageid2))
            else:
                counter2+=1
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Similarity computation of image1:',counter1,'- image2:',counter2)
                print('FINDINGS')
                print(image1[0], image1[1]['findings'], image2[0], image2[1]['findings'])
                findings1 = image1[1]['findings']
                findings2 = image2[1]['findings']
                anatomicalfindings=onto.search_one("UF1220")

                annot2 = []
                annot1 = []
                flabel1 = ""
                dlabel1 = ""
                rlabel1 = ""
                vlabel1 = ""
                mlabel1 = ""

                flabel2 = ""
                dlabel2 = ""
                rlabel2 = ""
                vlabel2 = ""
                mlabel2 = ""
                for f1 in findings1:
                    f11=f1[25:]
                    #print(onto.get_Label(f11))
                    flabel1+="-"+str(onto.get_Label(f11))
                for f2 in findings2:
                    f22=f2[25:]
                    flabel2+="-"+onto.get_Label(f22)
                annot1.append(flabel1)
                annot2.append(flabel2)

                if (findings1 == findings2 and findings1!=[''] and findings2!=['']):
                    simfindings = 1
                    print('similarity findings: ', findings1, findings2, simfindings)

                else:
                 if(findings1 != findings2 and (findings1==[''] or findings2==[''])):
                        simfindings = 0
                 else:
                  if(findings1 != findings2 and findings1!=[''] and findings2!=['']):
                    print('diff findings')
                    simf = []
                    for f1c in findings1:
                        for f2c in findings2:
                            x1=f1c[25:]
                            x2=f2c[25:]
                            f1cc=onto.search_one(x1)
                            f2cc=onto.search_one(x2)
                            super1=onto.subClassesOf(f1cc)
                            super2=onto.subClassesOf(f2cc)
                            if(super1==super2 and super1==anatomicalfindings):
                                simf.append(measure(f1cc, f2cc))
                                print('similarity findings: ', f1cc, f2cc, measure(f1cc, f2cc))


                            else:

                             simf.append(measure(f1cc, f2cc))
                             print('similarity findings: ',f1cc, f2cc, measure(f1cc, f2cc))
                    print('simf: ', simf)
                    simfindings = np.mean(simf)
                    print('mean sim findings: ', simfindings)

                    ####DISORDERS
                print('DISORDERS')
                print(image1[0], image1[1]['disorders'], image2[0], image2[1]['disorders'])

                disorders1 = image1[1]['disorders']
                disorders2 = image2[1]['disorders']
                for d1 in disorders1:
                    d11 = d1[25:]
                    # print(onto.get_Label(f11))
                    dlabel1 += "-" + str(onto.get_Label(d11))
                for d2 in disorders2:
                    d22 = d2[25:]
                    dlabel2 += "-" + onto.get_Label(d22)
                annot1.append(dlabel1)
                annot2.append(dlabel2)
                if (disorders1 == disorders2 and disorders1!=[''] and disorders2!=['']):
                    simdisorders = 1
                    print('similarity disorders: ',simdisorders)
                else:
                 if (disorders1 != disorders2 and (disorders1 == [''] or disorders2 == [''])):
                        simdisorders = 0
                 else:
                  if (disorders1 != disorders2 and disorders1 != [''] and disorders2 != ['']):
                    simd = []
                    for d1c in disorders1:
                        for d2c in disorders2:
                            x1 = d1c[25:]
                            x2 = d2c[25:]
                            d1cc = onto.search_one(x1)
                            d2cc = onto.search_one(x2)
                            simd.append(measure(d1cc, d2cc))
                            print('similarity disorders:',d1c, d2c, measure(d1cc, d2cc))
                    simdisorders = np.mean(simd)
                    print('mean sim disorders: ', simdisorders)

                print('MODES')
                print(image1[0], image1[1]['modes'], image2[0], image2[1]['modes'])

                modes1 = image1[1]['modes']
                modes2 = image2[1]['modes']
                for m1 in modes1:
                    m11 = m1[25:]
                    # print(onto.get_Label(f11))
                    mlabel1 += "-" + str(onto.get_Label(m11))
                for m2 in modes2:
                    m22 = m2[25:]
                    mlabel2 += "-" + onto.get_Label(m22)
                annot1.append(mlabel1)
                annot2.append(mlabel2)

                if (modes1 == modes2 and modes1 != [''] and modes2 != ['']):
                        simmodes = 1
                        print('similarity modes: ', simmodes)
                else:
                        if (modes1 != modes2 and (modes1 == [''] or modes2 == [''])):
                            simmodes = 0
                        else:
                            if (modes1 != modes2 and modes1 != [''] and modes2 != ['']):
                                simm = []
                                for d1c in modes1:
                                    for d2c in modes2:
                                        x1 = d1c[25:]
                                        x2 = d2c[25:]
                                        d1cc = onto.search_one(x1)
                                        d2cc = onto.search_one(x2)
                                        simm.append(measure(d1cc, d2cc))
                                        print('similarity modes:', d1c, d2c, measure(d1cc, d2cc))
                                simmodes = np.mean(simm)
                                print('mean sim modes: ', simmodes)
                print('ROUTES')
                print(image1[0], image1[1]['routes'], image2[0], image2[1]['routes'])

                routes1 = image1[1]['routes']
                routes2 = image2[1]['routes']
                for r1 in routes1:
                    r11 = r1[25:]
                    # print(onto.get_Label(f11))
                    rlabel1 += "-" + str(onto.get_Label(r11))
                for r2 in routes2:
                    r22 = r2[25:]
                    rlabel2 += "-" + onto.get_Label(r22)
                annot1.append(rlabel1)
                annot2.append(rlabel2)

                if (routes1 == routes2 and routes1 != [''] and routes2 != ['']):
                    simroutes = 1
                    print('similarity routes: ', simroutes)
                else:
                    if (routes1 != routes2 and (routes1 == [''] or routes2 == [''])):
                        simroutes = 0
                    else:
                        if (routes1 != routes2 and routes1 != [''] and routes2 != ['']):
                            simr = []
                            for d1c in routes1:
                                for d2c in routes2:
                                    x1 = d1c[25:]
                                    x2 = d2c[25:]
                                    d1cc = onto.search_one(x1)
                                    d2cc = onto.search_one(x2)
                                    simr.append(measure(d1cc, d2cc))
                                    print('similarity routes:', d1c, d2c, measure(d1cc, d2cc))
                            simroutes = np.mean(simr)
                            print('mean sim routes: ', simroutes)

                print('VIEWS')
                print(image1[0], image1[1]['views'], image2[0], image2[1]['views'])

                views1 = image1[1]['views']
                views2 = image2[1]['views']
                for v1 in views1:
                    v11 = v1[25:]
                    # print(onto.get_Label(f11))
                    vlabel1 += "-" + str(onto.get_Label(v11))
                for v2 in views2:
                    v22 = v2[25:]
                    vlabel2 += "-" + onto.get_Label(v22)
                annot1.append(vlabel1)
                annot2.append(vlabel2)
                if (views1 == views2 and views1 != [''] and views2 != ['']):
                    simviews = 1
                    print('similarity views: ', simviews)
                else:
                    if (views1 != views2 and (views1 == [''] or views2 == [''])):
                        simviews = 0
                    else:
                        if (views1 != views2 and views1 != [''] and views2 != ['']):
                            simv = []
                            for d1c in views1:
                                for d2c in views2:
                                    x1 = d1c[25:]
                                    x2 = d2c[25:]
                                    d1cc = onto.search_one(x1)
                                    d2cc = onto.search_one(x2)
                                    simv.append(measure(d1cc, d2cc))
                                    print('similarity views:', d1c, d2c, measure(d1cc, d2cc))
                            simviews = np.mean(simv)
                            print('mean sim views: ', simviews)

                simtech = ((0.1*simroutes + 0.3*simmodes + 0.6*simviews))

                if ((simfindings == 1 and simdisorders == 1 and simtech == 1) ):
                     similarity = 1

                else:
                    similarity =1-np.round(np.abs(np.log(0.4*simfindings +0.3*simdisorders + 0.3*simtech)),2)

                print('----Similarity result----:',test1,imageid1,test2, imageid2, similarity, simfindings, simdisorders, simtech)
                imagesim.append((test1,imageid1,annot1,test2,imageid2,annot2,simfindings, simdisorders, simroutes, simmodes, simviews,np.abs(similarity)))
                previous.append(tuple((imageid1,imageid2)))
                previous.append(tuple((imageid2,imageid1)))

                print(previous)

                elapsed_time = time.time() - start
                print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))


        for r in imagesim:
         writer.writerow(r)


