###########
# IMPORTS #
###########

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd #Seems redundant, but try this:
# >>> from tkinter import *
# >>> file<Tab>
#     |------|
#     |filter|
#     |float |
#     |format|
#       ...
# >>> from tkinter import filedialog
# >>> file<Tab>
#        vvv
# >>> filedialog
import random

####################
# ENCRYPTION SETUP #
####################
def encode(f, n, k): 
    random.seed(k)
    f = open(f, "bw+") 
    for i in n:
        f.write(bytes(0).fromhex(("00" + hex((i-random.randint(0,255))%256)[2:])[-2:]))

def decode(f, n, k): 
    random.seed(k)
    f = open(f, "bw+") 
    for i in n:
        f.write(bytes(0).fromhex(("00" + hex((i+random.randint(0,255))%256)[2:])[-2:]))

def hasher(n):
    hsh = 0
    for i in n:
        hsh *= 128
        hsh += ord(i)
    return 
        
#############
# GUI SETUP #
#############
w = Tk()
w.title("NCrypt")

errLabel = Label()
errLabel.grid(row=5, column = 1)
def error(txt):
    global errLabel
    errLabel.config(text=txt)
error("")
Label(w, text= #Don't worry aoout weird indent, it will be fine.
"""   |\  | /¯¯¯\ |¯¯¯\ \   / |¯¯¯\ ¯¯T¯¯ 
| \ | |     |___/  \ /  |___/   |
|  \| |     |  \    |   |       |
|   | \___/ |   \   |   |       |""", height=4, font="monospace").grid(
    row=0, column=0, columnspan=2
)

mode = "e"
fOut = None
fIn  = None
key  = StringVar()

def inF():
    global fIn
    tmp = fd.askopenfilename()
    if tmp == "":
        error("")
        return
    else:
        fIn = tmp
    inB.config(text="In: " + fIn)
    error("")

inB = Button(text="Select input file", command=inF)
inB.grid(row=1, column=0)


def outF():
    global fOut
    tmp = fd.asksaveasfilename()
    if tmp == "":
        error("")
        return
    else:
        fOut = tmp
    outB.config(text="Out: " + fOut)
    error("")

outB = Button(text="Select output file", command=outF)
outB.grid(row=1, column=1)


def modeF():
    global mode, modeB
    mode = ("e" if mode == "d" else "d")
    modeB.config(text="Mode: %scrypt" % ("En" if mode == "e" else "De"))
    error("")

modeB = Button(text="Mode: Encrypt", command=modeF)
modeB.grid(row=2, column=0, columnspan=2)


Label(text="Key:").grid(row=3, column=0)
keyE = Entry(show="\u2022", width=15, textvariable=key)
keyE.grid(row=3, column=1)


def goF():
    global fIn, fOut, encode, decode, mode, key
    error("%scrypting..." % ("En" if mode == "e" else "De"))
    if(fIn == None):
        error("No input selected.")
        return
    elif(fOut == None):
        error("No output selected.")
        return
    elif(key.get() == ""):
        if messagebox.askquestion(
            "No Key",
            "You have not entered a key.\nDoing so is recommended.\nContinue?",
            icon = 'warning'
        ) != "yes":
            return
    f = open(fIn, "br")
    data = f.read()
    f.close()
    func = (encode if mode == "e" else decode)
    func(fOut, data, key.get())
    error("%scrypted." % ("En" if mode == "e" else "De"))

Label().grid(row=4, column=0)
goB = Button(text="Go!", command=goF)
goB.grid(row=5, column=0, columnspan=2)

w.mainloop()
