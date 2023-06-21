def assign(gui_elements, current_task, max_capacity, num_slots):
    # Sort GUI elements based on their importance for the current task.
    # First element in list will have the highest importance
    gui_elements.sort(key=lambda gui_element: gui_element.importance_per_task[current_task], reverse=True)

    gui_elements_to_display = []

    current_load = 0.0
    number_assigned_elements = 0

    for gui_element in gui_elements:
        # add element if we have capacity to add one more element
        if current_load + gui_element.cost < max_capacity:
            gui_elements_to_display.append(gui_element)
            current_load = current_load + gui_element.cost
            number_assigned_elements = number_assigned_elements + 1

    return gui_elements_to_display
