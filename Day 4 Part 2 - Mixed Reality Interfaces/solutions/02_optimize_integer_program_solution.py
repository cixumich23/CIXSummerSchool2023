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
    for gui_element in gui_elements:
        items.append(gui_element.name)
        importances[gui_element.name] = gui_element.importance_per_task[current_task]
        appearances[gui_element.name] = gui_element.appearance
        costs[gui_element.name] = gui_element.cost

    assign = {}
    # Add decision variables
    for item in items:
        # addVar(lower_bound, upper_bound, objective, type, variable_name)
        # lower_bound and upper_bound: 0.0 --> not assigned; 1.0 --> assigned;
        # modify if you need to set a constraint that an object should or should not be assigned
        # assign[item] will be 1.0 if item is assigned, 0.0 if item is not assigned
        assign[item] = model.addVar(0.0, 1.0, 0.0, GRB.BINARY, item)

    model.setObjectiveN(gp.quicksum(importances[name] * assign[name] for name in items), index = 0)
    model.setObjectiveN(gp.quicksum(appearances[name] * assign[name] for name in items), index = 1)
    model.setObjectiveN(gp.quicksum(assign[name] for name in items), index = 2)

    # The objective is to minimize the total costs and inverse reward
    model.ModelSense = GRB.MAXIMIZE

    # Add constraint that the maximum number of items that are assigned is the number of slots
    model.addConstr(gp.quicksum(assign[name] for name in items) <= num_slots, "max_num_assigned_constraint")

    # Add constraint that the maximum cost of all assigned items is smaller than max capacity
    model.addConstr(gp.quicksum(costs[name] * assign[name] for name in items) <= max_capacity, "cost_constaint")

    model.optimize()
    util.print_gurobi_model_state(model)

    # #####################
    # DEBUG PRINT
    # total_cost = 0.0
    # total_importance = 0.0

    # for i in range(0, len(items)):
    #     item = items[i]
    #     # Item is assigned if variable decision variable ("x") is larger than 0
    #     if assign[item].x > 1e-6:
    #         print(f"item {item} has been assigned with importance {importances[item]} with cost {costs[item]}")
    #         total_cost = total_cost + costs[item]
    #         total_importance = total_importance + importances[item]
    # print(f"Total cost is {total_cost:.2f} / Total importance is {total_importance:.2f}")
    # #####################

    # Get all gui elements that were assigned by the optimization
    gui_elements_to_display = []
    for gui_element in gui_elements:
        # Item is assigned if variable decision variable ("x") is larger than 0
        if assign[gui_element.name].x > 1e-6:
            gui_elements_to_display.append(gui_element)

    return gui_elements_to_display
