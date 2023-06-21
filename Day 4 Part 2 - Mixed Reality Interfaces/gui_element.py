class GUI_Element:
    # image_index = -1
    # name = ""

    def __init__(self, name, image_index):
        self.name = name
        self.image_index = image_index
        self.importance_per_task = []

        self.cost = 0.0
        self.visible = 0.0
        self.locked = 0.0
        self.appearance = 0.0