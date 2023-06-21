def assign(gui_elements, current_task, max_capacity, num_slots):
    # Sort GUI elements based on their importance for the current task.
    # First element in list will have the highest importance
    gui_elements.sort(key=lambda gui_element: gui_element.importance_per_task[current_task], reverse=True)

    gui_elements_to_display = []

    current_load = 0.0
    number_assigned_elements = 0

    # Add GUI elements until we have no more capacity to add more elements

    return gui_elements_to_display
