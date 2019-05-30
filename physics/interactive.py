# coding: utf-8

import PIL.Image
import PIL.ImageDraw
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
    refracted_angle = cal_refracted_angle(incident_angle, mediums[0], mediums[1])

    width = 1024.0
    height = 1024.0
    im = PIL.Image.new('RGB', (int(width),int(height)), (255,0,0))
    draw = PIL.ImageDraw.Draw(im)

    draw.rectangle([(0, 0),(width, height/2)], fill="#e8f6f3", outline=None)
    draw.rectangle([(0, height/2),(width, height)], fill="#abd5ee", outline=None)

    draw.line([(0, height/2),(width, height/2)], fill="black")
    draw.line([(width/2, 0),(width/2, height)], fill="black")

    if incident_angle < 45:
        incident_y = math.tan(math.radians(incident_angle))*(height/2)
        incident_line = [((width/2)-incident_y, 0),(width/2, height/2)]
    else:
        incident_y = math.tan(math.radians(90-incident_angle))*(width/2)
        incident_line = [(0, (height/2)-incident_y),(width/2, height/2)]
    draw.line(incident_line, fill="red")

    incident_line_mid = ((incident_line[0][0] + incident_line[1][0])/2.0, (incident_line[0][1] + incident_line[1][1])/2.0)

    # incident_line_slope = (incident_line[0][1] - incident_line[1][1])/(incident_line[0][0] - incident_line[1][0])
    arrow_size = width/32
    draw.line([(incident_line[0][0] - arrow_size, incident_line[0][1]), (incident_line[1][0] - arrow_size, incident_line[1][1])], fill="blue")
    draw.line([(incident_line[0][0] + arrow_size, incident_line[0][1]), (incident_line[1][0] + arrow_size, incident_line[1][1])], fill="green")

    incident_line_1_mid = ((incident_line[0][0] - arrow_size + incident_line[1][0] - arrow_size)/2.0, (incident_line[0][1] + incident_line[1][1])/2.0)
    incident_line_2_mid = ((incident_line[0][0] + arrow_size + incident_line[1][0] + arrow_size)/2.0, (incident_line[0][1] + incident_line[1][1])/2.0)

    draw.line([incident_line_mid, (incident_line_1_mid[0] - (arrow_size/2), incident_line_1_mid[1] - (arrow_size/2))], fill="black")
    draw.line([incident_line_mid, (incident_line_2_mid[0] - arrow_size, incident_line_2_mid[1] - arrow_size)], fill="black")

    if refracted_angle < 45:
        refracted_y = math.tan(math.radians(refracted_angle))*(height/2)
        refracted_line = [(width/2, height/2),(width, (height/2)+refracted_y)]
    else:
        refracted_y = math.tan(math.radians(90-refracted_angle))*(width/2)
        refracted_line = [(width/2, height/2),((width/2)+refracted_y, height)]
    draw.line(refracted_line, fill="red")

    refracted_line_mid = ((refracted_line[0][0] + refracted_line[1][0])/2, (refracted_line[0][1] + refracted_line[1][1])/2)

    draw.line([(refracted_line[0][0] - arrow_size, refracted_line[0][1]), (refracted_line[1][0] - arrow_size, refracted_line[1][1])], fill="blue")
    draw.line([(refracted_line[0][0] + arrow_size, refracted_line[0][1]), (refracted_line[1][0] + arrow_size, refracted_line[1][1])], fill="green")

    refracted_line_1_mid = ((refracted_line[0][0] - arrow_size + refracted_line[1][0] - arrow_size)/2.0, (refracted_line[0][1] + refracted_line[1][1])/2.0)
    refracted_line_2_mid = ((refracted_line[0][0] + arrow_size + refracted_line[1][0] + arrow_size)/2.0, (refracted_line[0][1] + refracted_line[1][1])/2.0)

    draw.line([refracted_line_mid, (refracted_line_1_mid[0] - (arrow_size/2), refracted_line_1_mid[1] - (arrow_size/2))], fill="black")
    draw.line([refracted_line_mid, (refracted_line_2_mid[0] - arrow_size, refracted_line_2_mid[1] - arrow_size)], fill="black")

    # diff = 10
    # draw.line([incident_line_mid, (incident_line_mid[0]-diff,incident_line_mid[1]-diff)], fill="black")
    # draw.line([incident_line_mid, (incident_line_mid[0]+diff,incident_line_mid[1]-diff)], fill="black")
    #
    # draw.line([refracted_line_mid, (refracted_line_mid[0]-diff,refracted_line_mid[1]-diff)], fill="black")
    # draw.line([refracted_line_mid, (refracted_line_mid[0]+diff,refracted_line_mid[1]-diff)], fill="black")

    im.show()

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
