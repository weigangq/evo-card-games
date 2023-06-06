############################
# Game 2. Red Queen
# Ref: https://evolution-outreach.biomedcentral.com/articles/10.1186/s12052-015-0039-2
# Paper: Gibson, Drown & Lively (2015). "The Red Queen’s Race: An Experimental Card Game to Teach Coevolution"
###############################

library(tidyverse)

# create decks of cards
deck <- rep(c("dimond", "heart", "club", "spade"), 13)

# shuffle
deck <- sample(deck)

# create 2 pops and shuffle
host_deck <- sample(deck)
parasite_deck <- sample(deck)

# define functions
# host win doubles
reproduce_host <- function(host, reserve) {
  if(length(host) >= pop_size) {
    return(sample(rep(host, 2), pop_size))
  } else {
    return(c(host, sample(reserve, pop_size - length(host))))
  }
}  

# parasite wins triples
reproduce_parasite <- function(parasite, reserve) {
  if(length(parasite) >= pop_size) {
    return(sample(rep(parasite, 3), pop_size))
  } else {
    return(c(parasite, sample(reserve, pop_size - length(parasite))))
  }
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
pop_size = 12
round_max = 20

# initialize
all_index = 1:52
host_select <- sample(all_index, pop_size)
host_remain <- all_index[!all_index %in% host_select]
parasite_select <- sample(all_index, pop_size)
parasite_remain <- all_index[!all_index %in% parasite_select]

host <- host_deck[host_select]
host_reserve <- host_deck[host_remain]
parasite <- parasite_deck[parasite_select]
parasite_reserve <- parasite_deck[parasite_remain]

# play
out_freq <- vector("list", length = round_max)
r <- 1
while(r <= round_max) {
  host_win <- c()
  parasite_win <- c()
  
  for(i in 1:pop_size){
    if(host[i] == parasite[i]) {
      parasite_win <- append(parasite_win, parasite[i])
    } else {
      host_win <- append(host_win, host[i])
    }
  }
  
  # host wins doubles
  host <- reproduce_host(host_win, host_reserve)
  parasite <- reproduce_parasite(parasite_win, parasite_reserve)
  
  print(r)
  host_cts <- table_to_vector(host)
  parasite_cts <- table_to_vector(parasite)
  
  out_freq[[r]] <- tibble(round = rep(r,8), 
                          suite = rep(c('club', 'dimond', 'heart', 'spade'),2),
                          role = c(rep('host',4), rep('parasite',4)),
                          ct = c(host_cts['club'], host_cts['dimond'], host_cts['heart'], host_cts['spade'], parasite_cts['club'], parasite_cts['dimond'], parasite_cts['heart'], parasite_cts['spade'])
                                 )
  r <- r + 1
}
out <- bind_rows(out_freq)
out.long <- out %>% mutate(freq = ct / pop_size)

# visualize
# by role: balanced polymorphisms (rare allele advantages)
out.long %>% ggplot(aes(round, freq, color = suite)) +
  geom_line() +
  geom_point(shape=1, size = 2, color= "gray") +
  theme_bw() + 
  facet_wrap(~role, ncol = 1)

# by suite: parasite tracks host alleles?
out.long %>% ggplot(aes(round, freq, color = role, group = role)) +
  geom_line() +
  geom_point(shape=1, size = 2, color= "gray") +
  theme_bw() + 
  facet_wrap(~suite, ncol = 2)

# metapopulation: run a few times
#meta <- out.long %>% group_by(round, suite) %>% 
#  summarise(cts = sum(ct))
