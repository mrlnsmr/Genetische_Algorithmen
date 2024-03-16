from math import *
import random

ziel = 128
population_size = 8
population = []
descendants = []
descendants_decimal = []
parents = []
parents_decimal = []
parent1 = []
parent2 = []
child1 = []
child2 = []
mutation_decision = ["yes", "no"]


#Beispiel
#Funktion: f(x) = -x*(x-256) --> Erreiche das Maximum der Funktion mit Genetischen Algorithmen


#Anfangspopulation erstellen
def generatePopulation():
    for i in range(population_size):
        population.append(random.randint(0,256))
    print("Deine Anfangspopulation lautet: ", population)


#Fitnessfunktion
def fitness_function(chromosome):
    return -chromosome * (chromosome - 256)
       
    
#Sortierung der x-Werte nach Fitness
def sorting(population):
    population.sort(key = fitness_function, reverse = True)
   

#Selektion (Wettkampf)
def selection(parents):
    tournament1 = random.choices(population, k = 3)
    while tournament1[0] == tournament1[1] or tournament1[0] == tournament1[2] or tournament1[1] == tournament1[2]:
        tournament1 = random.choices(population, k = 3)
    tournament2 = random.choices(population, k = 3)
    while tournament2[0] == tournament2[1] or tournament2[0] == tournament2[2] or tournament2[1] == tournament2[2]:
        tournament2 = random.choices(population, k = 3)
    tournament1.sort(key = fitness_function, reverse = True)
    tournament2.sort(key = fitness_function, reverse = True)
    while tournament1[0] == tournament2[0]:
        tournament2 = random.choices(population, k = 3)
        while tournament2[0] == tournament2[1] or tournament2[0] == tournament2[2] or tournament2[1] == tournament2[2]:
            tournament2 = random.choices(population, k = 3)
        tournament2.sort(key = fitness_function, reverse = True)
    parents.append(tournament1[0])
    parents.append(tournament2[0])
    print("Die Eltern sind", parents)

    tournament1.clear()
    tournament2.clear()


#Übersetzung in Binärcode
def deziintobinär(parents, parents_decimal):
    binary_number1 = bin(parents[0])
    binary_number2 = bin(parents[1])
    parents_decimal.append(binary_number1)
    parents_decimal.append(binary_number2)

    parents.clear()


#Binärzahlen in Liste übertragen
def transmission(parents_decimal, parent1, parent2):
    parent1.extend(list(parents_decimal[0]))
    parent2.extend(list(parents_decimal[1]))
    for i in range(2):
        del parent1[0]
        del parent2[0]

    parents_decimal.clear()


#Crossover (Two-point-crossover)
def crossover(parent1, parent2, child1, child2):
    #crossover Site
    crossSite1 = 2
    crossSite2 = 5

    if len(parent1) < len(parent2):
        while len(parent1) < len(parent2):
            parent1.insert(0, "0")
        for i in range(len(parent1)):
            child1.append(0)
            child2.append(0)

        for i in range(len(parent2)):
            if i >= crossSite1 and i <= crossSite2:
                child1[i] = parent2[i]
                child2[i] = parent1[i]
            
            else:
                child1[i] = parent1[i]
                child2[i] = parent2[i]

    elif len(parent1) > len(parent2):
        while len(parent1) > len(parent2):
            parent2.insert(0, "0")
        for i in range(len(parent2)):
            child1.append(0)
            child2.append(0)

        for i in range(len(parent1)):
            if i >= crossSite1 and i <= crossSite2:
                child1[i] = parent2[i]
                child2[i] = parent1[i]
            else:
                child1[i] = parent1[i]
                child2[i] = parent2[i] 
    
    else:
        for i in range(len(parent2)):
            child1.append(0)
            child2.append(0)

        for i in range(len(parent1)):
            if i >= crossSite1 and i <= crossSite2:
                child1[i] = parent2[i]
                child2[i] = parent1[i]
            else:
                child1[i] = parent1[i]
                child2[i] = parent2[i]

    parent1.clear()
    parent2.clear()


#Mutation
def mutation(child):
    for i in range(len(child)):
        choice = random.choices(mutation_decision, weights=[1/len(child), (len(child)-1)/len(child)], k = 1)
        if choice == ["yes"]:
            if child[i] == "1":
                child[i] = "0"
            else:
                child[i] = "1"

    child.insert(0, "b")
    child.insert(0, "0")
    eltern_child_mutated = "".join(map(str, child))    
    descendants_decimal.append(eltern_child_mutated)

    child.clear()

    

#Übersetzung in Dezimal
def binärintodezi(descendants, descendants_decimal):
    decimal_number1 = eval(descendants_decimal[0])
    decimal_number2 = eval(descendants_decimal[1])
    descendants.append(decimal_number1)
    descendants.append(decimal_number2)
    print("Das erste Kind ist:", decimal_number1)
    print("Das zweite Kind ist:", decimal_number2)

    descendants_decimal.clear()


#Ersetzung (Mischung aus Elitismus & delete-n-last)
def replacement():
    sorting(descendants)
    for i in range(population_size-2):
        population.pop(2)
    population.extend(descendants)
    for i in range(2):
        population.pop()
    print("Deine neue Generation ist:", population)

    descendants.clear()


#Durchführung
start = input("Möchtest du starten? (J)a / (N)ein: ")
   
generatePopulation()

while start.lower() == "j":
    sorting(population)
    for i in range(int(population_size/2)):
        print()
        print("Eltern", i+1)
        selection(parents)
        deziintobinär(parents, parents_decimal)
        transmission(parents_decimal, parent1, parent2)
        crossover(parent1, parent2, child1, child2)
        mutation(child1)
        mutation(child2)
        binärintodezi(descendants, descendants_decimal)

    print()
    print()
    replacement()
    if any(variable == ziel for variable in population): #if population[0] == ziel or population[1] == ziel or population[2] == ziel...
        print("Das Maximum wurde erreicht.")
        break
    
    start = input("Möchtest du eine weitere Generation entwickeln lassen? (J)a / (N)ein: ")

print("Deine Endgeneration ist:", population)