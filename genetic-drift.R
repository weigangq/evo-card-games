# Evolutionary games with playing cards

library(tidyverse)

# create decks of cards
deck <- rep(c("dimond", "heart", "club", "spade"), 13)

# shuffle
deck <- sample(deck)

############################################
# Game 1. Genetic Drift
# Neutral evolution with Wright-Fisher Model:
# constant population size
# No selection
# No mutation
# random mating
# Drift only


# functions:
# each individual reproduce once
reproduce <- function(p){
  return(rep(p,2))
}

# count cards
table_to_vector <- function(p) {
  x <- table(p)
  v <- c()
  for(i in levels(as.factor(deck))) {
    v[i] <- if_else(is.na(x[i]), 0, x[i])
  }
  v
}

# constants
pop_size <- 20
gen_max <- 100

# initialize
pop <- sample(deck, pop_size)
g <- 1

# iterate & capture frequency
out_freq <- vector("list", length = gen_max)
while(g <= gen_max) {
  gametes <- reproduce(pop)
  pop <- sample(gametes, pop_size)
  print(g)
  print(table(pop))
  cts <- table_to_vector(pop)
  out_freq[[g]] <- tibble(gen = g, dimond = cts['dimond'], club = cts['club'], heart = cts['heart'], spade = cts['spade'])
  g <- g + 1
}
out <- bind_rows(out_freq)

# plot frequencies
out.long <- out %>% pivot_longer(2:5, names_to = "suite", values_to = "cts")
out.long <- out.long %>% mutate(freq = cts / pop_size)

out.long %>% ggplot(aes(gen, freq, color = suite)) +
  geom_line() +
  geom_point(shape=1, size = 2) +
  theme_bw()

out.long %>% ggplot(aes(gen, freq)) +
  geom_line() +
  geom_point(shape=1, size = 2, color= "gray") +
  theme_bw() + 
  facet_wrap(~suite, ncol = 1)

# End of Game 1
