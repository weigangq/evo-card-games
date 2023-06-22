#red queen card game data viz

library(ggplot2)
library(tidyverse)
library(tidyr)

setwd('/Users/brandonely/Desktop/rq_game_sim/')
x <- read_tsv('rq_sim_data.tsv', col_names = T)
x$gen <- factor(x$gen)
x_long <- gather(x, allele, freq, A_h:D_p, factor_key=TRUE)
x_long <- x_long %>% mutate('group' = if_else(allele == 'A_h', 'A', if_else(allele == 'A_p', 'A', if_else(allele == 'B_h', 'B', if_else(allele == 'B_p', 'B', if_else(allele == 'C_h', 'C', if_else(allele == 'C_p', 'C', 'D')))))))
x_long <- x_long %>% mutate('type' = if_else(str_detect(allele,'_p'),'pathogen', 'host'))

x_long %>%
  ggplot(aes(x=gen, y=freq, group = type, color = type))+
  geom_line() +
  facet_wrap(~group)



# x %>%
#   ggplot(aes(x=gen)) +
#   geom_line(aes(x=gen, y=A, color = 'Host(A)')) +
#   geom_line(aes(x=gen, y=B, color = 'B')) +
#   geom_line(aes(x=gen, y=C, color = 'C')) +
#   geom_line(aes(x=gen, y=D, color = 'D')) +
#   geom_line(aes(x=gen, y=`A'`, color = 'Pathogen(A\')')) +
#   geom_line(aes(x=gen, y=`B'`, color = 'B\''), alpha = 0.4) +
#   geom_line(aes(x=gen, y=`C'`, color = 'C\''), alpha = 0.4) +
#   geom_line(aes(x=gen, y=`D'`, color = 'D\''), alpha = 0.4) +
#   #scale_color_manual(values=c('green', 'purple')) +
#   theme_minimal() +
#   #geom_hline(yintercept = 1, linetype = 2) +
#   theme(axis.text=element_text(size=15), axis.title=element_text(size=18), legend.title=element_text(size = 12),legend.text=element_text(size=10),legend.box.background=element_rect(),legend.box.margin=margin(1,1,1,1), panel.border = element_rect(color = "black",fill = NA, size = 1)) +
#   labs(x = 'Generation', y = 'Allele frequency', color = 'Allele')

