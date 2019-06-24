import tkinter as tk
import sent_module as s

global textans
textans="None"
def ans():
    global textans
    resultwindow = tk.Toplevel()
    resultwindow.title("Result!")
    resultwindow.geometry("400x200")

    two = tk.Canvas(resultwindow, background='#fefdca')
    two.pack(expand=True, side='top', fill='both')
    if s.sentiment(textans) == "neg":
        l4 = tk.Label(two, text="Your review is negative!", font='Consolas 14 italic', padx=4, pady=4,
                      background='#ffde7d').place(x=120, y=75)
    else:
        l4= tk.Label(two, text="Your review is positive!", font='Consolas 14 italic', padx=4, pady=4,
                      background='#ffde7d').place(x=120, y=75)





mainwindow = tk.Tk()
mainwindow.title("Main Page")
mainwindow.configure(background='#fefdca')
mainwindow.geometry("800x400")

one=tk.Canvas(mainwindow,background='#fefdca')
one.pack(expand=True,side='top',fill='both')

sname=tk.StringVar(value=None)
l4=tk.Label (one,text="How was the movie? ",font='Consolas 14 italic',padx=4,pady=4,background='#ffde7d').place(x=250,y=150)
e4=tk.Entry(one,relief='ridge',font='Consolas 16 italic',textvariable=sname).place(x=250,y=200)

bsubmit= tk.Button(one,text="Submit",background='#738598',font="Consolas 14 italic",width=15,relief='ridge',padx=4,pady=4,command=lambda :ans2())
bsubmit.place(x=250,y=300)

def ans2():
    global textans
    textans=sname.get()
    ans()

mainwindow.mainloop()

