def formatter1(input_csv):
    import pandas as pd
    import numpy as np
    preferences_table = pd.DataFrame(np.array(pd.read_csv(input_csv).iloc[:, 1:])).rename(columns = {0:"N", 1:"P1", 2:"P2", 3:"P3"})
    for p_val in range(1, 4):
        p_val_string = "P" + str(p_val)    
        for position, value in enumerate(preferences_table[p_val_string]):
            if str(value) != "nan" and str(value) != "DO NOT CARE" and str(value) not in preferences_table["N"].values:
                preferences_table[p_val_string].values[position] = np.NaN
    preferences_table["P1"] = preferences_table["P1"].replace("DO NOT CARE", np.NaN)
    preferences_table = preferences_table.sample(frac = 1).reset_index(drop=True)
    del value, position, p_val_string, p_val, pd, np
    return preferences_table
def initial_pairs(formatted_table):    
    import pandas as pd
    initial_pairs = pd.DataFrame([["Person 1", "Person 2", "Strength"]])
    for position, person in enumerate(formatted_table["N"].values):
        p1, p2, p3 = formatted_table["P1"].values[position], formatted_table["P2"].values[position], formatted_table["P3"].values[position]
        if str(p1) == "nan" and str(p2) == "nan" and str(p3) == "nan":
            initial_pairs = initial_pairs.append([[person, formatted_table["N"].values[position - 1], 1]])
            initial_pairs = initial_pairs.append([[person, formatted_table["N"].values[position - 2], 1]])
            initial_pairs = initial_pairs.append([[person, formatted_table["N"].values[position - 3], 1]])
        else:
            try:
                counter = 1
                if person == formatted_table["P1"].values[list(formatted_table["N"].values).index(p1)]:
                    initial_pairs, counter = initial_pairs.append([[person, p1, 8]]), counter * 2
                if person == formatted_table["P2"].values[list(formatted_table["N"].values).index(p1)]:
                    initial_pairs, counter = initial_pairs.append([[person, p1, 7]]), counter * 2
                if person == formatted_table["P3"].values[list(formatted_table["N"].values).index(p1)]:
                    initial_pairs, counter = initial_pairs.append([[person, p1, 6]]), counter * 2
                if person == formatted_table["P1"].values[list(formatted_table["N"].values).index(p2)]:
                    initial_pairs, counter = initial_pairs.append([[person, p2, 7]]), counter * 3    
                if person == formatted_table["P2"].values[list(formatted_table["N"].values).index(p2)]:
                    initial_pairs, counter = initial_pairs.append([[person, p2, 6]]), counter * 3
                if person == formatted_table["P3"].values[list(formatted_table["N"].values).index(p2)]:
                    initial_pairs, counter = initial_pairs.append([[person, p2, 5]]), counter * 3
                if person == formatted_table["P1"].values[list(formatted_table["N"].values).index(p3)]:
                    initial_pairs, counter = initial_pairs.append([[person, p3, 6]]), counter * 5
                if person == formatted_table["P2"].values[list(formatted_table["N"].values).index(p3)]:
                    initial_pairs, counter = initial_pairs.append([[person, p3, 5]]), counter * 5
                if person == formatted_table["P3"].values[list(formatted_table["N"].values).index(p3)]:
                    initial_pairs, counter = initial_pairs.append([[person, p3, 4]]), counter * 5
            except ValueError as error:
                pass
            if counter % 2 != 0:
                initial_pairs = initial_pairs.append([[person, p1, 3]])                
            if counter % 3 != 0:
                initial_pairs = initial_pairs.append([[person, p2, 2]])
            if counter % 5 != 0:
                initial_pairs = initial_pairs.append([[person, p3, 1]])
    del p1, p2, p3, person, position, pd, counter, formatted_table
    return initial_pairs
def formatter2(pairs):
    import pandas as pd
    pairs, new_pairs, memory = pairs.dropna().iloc[1:], pd.DataFrame([[]]), []
    for row in pairs.values:
        if len(row[0]) > len(row[1]):
            new_pairs = new_pairs.append([[row[0], row[1], row[2]]])
        elif len(row[0]) < len(row[1]):
            new_pairs = new_pairs.append([[row[1], row[0], row[2]]])
        elif row[1] not in memory:
            memory.append(row[0])
            new_pairs = new_pairs.append([row])
        elif row[1] in memory:
            memory.remove(row[1])
            new_pairs = new_pairs.append([[row[1], row[0], row[2]]])
    new_pairs = new_pairs.drop_duplicates().iloc[1:]
    del pd, row, pairs, memory
    return new_pairs
def room_maker(formatted_table, formatted_pairs, rooms_sizes):
    import pandas as pd
    import numpy as np
    is_num = True
    try:
        rooms_sizes = rooms_sizes + 3 - 3
    except:
        is_num = False
        rooms_sizes.sort(reverse = True)
    net_pair_strengths = pd.DataFrame([[0, 0]])
    for pair in formatted_pairs.values:
        net_pair_strengths = net_pair_strengths.append([[pair[0], pair[2]]])
        net_pair_strengths = net_pair_strengths.append([[pair[1], pair[2]]])    
    net_pair_strengths, nps = net_pair_strengths.iloc[1:].sort_values(0).append(["sf", 0]), pd.DataFrame([[]])
    name, net_pair_strength = net_pair_strengths.values[0][0], 0
    for row in net_pair_strengths.values:
        if row[0] == name:
            net_pair_strength = net_pair_strength + row[1]
        else:
            nps, net_pair_strength = nps.append([[name, net_pair_strength]]), row[1]
        name = row[0]
    nps, rooms = nps.iloc[1:].sort_values(1).iloc[:-1], pd.DataFrame([[]])
    if is_num:
        rooms_sizes_list = []
        for i in range((len(formatted_table) // rooms_sizes) + 2):
            rooms_sizes_list.append(rooms_sizes)
        rooms_sizes = rooms_sizes_list
    for room in rooms_sizes:
        new_room = pd.DataFrame([[]])
        try:
            new_room, nps = new_room.append([nps.values[0][0]]).iloc[1:], nps.iloc[1:]
        except:
            break
        try:
            strengths = pd.DataFrame([[]])            
            for pair in formatted_pairs.values:
                if pair[0] == new_room[0][0]:
                    strengths = strengths.append([[pair[1], pair[2]]])
                elif pair[1] == new_room[0][0]:
                    strengths = strengths.append([[pair[0], pair[2]]])
            strengths = strengths.sort_values(1, ascending = False)
            new_room = new_room.append([strengths.values[0][0]])
            nps = nps[nps[0] != strengths.values[0][0]]        
        except:
            try:
                new_room = new_room.append([nps.values[0][0]])
                nps = nps.iloc[1:]
            except:
                pass
        for r in range(room - 2):
            try:
                strengths = pd.DataFrame([[]])
                for pair in formatted_pairs.values:
                    if pair[0] in new_room.values and pair[1] not in new_room.values:
                        strengths = strengths.append([[pair[1], pair[2]]])
                    elif pair[1] in new_room.values and pair[0] not in new_room.values:
                        strengths = strengths.append([[pair[0], pair[2]]])
                strength_sums, strengths = pd.DataFrame([[]]), strengths.dropna()
                name = strengths.values[0][0]
                strengths, strength_sum = strengths.append(["sf", 0]), 0
                for row in strengths.values:
                    if row[0] == name:
                        strength_sum = strength_sum + row[1]
                    else:
                        strength_sums = strength_sums.append([[name, strength_sum]])
                        strength_sum = row[1]
                    name = row[0]
                strength_sums = strength_sums.sort_values(1, ascending = False)
                new_room = new_room.append([strength_sums.values[0][0]])      
                nps = nps[nps[0] != strength_sums.values[0][0]]
            except:
                try:
                    new_room = new_room.append([nps.values[0][0]])
                    nps = nps.iloc[1:]
                except:
                    pass
        for person in new_room[0]:
            formatted_pairs = formatted_pairs[formatted_pairs[0] != person][formatted_pairs[formatted_pairs[0] != person][1] != person]
        new_room = pd.DataFrame(np.array(new_room).reshape(1, -1))
        rooms = rooms.append(new_room)
    return rooms
def SkiCampRoomMaker(input_csv, room_dimensions):
    return room_maker(formatter1(input_csv), formatter2(initial_pairs(formatter1(input_csv))), room_dimensions)


def SkiCampRooms():
    from tkinter import Tk, filedialog, Canvas, Entry, StringVar
    import time
    
    def ImportAction(event):
        global input_csv_file_name
        input_csv_file_name = filedialog.askopenfilename(filetypes=[("Comma-separated values files", "*.csv")])
        TemporaryMessages("Import Succesful!", 2, False)
        
    def TemporaryMessages(text, duration, is_error):
        if is_error:
            box_colour = "Red"
        else:
            box_colour = "#ff8a59"

        temp_confirmation_button = canvas.create_rectangle((400 - len(text) * 4), 30, (400 + len(text) * 4), 60, fill = box_colour)
        temp_confirmation_text = canvas.create_text(400, 45, font = ("Hind Madurai", 14), text = text)
        app.update()
        time.sleep(duration)
        canvas.delete(temp_confirmation_button)
        canvas.delete(temp_confirmation_text)
        app.update()
           
    def RoomsSizesInput(event):
        global rooms_sizes
        canvas.delete(rooms_sizes_text)
        rooms_sizes = StringVar()
        rooms_sizes_entry = Entry(canvas, textvariable = rooms_sizes, background = "#ff8a59", borderwidth = 0, width = 16)
        canvas.create_window(695, 45, window = rooms_sizes_entry)

    def MakeRooms(event):
        
        SkiCampRoomMaker(input_csv_file_name, rooms_sizes.get())
    
    def ExportJPG(event):
        pass
    
    def ExportCSV(event):
        pass
    
    def ShowHideInstructions(event):
        pass
    
    app = Tk()
    canvas = Canvas(app, width = 800, height = 600)
    canvas.pack()
    
    open_button = canvas.create_rectangle(20, 20, 220, 70, fill = "#ff8a59")
    canvas.tag_bind(open_button, "<1>", ImportAction)
    open_button_text = canvas.create_text(120, 45, font = ("Hind Madurai", 16), text = "Import CSV File")
    canvas.tag_bind(open_button_text, "<1>", ImportAction)
    
    rooms_sizes_space = canvas.create_rectangle(610, 20, 780, 70, fill = "#ff8a59")
    canvas.tag_bind(rooms_sizes_space, "<1>", RoomsSizesInput)
    rooms_sizes_text = canvas.create_text(695, 45, font = ("Hind Madurai", 16), text = "Enter Room Sizes...")
    canvas.tag_bind(rooms_sizes_text, "<1>", RoomsSizesInput)

    make_rooms_button = canvas.create_rectangle(20, 530, 170, 580, fill = "#6fa8dc")
    canvas.tag_bind(make_rooms_button, "<1>", MakeRooms)
    make_rooms_text = canvas.create_text(95, 555, font = ("Hind Madurai", 16), text = "Make Rooms")
    canvas.tag_bind(make_rooms_text, "<1>", MakeRooms)
    
    export_jpg_button = canvas.create_rectangle(190, 530, 350, 580, fill = "#0097a7")
    canvas.tag_bind(export_jpg_button, "<1>", ExportJPG)
    export_jpg_text = canvas.create_text(270, 555, font = ("Hind Madurai", 16), text = "Export as JPG")
    canvas.tag_bind(export_jpg_text, "<1>", ExportJPG)

    export_csv_button = canvas.create_rectangle(370, 530, 530, 580, fill = "#0097a7")
    canvas.tag_bind(export_csv_button, "<1>", ExportCSV)
    export_csv_text = canvas.create_text(450, 555, font = ("Hind Madurai", 16), text = "Export as CSV")
    canvas.tag_bind(export_csv_text, "<1>", ExportCSV)
    
    show_instructions_button = canvas.create_rectangle(550, 530, 780, 580, fill = "#6fa8dc")
    canvas.tag_bind(show_instructions_button, "<1>", ShowHideInstructions)
    show_instructions_text = canvas.create_text(665, 555, font = ("Hind Madurai", 16), text = "Show/Hide Instructions")
    canvas.tag_bind(show_instructions_text, "<1>", ShowHideInstructions)
#    e1 = Entry(canvas)
#    canvas.create_window(200, 80, window = e1)
#    
#    new_rooms = canvas.create_rectangle(360, 20, 480, 50, fill = "#ff8a59")
#    canvas.tag_bind(new_rooms, "<1>", RoomSizes)
#    new_rooms_text = canvas.create_text(420, 35, text = "Create New Rooms")
    
#    open_button = canvas.create_rectangle(360, 20, 480, 50, fill = "#ff8a59")
#    canvas.tag_bind(open_button, "<1>", MakeRooms)
    
#    open_button_text = canvas.create_text(420, 35, text = "Enter Room Sizes")
    
    canvas.update()
    
    app.mainloop()

SkiCampRooms()
