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
    costs = {}

    # Create helpers to build adjacency matrix (dictionary in python)
    item_tuples = []
    pairwise_similarities = {}

    assign = {}

    #  Objective that ensures that closely related objects are displayed

    # The objective is to maximize the overall objective
    model.ModelSense = GRB.MAXIMIZE

    ##### CONSTRAINTS ####

    # Add constraint that the maximum number of items that are assigned is the number of slots
    model.addConstr(gp.quicksum(assign[name] for name in items) <= num_slots, "max_num_assigned_constraint")

    # Add constraint that the maximum cost of all assigned items is smaller than max capacity
    model.addConstr(gp.quicksum(costs[name] * assign[name] for name in items) <= max_capacity, "cost_constaint")

    model.optimize()
    util.print_gurobi_model_state(model)

    # Get all gui elements that were assigned by the optimization
    gui_elements_to_display = []

    return gui_elements_to_display
