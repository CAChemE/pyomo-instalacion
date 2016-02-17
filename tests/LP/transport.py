#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""
Basic example of transport model from GAMS model library translated to Pyomo
 
To run this you need pyomo and a linear solver installed.
When these dependencies are installed you can solve this example in one of
this ways (glpk is the default solver):
 
    ./transport.py (Linux only)
    python transport.py
    pyomo solve transport.py
    pyomo solve --solver=glpk transport.py
 
To display the results:
 
    cat results.json
    cat results.yml (if PyYAML is installed on your system)
 
GAMS equivalent code is inserted as single-dash comments. The original GAMS code
needs slighly different ordering of the commands and it's available at
http://www.gams.com/mccarl/trnsport.gms
 
Original problem formulation:
    Dantzig, G B, Chapter 3.3. In Linear Programming and Extensions.
    Princeton University Press, Princeton, New Jersey, 1963.
GAMS implementation:
    Rosenthal, R E, Chapter 2: A GAMS Tutorial. In GAMS: A User's Guide.
    The Scientific Press, Redwood City, California, 1988.
Pyomo translation:
    Antonello Lobianco
 
This file is in the Public Domain
"""
 
# Import
from pyomo.environ import *
 
# Creation of a Concrete Model
model = ConcreteModel()
 
## Define sets ##
#  Sets
#       i   canning plants   / seattle, san-diego /
#       j   markets          / new-york, chicago, topeka / ;
model.i = Set(initialize=['seattle','san-diego'], doc='Canning plans')
model.j = Set(initialize=['new-york','chicago', 'topeka'], doc='Markets')
 
## Define parameters ##
#   Parameters
#       a(i)  capacity of plant i in cases
#         /    seattle     350
#              san-diego   600  /
#       b(j)  demand at market j in cases
#         /    new-york    325
#              chicago     300
#              topeka      275  / ;
model.a = Param(model.i, initialize={'seattle':350,'san-diego':600}, doc='Capacity of plant i in cases')
model.b = Param(model.j, initialize={'new-york':325,'chicago':300,'topeka':275}, doc='Demand at market j in cases')
#  Table d(i,j)  distance in thousands of miles
#                    new-york       chicago      topeka
#      seattle          2.5           1.7          1.8
#      san-diego        2.5           1.8          1.4  ;
dtab = {
    ('seattle',  'new-york') : 2.5,
    ('seattle',  'chicago')  : 1.7,
    ('seattle',  'topeka')   : 1.8,
    ('san-diego','new-york') : 2.5,
    ('san-diego','chicago')  : 1.8,
    ('san-diego','topeka')   : 1.4,
    }
model.d = Param(model.i, model.j, initialize=dtab, doc='Distance in thousands of miles')
#  Scalar f  freight in dollars per case per thousand miles  /90/ ;
model.f = Param(initialize=90, doc='Freight in dollars per case per thousand miles')
#  Parameter c(i,j)  transport cost in thousands of dollars per case ;
#            c(i,j) = f * d(i,j) / 1000 ;
def c_init(model, i, j):
  return model.f * model.d[i,j] / 1000
model.c = Param(model.i, model.j, initialize=c_init, doc='Transport cost in thousands of dollar per case')
 
## Define variables ##
#  Variables
#       x(i,j)  shipment quantities in cases
#       z       total transportation costs in thousands of dollars ;
#  Positive Variable x ;
model.x = Var(model.i, model.j, bounds=(0.0,None), doc='Shipment quantities in case')
 
## Define contrains ##
# supply(i)   observe supply limit at plant i
# supply(i) .. sum (j, x(i,j)) =l= a(i)
def supply_rule(model, i):
  return sum(model.x[i,j] for j in model.j) <= model.a[i]
model.supply = Constraint(model.i, rule=supply_rule, doc='Observe supply limit at plant i')
# demand(j)   satisfy demand at market j ;  
# demand(j) .. sum(i, x(i,j)) =g= b(j);
def demand_rule(model, j):
  return sum(model.x[i,j] for i in model.i) >= model.b[j]  
model.demand = Constraint(model.j, rule=demand_rule, doc='Satisfy demand at market j')
 
## Define Objective and solve ##
#  cost        define objective function
#  cost ..        z  =e=  sum((i,j), c(i,j)*x(i,j)) ;
#  Model transport /all/ ;
#  Solve transport using lp minimizing z ;
def objective_rule(model):
  return sum(model.c[i,j]*model.x[i,j] for i in model.i for j in model.j)
model.objective = Objective(rule=objective_rule, sense=minimize, doc='Define objective function')
 
 
## Display of the output ##
# Display x.l, x.m ;
def pyomo_postprocess(options=None, instance=None, results=None):
  model.x.display()
 
# This is an optional code path that allows the script to be run outside of
# pyomo command-line.  For example:  python transport.py
if __name__ == '__main__':
 
    #This replicates what the pyomo command-line tools does
    from pyomo.opt import SolverFactory
    import pyomo.environ
    opt = SolverFactory("glpk")
    instance = model.create()
    results = opt.solve(instance)
    #sends results to stdout
    results.write()
    pyomo_postprocess(None, instance, results)
 
# Expected result:
# obj= 153.675
#['seattle','new-york']   = 50
#['seattle','chicago']    = 300
#['seattle','topeka']     = 0
#['san-diego','new-york'] = 275
#['san-diego','chicago']  = 0
#['san-diego','topeka']   = 275