# From https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/
# import the opencv library
import math
import random

import cv2
import numpy as np
import os

from gui_element import GUI_Element
from slot import Slot

from enum import Enum
class Optimizer(Enum):
    TRIVIAL = 0
    GREEDY = 1
    INTEGER_PROGRAM = 2
    QAP = 3

import sys
sys.path.insert(1, './solutions/')

assign_all = __import__('00_assign_all')
optimize_greedy = __import__('01_optimize_greedy')
optimize_integer_program = __import__('02_optimize_integer_program')
optimize_qap = __import__('03_optimize_qap')

optimizer = Optimizer.TRIVIAL

num_slots = 10
slots = []

num_gui_elements = 12
gui_elements = []
assigned_gui_elements = []

num_tasks = 3
current_task = 0

max_capacity = 2.0

offset = 10
img_width = 640
img_height = 480
img_slot_size = 50

slot_occupancy = np.zeros((1, 10))

# Load the cascade
face_cascade = cv2.CascadeClassifier('assets/models/haarcascade_frontalface_default.xml')


def detect_face(frame):
    # Convert into grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    face = [-1, -1, -1, -1]
    if len(faces) > 0:
        face = faces[0]

    # mark face
    (x, y, w, h) = face
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return face


def set_slot_activity(face):
    # face are (x,y,w,h) coordinates
    (face_x, face_y, face_width, face_height) = face

    # face not recognized if width < 0
    if face_width < 0:
        return

    face_center_x = face_x + face_width / 2.0
    face_center_y = face_y + face_height / 2.0
    face_diameter = math.sqrt(math.pow(face_width / 2.0, 2) + math.pow(face_height / 2.0, 2))

    for i in range(0, num_slots):
        slot = slots[i]
        slot_center_x = slot.x + slot.size / 2.0
        slot_center_y = slot.y + slot.size / 2.0
        distance_slot_face = math.sqrt(
            math.pow(face_center_x - slot_center_x, 2) + math.pow(face_center_y - slot_center_y, 2))
        face_overlaps_slot = distance_slot_face < face_diameter

        # print (face_center_x, face_center_y,face_diameter, distance_slot_face, face_overlaps_slot)

        if face_overlaps_slot:
            slot.occupancy = min(slot.occupancy + 0.05, 1)
        else:
            slot.occupancy = max(slot.occupancy - 0.01, 0)


def visualize_slot_activity(frame):
    for slot in slots:
        frame[slot.y:slot.y + slot.size, slot.x:slot.x + slot.size] = \
            frame[slot.y:slot.y + slot.size, slot.x:slot.x + slot.size] + (int)(255 * slot.occupancy)

    return frame


def display_assigned_gui_elements(frame):
    for i in range(0, len(assigned_gui_elements)):
        slot = slots[i]
        gui_element = assigned_gui_elements[i]
        icon = gui[gui_element.image_index]
        frame[slot.y:slot.y + slot.size, slot.x:slot.x + slot.size] = icon


def print_assigned_gui_elements_info():
    print(f"Assigned elements for task {current_task}:")
    total_cost = 0.0
    total_importance = 0.0
    total_apperance = 0.0
    for gui_element in assigned_gui_elements:
        total_cost = total_cost + gui_element.cost
        total_importance = total_importance + gui_element.importance_per_task[current_task]
        total_apperance = total_cost + gui_element.appearance
        print(f"{gui_element.name}. Importance {gui_element.importance_per_task[current_task]:.2f} / Cost {gui_element.cost:.2f}")

    print(f"Total cost: {total_cost:.2f} / Total importance: {total_importance:.2f} / Total appearance: {total_apperance:.2f}")


def start_video_capture():
    # hacky, use classes
    global current_task, max_capacity, assigned_gui_elements, optimizer

    print("Starting video from webcam.")
    vid = cv2.VideoCapture(0)

    if not vid.isOpened():
        raise Exception("Could not open video device")

    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # Capture the video frame by frame
        ret, frame = vid.read()

        face = detect_face(frame)

        set_slot_activity(face)
        frame = visualize_slot_activity(frame)
        display_assigned_gui_elements(frame)

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break
        elif key == ord('p'):
            if optimizer == Optimizer.GREEDY:
                optimizer = Optimizer.INTEGER_PROGRAM
                print("Switched optimizer to Integer Program")
            elif optimizer == Optimizer.INTEGER_PROGRAM:
                optimizer = Optimizer.QAP
                print("Switched optimizer to Quadratic Assignment")
            else:
                optimizer = Optimizer.GREEDY
                print("Switched optimizer to Greedy")
        elif key == ord('o'):
            print("###############")
            print("OPTIMIZING")
            if optimizer == Optimizer.TRIVIAL:
                assigned_gui_elements = assign_all.assign(gui_elements, current_task, max_capacity, num_slots)
            elif optimizer == Optimizer.GREEDY:
                assigned_gui_elements = optimize_greedy.assign(gui_elements, current_task, max_capacity, num_slots)
            elif optimizer == Optimizer.INTEGER_PROGRAM:
                assigned_gui_elements = optimize_integer_program.assign(gui_elements, current_task, max_capacity, num_slots)
            elif optimizer == Optimizer.QAP:
                assigned_gui_elements = optimize_qap.assign(gui_elements, current_task, max_capacity, num_slots)

            print_assigned_gui_elements_info()
            print("###############")
        elif key == ord('t'):
            current_task = (current_task + 1) % num_tasks
            print(f"Current task is {current_task}")
        elif key == ord('c'):
            max_capacity = max_capacity + 0.1
            print(f"Current capacity is {max_capacity:.2f}")
        elif key == ord('v'):
            max_capacity = max(max_capacity - 0.1, 0.0)
            print(f"Current capacity is {max_capacity:.2f}")

    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def load_gui_images():
    print("Loading GUI images.")
    imgs = []
    path = "./assets/images"
    valid_images = [".jpg"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue

        img_path = os.path.join(path, f)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (img_slot_size, img_slot_size))

        # cv2.imshow("image", img)
        # cv2.waitKey(0)

        imgs.append(img)
    return imgs


# Initializes the slots in which we can place gui element, and their position in the image
def init_slots():
    for i in range(0, num_slots):
        slot = Slot()
        slot.index = i
        slot.size = img_slot_size

        slot.x = offset

        if i >= 5:
            slot.x = img_width - img_slot_size - offset

        slot.y = offset * (1 + i % 5) + img_slot_size * (i % 5)
        slots.append(slot)

# Initializes the gui elements that are available to be placed in slots
def init_gui_elements():
    for i in range(0, num_gui_elements):
        name = "gui_element_" + str(i)
        image_index = i
        gui_element = GUI_Element(name, image_index)

        # Set how "expensive" it is to show a gui element, e.g., because distracting, or mentally straining
        # Values are normalized, so "expensive" items are closer to 1.
        # An element with a lot of text, for example, could be more cognitively straining than a simple icon
        gui_element.cost = random.random()
        gui_element.appearance = random.random()

        # Set how "important" a gui element is for individual tasks.
        # An email app, for example, could be highly important for productivity task (close to 1)
        # but not important for relaxing (close to 0)
        for t in range(0, num_tasks):
            gui_element.importance_per_task.append(random.random())

        gui_elements.append(gui_element)


gui = load_gui_images()
init_gui_elements()
init_slots()
start_video_capture()