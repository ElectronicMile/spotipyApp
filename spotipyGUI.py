

currentWidgets = []
bgcolor = "#2ECC71"

master.configure(background=bgcolor)

master.title("Spotipy GUI")
master.geometry("800x800")

queryframe = LabelFrame(master, text="Query", borderwidth=3, padx=5, pady=5, relief=GROOVE, bg=bgcolor)
queryframe.grid(row=0, column=0, sticky=E + W + N + S)

resultframe = LabelFrame(master, text="Result", borderwidth=3, padx=5, pady=5, relief=GROOVE, bg=bgcolor)
resultframe.grid(row=1, column=0, sticky=E + W + N + S)

controlframe = LabelFrame(master, text="Play", borderwidth=1d, padx=5, pady=5, relief=GROOVE, bg=bgcolor)
controlframe.grid(row=0, column=1, sticky=E + N)

welcome = Label(queryframe, text="Welcome.", bg=bgcolor)
welcome.grid(sticky=W, column=0, row=0)

lbl = Label(queryframe, text="Enter an album URI:", bg=bgcolor)
lbl.grid(sticky=W, column=0, row=1)

txt = Entry(queryframe, width=30, bg="#229954")
txt.grid(sticky=W, column=0, row=2)
txt.focus()
txt = txt

btn = Button(queryframe, text="Enter", command=search, bg=bgcolor)
btn.configure(background="grey")
btn.grid(sticky=W, column=0, row=3)

errorText = Label(resultframe, text="Invalid URI", bg=bgcolor)

playbtn = Button(controlframe, text="play", bg=bgcolor)
playbtn.grid(sticky=W, column=0, row=1)

master.bind('<Return>', search2)
master.bind('<Command-a>', selectall)
#master.bind('<Control-a>', selectall) Will work for Windows?


