import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from io import BytesIO
import requests
import sys
from threading import Thread
from time import sleep
import os

def get_token():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        print("NO TOKEN PROVIDED, PROVIDE ONE NOW, THIS MAY BE BECAUSE NORMAL SETUP WAS SKIPPED!")
        token = input("ENTER HERE: ")
        if not token:
            os.system("py minispottest.py")
        return token

def make_api_request(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "item" in data:
            return [data["item"]["name"], data['item']['album']['images'][0]['url'], data['item']['album']['artists'][0]['name']]
    else:
        print("ERROR! FAIL")
        print("Status Code:", response.status_code)

def update_gui_with_song_info(root, sng, art, url):
    image_url = url
    response = requests.get(image_url)
    global song
    global authortxt
    global txtf
    global label
    try:
        txtf.pack_forget()
        song.pack_forget()
        authortxt.pack_forget()
        label.pack_forget()
    except Exception as e:
        print(e)
    if response.status_code == 200:
        image_data = response.content
        image_bytes_io = BytesIO(image_data)
        image = Image.open(image_bytes_io)
        w, h = image.size
        left, top, right, bottom = 0, 0, w, h
        im1 = image.crop((left, top, right, bottom))
        resized_image = im1.resize((120, 120))
        photo = ImageTk.PhotoImage(resized_image)

        songtxt = sng
        authortxt = art

        txtf = Frame(root, width=200, height=100)
        song = Label(txtf, text=songtxt, font=("8514OEM", 18))
        authortxt = Label(txtf, text=authortxt, font=("8514OEM", 12))

        label = tk.Label(root, image=photo)
        label.image = photo
        label.pack(side=LEFT)
        txtf.pack(side=RIGHT)
        authortxt.pack(pady=2)
        song.pack()
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")

def create_gui():
    root = tk.Tk()
    root.title("Image Viewer")
    root.configure(background='black')
    return root

def for_now_req():
    root = create_gui()
    old_song = None
    while True:
        sleep(1.5)
        current_song = make_api_request(token)
        
        if current_song != old_song and current_song[1] is not None:
            print("Song changed!")
            print("New song:", current_song)
            update_gui_with_song_info(root, current_song[0], current_song[2], current_song[1])
            root.update()
            old_song = current_song

if __name__ == "__main__":
    token = get_token()
    Thread(target=for_now_req).start()
    tk.mainloop()  # Start the Tkinter main loop
