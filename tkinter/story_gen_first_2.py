import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import ImageTk, Image
from chatgpt_wrapper import ChatGPT
import requests
import shutil
import os
import re
import dalle

bot = ChatGPT()

def process_text(input_text):
    # Replace this with your own function that processes the input
    print("Inside process_text")
    output_text="passed"
    success, response, message = bot.ask(input_text)
    print("Got resp")
    if success:
        output_text = response
    else:
        output_text = message

    generated_story_text_file = open("./dynamically_gen_files/story.txt", "w")
    generated_story_text_file.write(output_text)
    generated_story_text_file.close()

    return output_text

def process_input():
    global char_list
    global trait_list
    # Get the input text from the text box
    input_text = input_box.get('1.0', 'end-1c')
    genre_text = genre_box.get('1.0', 'end-1c')
    intro_text = intro_box.get('1.0', 'end-1c')
    climax_text = climax_box.get('1.0', 'end-1c')
    input_prompt = 'Write an story '
    if genre_text:
        genre_string = ' based on '+ genre_text + ' genre '
        input_prompt+=genre_string
    if input_text:
        input_string = ' based on '+ input_text
        input_prompt+=input_string
    if char_list:
        character_string = ' with ' +str(len(char_list))+ ' characters with the names ' + str(char_list) +' and their corresponding traits being '+ str(trait_list) + '(note that the character names and traits are in the form of lists, so associate each character name index only to the same trait list index for generating the story)'
        input_prompt+=character_string
    if intro_text:
        intro_string = ' that starts with '+ intro_text
        input_prompt+=intro_string
    if climax_text:
        climax_string = ' that ends with '+ climax_text
        input_prompt+=climax_string

    print(input_prompt)
    output_text = process_text(input_prompt)

    # Create the output label and text box
    output_label = customtkinter.CTkLabel(frame, text='Generated story', anchor='center')
    output_label.pack(pady=5, fill='x')
    output_box = customtkinter.CTkTextbox(frame, height=900, width=400, state='disabled')
    output_box.pack(pady=10)
    output_box.configure(state='normal')
    output_box.delete('1.0', 'end')
    output_box.insert('end', output_text)
    output_box.configure(state='disabled')

    # Create the edit button
    edit_button = customtkinter.CTkButton(frame, text="Edit the story", command=open_textbox)
    edit_button.pack()
    
def calc():
    global x
    print("calc")
    x=0
    x=int(a.get())
    print(x)
    x=x-1
    create_character()

def gettingfunc(character_box,trait_box,character_label,trait_label,button2):
    root.after(0, button2.destroy)
    print("gettingfunc")
    character_text = character_box.get('1.0', 'end-1c')
    char_list.append(character_text)
    print(char_list)
    trait_text = trait_box.get('1.0', 'end-1c')
    trait_list.append(trait_text)
    print(trait_list)
    button_1 = customtkinter.CTkButton(root, text ="Finish", command = lambda:[character_box.destroy(),character_label.destroy(),trait_box.destroy(),trait_label.destroy(),add_character(button_1)])
    
    #Exteral padding for the buttons
    button_1.pack(pady = 40)

def add_character(button_1):
    root.after(0, button_1.destroy)
    button_1.destroy
    print("add character")
    global char_list
    global trait_list
    global x
    print(x)
    if(x>0):
        x=x-1
        create_character()

def create_character():
    print("create character")
    character_label = customtkinter.CTkLabel(root, text='Character Name', anchor='center')
    character_label.pack(pady=50, fill='x')
    character_box = customtkinter.CTkTextbox(root, height=1, width=50)
    character_box.pack(padx=0,pady=10)
    
    #character_box.config(command=character_box.pack_forget) 
    trait_label = customtkinter.CTkLabel(root, text='Character Traits', anchor='center')
    trait_label.pack(pady=5, fill='x')
    trait_box = customtkinter.CTkTextbox(root, height=1, width=50)
    trait_box.pack(padx=0,pady=10)
    #trait_box.config(command=trait_box.pack_forget) 
    button2 = customtkinter.CTkButton(root,text="Record Data",command=lambda:[gettingfunc(character_box,trait_box,character_label,trait_label,button2)])
    button2.pack(pady = 40)

def open_textbox():
    textbox = customtkinter.CTkTextbox(frame, height=30, width=400)
    textbox.pack()
    
    def get_edit_text():
        edit_text = textbox.get("1.0", "end-1c")
        return edit_text
    
    def show_output():
        edit_input_text = get_edit_text()
        with open('./dynamically_gen_files/story.txt', 'r') as file:
            data = file.read().replace('\n', '')
        # print("Read the in-dialogue story")
        edited_prompt = data + ' Build an edited story based on above story with new edits as '+ edit_input_text
        edit_output_text = process_text(edited_prompt)

        # Creating and displaying the output based on new prompt
        edit_output_label = customtkinter.CTkLabel(frame, text='Edited Story', anchor='center')
        edit_output_label.pack(pady=10, fill='x')
        edit_output_box = customtkinter.CTkTextbox(frame, height=900, width=400, state='disabled')
        edit_output_box.pack(pady=10)

        edit_output_box.configure(state='normal')
        edit_output_box.delete('1.0', 'end')
        edit_output_box.insert('end', edit_output_text)
        edit_output_box.configure(state='disabled')

    # Creating Submit button
    ok_button = ttk.Button(frame, text="OK", command= show_output)
    ok_button.pack()

def generate_character_profile():
    # Create the GUI
    char_win = customtkinter.CTkToplevel(frame)
    w, h = char_win.winfo_screenwidth(), char_win.winfo_screenheight()
    char_win.geometry("%dx%d+0+0" % (w, h))

    char_canvas = tk.Canvas(char_win)
    char_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = customtkinter.CTkScrollbar(char_win, command=char_canvas.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    char_canvas.configure(yscrollcommand=scrollbar.set)

    sub_frame = customtkinter.CTkFrame(char_canvas, height=200)
    char_canvas.create_window((0, 0), window=sub_frame, anchor='nw')

    char_canvas.configure(scrollregion=char_canvas.bbox('all'))
    char_canvas.bind('<Configure>', lambda e: char_canvas.configure(scrollregion=char_canvas.bbox('all')))

    generated_story_file = open("./dynamically_gen_files/story.txt", "r")
    generated_story = generated_story_file.read()
    generated_story_file.close()
    char_profile_prompt_file = open("./char_profile_prompt.txt")
    char_profile_prompt = char_profile_prompt_file.read()
    char_profile_prompt_file.close()
    fin_char_profile_prompt = generated_story + "\n" + char_profile_prompt
    
    success, response, message = bot.ask(fin_char_profile_prompt)

    if success:
        output_text = response
    else:
        output_text = message

    # Split the contents into separate character profiles
    print(output_text)
    profiles = output_text.split('##########\n')
    print(profiles)

    char_file_names = []

    # Process each character profile
    for i in range(1, len(profiles)):
        profile = profiles[i]

        name_regex = r"Name:\s*([\w.\s*,-]+)\n"
        name_match = re.search(name_regex, profile)
        if name_match:
            name = name_match.group(1)
        print("\n" + name)

        # Create a new file with the name of the character
        char_file_name = './dynamically_gen_files/char_' + name + '.txt'
        char_file_names.append(char_file_name)
        with open(char_file_name, 'w') as outfile:
            # Write the character's profile to the file
            outfile.write(profile)
            print("File created")

    # Create a frame to contain the text box and canvas
    bb_frame = customtkinter.CTkFrame(sub_frame)
    bb_frame.pack()

    # iterate over the file paths and create a text box for each file
    for i, file_path in enumerate(char_file_names):
        
        with open(file_path, "r") as f:
            contents = f.read()

            canvas_img = tk.Canvas(bb_frame, width=256, height=256)
            canvas_img.grid(row=i, column=1, padx=10, pady=10)

            url = dalle.generate_visual_character(contents + "\nGenerate a character which suits the above description")
            res = requests.get(url, stream = True)
            new_file_path = file_path[:-3] + "png"
            with open(new_file_path,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            
            char_text_box = customtkinter.CTkTextbox(bb_frame,  height=200, width=400, state='disabled')
            char_text_box.grid(row=i, column=0, padx=10, pady=10)
            char_text_box.configure(state='normal')
            char_text_box.delete('1.0', 'end')
            char_text_box.insert('end', contents)
            char_text_box.configure(state='disabled')

            img_tk = ImageTk.PhotoImage(Image.open(new_file_path))
            canvas_img.img_tk = img_tk
            canvas_img.create_image((10,10),anchor='nw',image=img_tk)


def cleanup():
    dir = './dynamically_gen_files'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


#cleanup of the dynamically gen files
cleanup()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Create the GUI
root = customtkinter.CTk()
root.state('zoomed')
root.title('ECS 289G - Short Story Long - Project')

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = customtkinter.CTkScrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.configure(command=canvas.yview)


canvas.configure(yscrollcommand=scrollbar.set)

frame = customtkinter.CTkFrame(canvas, height=2000)
canvas.create_window((0, 0), window=frame, anchor='nw')

canvas.configure(scrollregion=canvas.bbox('all'))
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))


# Create the input text box
genre_label = customtkinter.CTkLabel(frame, text='Description', anchor='center')
genre_label.pack(pady=5, fill='x')
input_box = customtkinter.CTkTextbox(frame, height=100, width=400)
input_box.pack()

genre_label = customtkinter.CTkLabel(frame, text='Genre', anchor='center')
genre_label.pack(pady=5, fill='x')
genre_box = customtkinter.CTkTextbox(frame, height=10, width=400)
genre_box.pack()

intro_label = customtkinter.CTkLabel(frame, text='Intro', anchor='center')
intro_label.pack(pady=5, fill='x')
intro_box = customtkinter.CTkTextbox(frame, height=10, width=400)
intro_box.pack()

climax_label = customtkinter.CTkLabel(frame, text='Climax', anchor='center')
climax_label.pack(pady=5, fill='x')
climax_box = customtkinter.CTkTextbox(frame, height=10, width=400)
climax_box.pack()

char_list=[]
trait_list=[]

customtkinter.CTkLabel(frame, text="Enter Number of Characters").pack()
a = customtkinter.CTkEntry(frame, width=35)
a.pack()
gen_button = customtkinter.CTkButton(frame, text='Enter Character Details', command=calc)
gen_button.pack(pady=10)

# Create the process button
process_button = customtkinter.CTkButton(frame, text='Generate a story', command=process_input)
process_button.pack(pady=10)


# Create the generate button
gen_button = customtkinter.CTkButton(frame, text='Generate Character profile', command=generate_character_profile)
gen_button.pack(pady=10)

# Start the GUI
root.mainloop()