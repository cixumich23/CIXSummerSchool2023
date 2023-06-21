import random
from itertools import product

import gurobipy as gp
from gurobipy import GRB

import util

def assign(gui_elements, current_task, max_capacity, num_slots):

    # Init model
    model = gp.Model('assignment')

    # Supress Gurobi output (ie set to quiet instead of verbose)
    model.Params.LogToConsole = 0
    model.Params.OutputFlag = 0

    # Create helper lists and dictionaries
    items = []
    importances = {}
    appearances = {}
    costs = {}

    assign = {}
    # Add decision variables

    ##### OBJECTIVE FUNCTIONS ####

    # set objective for importance elements

    # set objective for appearance

    # set objective that prioritizes solutions that display more elements

    # The objective is to maximize the total objective function
    model.ModelSense = GRB.MAXIMIZE

    ##### CONSTRAINTS ####

    # Add constraint that the maximum number of items that are assigned is the number of slots

    # Add constraint that the maximum cost of all assigned items is smaller than max capacity

    # optimize model
    model.optimize()
    util.print_gurobi_model_state(model)

    # Get all gui elements that were assigned by the optimization
    gui_elements_to_display = []

    return gui_elements_to_display
