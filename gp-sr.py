import random
from random import randrange

functions = ['+', '-', '/', '*']
terminals = ['1', 'x']
functerm = functions + terminals
flen = len(functions)
tlen = len(terminals)
ftlen = len(functerm)


def randomElement(r):
    return random.randrange(r)


# Make an individual
def mkExpr(symb, d):
    if (symb in terminals):
        return symb
    else:
        if (d == 0):
            return terminals[randomElement(tlen)]
        else:
            return [symb] + [mkExpr(functerm[randomElement(ftlen)], (d - 1))] + [
                mkExpr(functerm[randomElement(ftlen)], (d - 1))]


# count total number of nodes
def countNodes(expr):
    if (len(expr) > 1):
        return 1 + countNodes(expr[1]) + countNodes(expr[2])
    else:
        return 1


# MUTATION

def mutate(expr, n):
    if (n == 0):
        if (expr in terminals):
            return terminals[randomElement(tlen)]
        else:
            return [functions[randomElement(flen)]] + [expr[1]] + [expr[2]]
    else:
        nl = countNodes(expr[1])
        if (nl >= n):
            return [expr[0]] + [mutate(expr[1], (n - 1))] + [expr[2]]
        else:
            return [expr[0]] + [expr[1]] + [mutate(expr[2], (n - (nl + 1)))]


# CROSSOVER

def getBranch(expr, n):
    if (n == 0):
        return expr
    else:
        nl = countNodes(expr[1])
        if (nl >= n):
            return getBranch(expr[1], (n - 1))
        else:
            return getBranch(expr[2], (n - (nl + 1)))


def insertSubBranch(expr, n, subranch):
    if (n == 0):
        return subranch
    else:
        nl = countNodes(expr[1])
        if (nl >= n):
            return [expr[0]] + [insertSubBranch(expr[1], (n - 1), subranch)] + [expr[2]]
        else:
            return [expr[0]] + [expr[1]] + [insertSubBranch(expr[2], (n - (nl + 1)), subranch)]



def crossover(expr1, expr2):
    n1 = random.randrange(countNodes(expr1))
    n2 = random.randrange(countNodes(expr2))
    g1 = getBranch(expr1, n1)
    g2 = getBranch(expr2, n2)
    if (random.randrange(2) == 0):
        return insertSubBranch(expr1, n1, g2)
    else:
        return insertSubBranch(expr2, n2, g1)


def mydiv(x, y):
    if (y == 0):
        return 1
    else:
        return x / y


# EVALUATION

def evalExpr(expr, vs):
    if (len(expr) > 1):
        op = expr[0]
        lb = evalExpr(expr[1], vs)
        rb = evalExpr(expr[2], vs)
        if (op == '+'):
            return lb + rb
        if (op == '-'):
            return lb - rb
        if (op == '*'):
            return lb * rb
        if (op == '/'):
            return mydiv(lb, rb)
    else:
        if (expr == '1'):
            return 1
        else:
            return vs


def calcFitness(expr, fcases):
    return -calcFitness_aux(expr, fcases)


def calcFitness_aux(expr, fcases):
    if not fcases:
        return 0
    else:
        return calc_aux_ft(expr, fcases[0]) + calcFitness_aux(expr, fcases[1:])


def calc_aux_ft(expr, ft):
    vs1 = ft[0]
    vs = float(vs1[0])
    aout = evalExpr(expr, vs)
    error = aout - float(ft[1])
    return error


# LOAD FITNESS CASES

def loadCases():
    f = open('data', 'r+')
    var = f.readline().split()
    nv = var[0]
    nf = var[1]
    list1 = []
    for i in range(0, int(nf)):
        x = f.readline().split()
        list1 += [[[x[0]]] + [x[1]]]
        # list2 = list2 + list1
    return [nf] + [list1]


def getExpr(ind):
    return ind[0]


def getFitness(ind):
    return ind[1]


# Creating a Population of Individuals with fitness 0

def initPopulation(popsize, depth):
    return list(map(lambda x: [mkExpr(functerm[randomElement(ftlen)], depth), 0], range(popsize)))


# Evaluating Population against fitness cases

def evalPopulation(pop, fitCases):
    return list(map(lambda ind: [getExpr(ind)] + [calcFitness(getExpr(ind), fitCases)], pop))

# TOURNAMENT SELECTION

def positiveTS(tsize, pop):
    best = pop[randomElement(len(pop))]
    for n in range(0,tsize):
        best_t = pop[randomElement(len(pop))]
        if(getFitness(best) > getFitness(best_t)):
            best = best
        else:
            best = best_t
    return getExpr(best)


def negativeTS(tsize, pop):
    best = pop[randomElement(len(pop))]
    for n in range(0,tsize):
        best_t = pop[randomElement(len(pop))]
        if(getFitness(best) < getFitness(best_t)):
            best = best
        else:
            best = best_t
    return getExpr(best)


def replace_worst(newind, worst, pop):
    if(worst == getExpr(pop[0])):
        return [newind] + pop[1:]
    else:
        return [pop[0]] + replace_worst(newind, worst, pop[1:])


def doMutation(expr):
    nl = countNodes(expr)
    return mutate(expr, random.randrange(0,nl))

def evolve(f, pop, gen, popsize, crossoverP, tsize, ftcs):
    for n in range(0,gen):
        sor = sorted(pop, key=lambda pop: pop[1]) #, reverse=True)
        best = sor[0]
        if(getFitness(best) > -1e-5):
            print(n,best)
            break
        else:
            for i in range(popsize):
                parent1 = positiveTS(tsize, pop)
                worstOffspring = negativeTS(tsize, pop)
                if(random.random() > crossoverP):
                    parent2 = positiveTS(tsize, pop)
                    newind = crossover(parent1, parent2)
                else:
                    newind = doMutation(parent1)
                fitness = calcFitness(newind, ftcs)
                newindWithFitness = [newind] + [fitness]
                newPop = replace_worst(newindWithFitness, worstOffspring, pop)
                pop = newPop
        stats(f, n, gen, popsize, pop, ftcs)
        pop = pop



def stats(f, n, gen, popsize, pop, ftcs):
    sor = sorted(pop, key=lambda pop: pop[1], reverse=True)
    best = sor[0]
    fbest = getFitness(best)
    avgLength = mydiv(countNodesPop(pop), popsize)
    avgFitness = mydiv(avgFitnessPop(pop), popsize)
    f.write("%f,%f,%f,%f\n" % (n, gen, avgLength, avgFitness))

def countNodesPop(pop):
    if not pop:
        return 0
    else:
        return countNodes(getExpr(pop[0])) + countNodesPop(pop[1:])

def avgFitnessPop(pop):
    if not pop:
        return 0
    else:
        return getFitness(pop[0]) + avgFitnessPop(pop[1:])


def main():
    n = 3
    f = open('GP-data.csv', 'w+')
    f.write('run,gen,avglen,avgfit\n')
    popsize = 100
    depth = 5
    ipop = initPopulation(popsize, depth)
    gen = 50
    crossoverP = 0.9
    tsize = 2
    lc = loadCases()
    ftcs = lc[1]
    pop = evalPopulation(ipop, ftcs)
    for x in range(0,n):
        evolve(f, pop, gen, popsize, crossoverP, tsize, ftcs)


main()


