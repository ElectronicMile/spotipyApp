from io import BytesIO
import Tkinter as tk
import urllib  # not urllib.request
from PIL import Image, ImageTk

root = tk.Tk()
url = "http://imgs.xkcd.com/comics/python.png"

u = urllib.urlopen(url)
raw_data = u.read()
u.close()

im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)
label = tk.Label(image=image)
label.pack()
root.mainloop()