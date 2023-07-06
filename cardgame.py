import random
import pandas


suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

fulldeck = [suit for suit in suits] * 13


random.shuffle(fulldeck)

# 12 card draws 
host_cards = random.sample(fulldeck, 12)  #look in documentation ,should be w/o replacement
parasite_cards = random.sample(fulldeck, 12)


##TO DO
#Define a dictionary to be updated for each generation
#host={}
#host['hearts] =[insert number of hearts for gen0]
#host['spade'] =[insert number of spades for gen0]
#....
#Do the same for parasite.



# Print the first draw
print("First draw:")
for card in host_cards:
    print(card)

print("\n")

# Print the second draw
print("Second draw:")
for card in parasite_cards:
    print(card)


print("\n")

#for i in range(len(host_cards)):
 #  print(parasite_cards[i]==host_cards[i])

# Count suit matches
suit_count = {}
for suit in suits:
    suit_count[suit] = 0

for suit in suits:   ###do a sanity check,  Does this do what you want it to do?
    count = sum(hcard == suit and pcard == suit for hcard, pcard in zip(host_cards, parasite_cards))
    suit_count[suit] = count
print(host_cards)
print(parasite_cards)
print(suit_count)
