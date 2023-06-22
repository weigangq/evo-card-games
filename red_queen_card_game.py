#red queen card game simulator 
import random
import numpy as np
import pandas as pd
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
    description='This program is a simulation of "The Red Queens Race:\n'
    'An Experimental Card Game to Teach Coevolution\n'
    'Gibson et al 2015 https://doi.org/10.1186/s12052-015-0039-2\n'
    ' \n', formatter_class=RawTextHelpFormatter)

###arguments

parser.add_argument('-n', '--generation', type=int, default=15, help='number of generations for simulation')
parser.add_argument('-pop', '--population_size', type=int, default=12, help='population size (number of cards in hand)')
parser.add_argument('-hrr', '--host_rep', type=int, default=1, help='host replication rate')
parser.add_argument('-prr', '--path_rep', type=int, default=2, help='pathogen replication rate')
args = parser.parse_args()

###functions 

def choose_and_remove(items):
    if items:
        index = random.randrange(len(items))
        return items.pop(index)

def genotype_frequency(hand):
  A = hand.count('A')
  B = hand.count('B')
  C = hand.count('C')
  D = hand.count('D')
  composition = {'A': round(A/len(hand),2), 'B': round(B/len(hand),2), 'C': round(C/len(hand),2), 'D': round(D/len(hand),2)}
  return composition

###set up the game

#define genotypes
genotypes = ['A', 'B', 'C', 'D']

#create card decks
host_deck = genotypes * 13
path_deck = genotypes * 13

#deal hands 
host_hand = []
path_hand = []
for n in range(args.population_size):
  host_card = choose_and_remove(host_deck)
  host_hand.append(host_card)
  path_card = choose_and_remove(path_deck)
  path_hand.append(path_card)

#record genotype frequencies for starting generation
host_generation = [genotype_frequency(host_hand)]
path_generation = [genotype_frequency(path_hand)]

###simulate the game
for n in range(args.generation): #set how many rounds you want to play here
  host_winners = []
  host_losers = []
  path_winners = []
  path_losers = []
  for n in range(args.population_size):
    host_card = choose_and_remove(host_hand)
    path_card = choose_and_remove(path_hand)
    if host_card != path_card:
      host_winners.append(host_card)
      path_losers.append(path_card)
    else:
      path_winners.append(path_card)
      host_losers.append(host_card)

  #add loser cards back to appropriate deck
  host_deck += host_losers
  path_deck += path_losers

  #reproduce host winners
  new_cards = []
  for n in range(args.host_rep):
    for item in host_winners:
      if item in host_deck:
        host_deck.remove(item)
        new_cards.append(item)
      else:
        new_cards.append(choose_and_remove(host_deck))
  
  #reset hand for next generation
  host_hand = host_winners + new_cards
  if len(host_hand) > args.population_size:
    for i in range(len(host_hand)-args.population_size):
      host_deck.append(choose_and_remove(host_hand))
  if len(host_hand) < args.population_size:
    for i in range(args.population_size-len(host_hand)):
      host_hand.append(choose_and_remove(host_deck))

  #reproduce pathogen winners
  new_cards = []
  for n in range(args.path_rep):
    for item in path_winners:
      if item in path_deck:
        path_deck.remove(item)
        new_cards.append(item)
      else:
        new_cards.append(choose_and_remove(path_deck))

  #reset hand for next generation
  path_hand = path_winners + new_cards
  if len(path_hand) > args.population_size:
    for i in range(len(path_hand)-args.population_size):
      path_deck.append(choose_and_remove(path_hand))
  if len(path_hand) < args.population_size:
    for i in range(args.population_size-len(path_hand)):
      path_hand.append(choose_and_remove(path_deck))

  #record new genotype frequencies
  host_generation.append(genotype_frequency(host_hand))
  path_generation.append(genotype_frequency(path_hand))

#generate dataframes with host and pathogen genotype frequencies
#host_data = pd.DataFrame(host_generation)
#path_data = pd.DataFrame(path_generation)
#path_data = path_data.rename({'A': 'A\'', 'B': 'B\'', 'C': 'C\'', 'D': 'D\''}, axis='columns')
#results = pd.concat([host_data, path_data], axis = 1, join = 'inner')

#print genotype frequencies for every generation
print('gen','\t',
      'A_h','\t','B_h','\t','C_h','\t','D_h','\t',
      'A_p','\t','B_p','\t','C_p','\t','D_p')
k=0
for i in range(len(host_generation)):
  print(k,'\t',host_generation[i]['A'],'\t',host_generation[i]['B'],'\t',host_generation[i]['C'],'\t',host_generation[i]['D'],'\t',
        path_generation[i]['A'],'\t',path_generation[i]['B'],'\t',path_generation[i]['C'],'\t',path_generation[i]['D'])
  k+=1
