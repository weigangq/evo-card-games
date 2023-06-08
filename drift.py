import numpy as np

def build_population(N, p):
  """The population consists of N diploid individuals.
  
      Each individual has two chromosomes, containing
      allele "A" or "a", with probability p or 1-p,
      respectively.

      The population is a list of tuples.
  """
  population = []
  for i in range(N):
    # set allele 1 as A or a (with prob of p)
    allele1 = "A"
    if np.random.uniform() > p:
      allele1 = "a"

    # set allele 2 as A or a (with prob of p)
    allele2 = "A"
    if np.random.uniform() > p:
      allele2 = "a"
    # a dipolid individual as a tuple
    population.append((allele1, allele2))
  return population

def simulate_drift(N, p):
  # initialize the population
  my_pop = build_population(N, p)
  fixation = False # a logical variable to mark termination point (when true)
  num_generations = 0 # initialize a generation counter
  while fixation == False:
    # compute genotype counts
    genotype_counts = compute_frequencies(my_pop)
    # if one allele went to fixation, end
    if genotype_counts["AA"] == N or genotype_counts["aa"] == N:
      print("An allele reached fixation at generation", num_generations, end = "\t")
      print("The genotype counts are", end = "\t")
      print(genotype_counts)
      fixation == True
      break
    # if not, reproduce
    my_pop = reproduce_population(my_pop)
    num_generations = num_generations + 1

def compute_frequencies(population):
  """ Count the genotypes.
      Returns a dictionary of genotypic frequencies.
  """
  # count the tuples
  AA = population.count(("A", "A"))
  Aa = population.count(("A", "a"))
  aA = population.count(("a", "A"))
  aa = population.count(("a", "a"))
  # return counts as a dict
  return({"AA": AA,
          "aa": aa,
          "Aa": Aa,
          "aA": aA})

def reproduce_population(population):
  """ Create new generation through reproduction
      For each of N new offspring,
      - choose the parents at random;
      - the offspring receives a chromosome from
        each of the parents.
  """
  new_generation = []
  N = len(population)
  for i in range(N):
    # random integer between 0 and N-1
    dad = np.random.randint(N) # pick an individual as dad
    mom = np.random.randint(N) # pick an individual as mom (could be the same as dad by chance!!)
    # which chromosome comes from mom
    chr_mom = np.random.randint(2) # return either 0 or 1
    offspring = (population[mom][chr_mom], population[dad][1 - chr_mom])
    new_generation.append(offspring)
  return(new_generation)

def simulate_drift(N, p):
  # initialize the population
  my_pop = build_population(N, p)
  fixation = False # a logical variable to mark termination point (when true)
  num_generations = 0 # initialize a generation counter
  while fixation == False:
    # compute genotype counts
    genotype_counts = compute_frequencies(my_pop)
    # if one allele went to fixation, end
    if genotype_counts["AA"] == N or genotype_counts["aa"] == N:
      print("An allele reached fixation at generation", num_generations, end = "\t")
      print("The genotype counts are", end = "\t")
      print(genotype_counts)
      fixation == True
      break
    # if not, reproduce
    my_pop = reproduce_population(my_pop)
    num_generations = num_generations + 1
