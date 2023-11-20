import json
import requests
import urllib.request
from PIL import ImageTk
import PIL.Image
import tkinter as tk
from tkinter import *
import os.path


ford = {"make":"Ford", "model":"Mustang", "year":1969, "course": 320000,"price": 10000}
audi = {"make":"Audi", "model":"A4", "year":2004, "course": 120000, "price": 5000}
bmw = {"make":"BMW", "model":"M3", "year":2010, "course": 100000, "price": 15000}
mercedes = {"make":"Mercedes", "model":"C", "year":2015, "course": 80000, "price": 20000}
cars = [ford, audi, bmw, mercedes]

def json_reader(filename):
    with open(filename) as f:
        for line in f:
            yield json.loads(line)
def json_writer(file, json_objects):
    with open(file, "w") as f:
        for jsonobj in json_objects:
            jsonstr = json.dumps(jsonobj)
            f.write(jsonstr + "\n")

json_writer("cars.json", cars)
list_of_cars = list(json_reader("cars.json"))


def api_responses():

    url = "https://api.edenai.run/v2/text/generation"
    url_img = "https://api.edenai.run/v2/image/generation"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzgyNjhiOTMtM2U4NC00YWI4LTk5YjYtMzU5NzgxZmYwNjQzIiwidHlwZSI6bnVsbCwibmFtZSI6bnVsbCwiaXNfY3VzdG9tIjp0cnVlfQ.mSH_u7eE_jJADlmFmss3KYYJD73OSuKX3hI4JOXoHBI"
    }
    list_of_responses = []
    list_of_images = []

    #print(response_img['openai']['items'][0]['image_resource_url'])
    #print(response['openai']['generated_text'])

    for value in json_reader("cars.json"):
        payload = {
            "response_as_dict": True,
            "attributes_as_list": False,
            "show_original_response": False,
            "temperature": 0,
            "max_tokens": 1000,
            "text": f"Give me a convincing sale offer for this car {value}",
            "providers": "openai"
        }
        response = requests.post(url, json=payload, headers=headers)
        response = response.json()
        response = response['openai']['generated_text']
        response = response.replace("\n", "")
        response = response + "\n"
        list_of_responses.append(response)
        payload_img = {
            "response_as_dict": True,
            "attributes_as_list": False,
            "show_original_response": False,
            "resolution": "256x256",
            "num_images": 1,
            "providers": "replicate",
            "text": f"detailed image of the outside of the whole car {value}"
        }
        response_img = requests.post(url_img, json=payload_img, headers=headers)
        response_img = response_img.json()
        img_url = response_img['replicate']['items'][0]['image_resource_url']
        list_of_images.append(img_url)

    i=0
    while i<len(list_of_images):
        urllib.request.urlretrieve(list_of_images[i], f"car{i}.jpg")
        i+=1

    with open(r'description.txt', 'w') as fp:
        for item in list_of_responses:
            fp.write(item)


path = "car0.jpg"
path_desc = "description.txt"
check_desc = os.path.isfile(path_desc)
check = os.path.isfile(path)
if check == False or check_desc == False:
    api_responses()

list_of_responses = []
list_of_makes = []
for i in list_of_cars:
    list_of_makes.append(i['make'])

with open("description.txt", 'r') as fp:
    for line in fp:
        x = line[:-1]
        list_of_responses.append(x)
print(list_of_responses[0])
def select_callback(event):
    getval = event.widget.curselection()
    temp_car = list_of_cars[getval[0]]
    temp_desc = list_of_responses[getval[0]]
    car_make = temp_car['make']
    car_model = temp_car['model']
    car_year = temp_car['year']
    car_course = temp_car['course']
    car_price = temp_car['price']
    car_img = PIL.Image.open(f"car{getval[0]}.jpg")
    car_img = car_img.resize((200, 200))
    car_img = ImageTk.PhotoImage(car_img)
    label_img = Label(root, image=car_img)
    label_img.image = car_img
    label_img.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
    label_make.config(text = f"Car Make: {str(car_make)}")
    label_model.config(text = f"Model: {str(car_model)}")
    label_year.config(text = f"Production Year: {str(car_year)}")
    label_course.config(text = f"Car Course: {str(car_course)}km")
    label_price.config(text = f"Price: {str(car_price)}$")
    label_response.config(text = f"Description: \n\n{str(temp_desc)}")
#Window
root = Tk()
root.title("Car Sales")
root.geometry("800x500")
root.resizable(0, 0)
#Widgets
listvar=StringVar()
listvar.set(list_of_makes)
listbox=Listbox(root, height=10, width=10, listvariable=listvar, font="arial 10")
listbox.grid(row=0, column=0, padx=10, pady=10)
label_make = Label(root, text=f"Car Make: ", font="georgia 10 ")
label_make.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
label_model = Label(root, text=f"Model: ", font="georgia 10 ")
label_model.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
label_year = Label(root, text=f"Production Year: ", font="georgia 10 ")
label_year.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
label_course = Label(root, text=f"Car Course: ", font="georgia 10 ")
label_course.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)
label_price = Label(root, text=f"Price: ", font="georgia 10 ")
label_price.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)
label_response = Label(root, text=f"Description: ", font="georgia 10 ", width=50,justify=CENTER, wraplength=300)
label_response.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5, rowspan=6)
#Event
listbox.bind("<<ListboxSelect>>", select_callback)
#Mainloop
root.mainloop()
