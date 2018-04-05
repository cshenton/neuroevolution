# Policy network architecture (specify only # actions)
# Convenient 'choose action' type functions
# Function that takes an initialised network and "evolves" it into individual
#   in particular, one that can reset the weights of an already constructed net
# Function that takes a policy network and runs it against an environment
#   for specified number of time steps
#   just returns score
# Worker process
#   init environment
#   init network architecutre
#   for:
#   Seek()
#   build individual net
#   evaluate net
#   Show()
