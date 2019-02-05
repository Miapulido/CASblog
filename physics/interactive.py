# coding: utf-8

from Tkinter import *
import math

medium_indices = {
  "vacuum": 1,
  "water": 1.33,
  "acetone": 1.36,
  "quartz": 1.46,
  "crown glass": 1.52,
  "sapphire": 1.77,
  "diamond": 2.42
}

def cal_refracted_angle(incident_angle, medium_1, medium_2):
    index_1 = medium_indices[medium_1]
    index_2 = medium_indices[medium_2]

    sin_incident_angle = math.sin(math.radians(incident_angle))
    refracted_angle_radians = math.asin((sin_incident_angle*index_1)/index_2)
    return math.degrees(refracted_angle_radians)

def calculate_from_input():
    incident_angle = float(incident_angle_input.get())
    mediums = []
    for i in range(2):
        mediums.append(medium_list_options[medium_lists[i].curselection()[0]])
    print cal_refracted_angle(incident_angle, mediums[0], mediums[1])

ui = Tk()

incident_angle_label = Label(ui, text="Incident Angle (°)")
incident_angle_label.grid(row=0,column=0)

incident_angle_input = Entry(ui)
incident_angle_input.grid(row=0,column=1)

medium_list_options = medium_indices.keys()
medium_lists = []
for i in range(2):
    curr_row = i+1
    curr_medium_label = Label(ui, text="Medium " + str(curr_row))
    curr_medium_label.grid(row=curr_row,column=0)

    curr_medium_list = Listbox(ui, selectmode=SINGLE, exportselection=0)
    i = 1
    for medium in medium_list_options:
        curr_medium_list.insert(i, medium)
        i += 1
    curr_medium_list.grid(row=curr_row,column=1)
    medium_lists.append(curr_medium_list)

run_button = Button(ui, text='Run', command=calculate_from_input)
run_button.grid(row=3,column=1)

ui.mainloop()
