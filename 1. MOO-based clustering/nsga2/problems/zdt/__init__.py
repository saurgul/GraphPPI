"""Module with definition of ZDT problem interface"""

from nsga2.individual import Individual
from nsga2.problems import Problem
from nsga2.problems.zdt.fcm import FCM

import time
import functools

class ZDT(Problem):

    def __init__(self, zdt_definitions, all_data_matrix, individual_no):
        self.zdt_definitions = zdt_definitions
        self.all_data_matrix = all_data_matrix
        self.individual_no= individual_no
        self.max_objectives = [None, None, None, None]
        self.min_objectives = [None, None, None, None]
        self.problem_type = None


    def __dominates(self, individual2, individual1):
        worse_than_other = individual1.objectives[0] >= individual2.objectives[0] and individual1.objectives[1] >= individual2.objectives[1] and individual1.objectives[2] >= individual2.objectives[2] and individual1.objectives[3] >= individual2.objectives[3]
        better_than_other = individual1.objectives[0] > individual2.objectives[0] or individual1.objectives[1] > individual2.objectives[1] or individual1.objectives[2] > individual2.objectives[2] or individual1.objectives[3] > individual2.objectives[3]
        return worse_than_other and better_than_other

    def generateIndividual(self):
        xy = FCM(self.all_data_matrix, self.individual_no)
        center, u, d ,fpc, no_of_cluster, label = xy.FuzzyCMeans()             #Generate each individual using Fuzzy C means
        individual = Individual()
        individual.partition_matrix = u
        individual.distance_matrix = d
        individual.no_of_Cluster = no_of_cluster
        individual.fpc = fpc
        individual.labels= label
        individual.silhoutte_score = self.zdt_definitions.silhoutte(individual)
        individual.features = []
        for sub_list in center:
                for feature in sub_list:
                    individual.features.append(feature)
        #print individual.no_of_Cluster , individual.features
        individual.dominates = functools.partial(self.__dominates, individual1=individual)
        self.calculate_objectives(individual)
        return individual

    def calculate_objectives(self, individual):
        individual.objectives = []
        individual.objectives.append(self.zdt_definitions.f1(individual))
        individual.objectives.append(self.zdt_definitions.f2(individual))
        individual.objectives.append(self.zdt_definitions.f3(individual))
        individual.objectives.append(self.zdt_definitions.f4(individual))
        #print "\n Hello I am Calculate Objectives";
        for i in range(4):
            if self.min_objectives[i] is None or individual.objectives[i] < self.min_objectives[i]:
                self.min_objectives[i] = individual.objectives[i]
                #print "min_obj", individual.objectives[i] , self.min_objectives[i]
            if self.max_objectives[i] is None or individual.objectives[i] > self.max_objectives[i]:
                self.max_objectives[i] = individual.objectives[i]
                #print "max_obj", individual.objectives[i], self.max_objectives[i]
