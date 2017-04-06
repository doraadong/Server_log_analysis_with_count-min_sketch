// your Python code to implement the features could be placed here
// note that you may use any language, there is no preference towards Python

import os 

import controller as con
import hosts as hosts
import resources as resources
import hours as hours
import blocked as blocked


# setup directory
filename = './log_input/log.txt'
output = './log_output/'
control = con.controller(filename, output)

# register features
control.register(hosts.hosts(d=100,w=100000,k=10))
control.register(resources.resources(d=100,w=100000,k=10))
control.register(hours.hours(3600,10))
control.register(blocked.blocked(20,5,3))

# run 
control.run()