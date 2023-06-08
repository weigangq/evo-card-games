#!/usr/bin/env python
# Simulate genetic drift
# with Wright-Fisher model of neutrality, random mating,
#   constant pop, and non-overlapping generations

import sys
import drift # assume in the same directory

if __name__ == "__main__":
  # read the arguments on the command line
  # and convert to the right type
  # (they are strings by default)
  N = int(sys.argv[1])
  p = float(sys.argv[2])
  # call the simulation
  drift.simulate_drift(N, p)
