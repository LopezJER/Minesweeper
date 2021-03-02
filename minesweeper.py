from tkinter import *
import random, time
from tkinter import messagebox

window=Tk()
window.title("M!nesweeper")
window.configure(bg="black")


board={}
button={}
diff={"Beginner":(8,8,10), "Intermediate":(16,16,40), "Expert":(16,30,99)}
dimensions={"height":0, "width":0, "mines":0,"first_move":True}
flagcount=IntVar() #associated with Info Label at the end of the code

#Functions
def show_menu(): 
	window.geometry("330x330")
	menu_frame.grid()
	letters=["M","!","N","E","S","W","E","E","P", "E", "R"]
	buttons={}
	letterframe.grid(pady=25)
	optionframe.grid(pady=5)
	window.config(cursor="none")
	for i in range (len(letters)):
		buttons[i]=Button(letterframe, text=letters[i], bg="black", font=("courier",13, "bold"), width=2, height=1, fg="white")
		buttons[i].grid(row=0, column=i)
		time.sleep(0.05)
		buttons[i].update()
	for i in range(3):
		buttons[1].flash()
	

	newgame_btn=Button(optionframe, bg="black", fg="white", font=("courier", 13), text="NEW GAME", width=10, bd=2, command=ask_difficulty)
	continue_btn=Button(optionframe, bg="black",fg="white",  font=("courier", 13), text="CONTINUE", width=10, bd=2, command=call_continue)
	about_btn=Button(optionframe, bg="black", fg="white", font=("courier", 13),text="ABOUT", width=10, bd=2, command=about_topics)
	exit_btn=Button(optionframe, bg="black", fg="white", font=("courier" ,13), text="EXIT", width=10, bd=2, command=exit_game)

	newgame_btn.grid(row=1, pady=7)
	continue_btn.grid(row=2, pady=7)
	about_btn.grid(row=3,  pady=7)
	exit_btn.grid(row=4,  pady=7)
		
	fr=open("save.txt", "r")
	if fr.read()=="": continue_btn.configure(state=DISABLED)
	fr.close()
	
	window.config(cursor="arrow")
def ask_difficulty():
	if dimensions["first_move"]==False: #when a player stops playing and starts a new game
		dimensions["first_move"]=True
		clear_save()
	menu_frame.grid_forget()
	letterframe.grid_forget()
	optionframe.grid_forget()
	
	for k,v in diff.items():
		lvl_button.append(Button(lvl_frame, text=k, bg="black", fg="white", font=("Courier", 13), command=lambda h=v[0], w=v[1], m=v[2]: spec_dimensions(h,w,m)))#a list of buttons for easier deletion
		lvl_button[-1].pack(padx=10,pady=10)
	caption.pack(pady=10, ipady=10)
	lvl_frame.pack(pady=40)
	
def spec_dimensions(h,w,m):
	caption.pack_forget()
	lvl_frame.pack_forget()
	dimensions["height"]=h
	dimensions["width"]=w
	dimensions["mines"]=m
	init_board()
	
def config_window():
	if dimensions["height"]==8 and dimensions["width"]==8:
		window.geometry("350x350")
	elif dimensions["height"]==16 and dimensions["width"]==16:
		window.geometry("520x650")
	elif dimensions["height"]==16 and dimensions["width"]==30:
		window.geometry("1200x650")
		
def init_board():
	for i in lvl_button: i.destroy()
	lvl_frame.grid_forget()
	config_window()
	for i in range(dimensions["height"]):
		board[i]={}
		button[i]={}
		frame[i]=Frame(newgame_frame, bg="black")
		frame[i].pack()
		for j in range(dimensions["width"]):
			board[i][j]=-1
			button[i][j]=Button(frame[i], text='?', bg="black", font=("arial",13, "bold"), width=2, height=1, fg="black", command=lambda row=i, col=j: check_position(row, col)) # next function call 
			button[i][j].bind("<Button-3>", put_flag)
			button[i][j].pack(side=LEFT)
	flagcount.set(dimensions["mines"])
	info.pack(side=RIGHT)
	back.pack(side=LEFT)
	newgame_frame.pack(pady=30)
	
def put_mines(row,col):
	list=[]
	count=0
	while count!=dimensions["mines"]:
		randrow=random.randint(0,dimensions["height"]-1)
		randcol=random.randint(0,dimensions["width"]-1)
		if board[randrow][randcol]==-1 and (randrow,randcol)!=(row,col):
			board[randrow][randcol]=-99
			count+=1
			list.append([randrow,randcol])
	print(list)
	showClues(row,col)

def check_position(row, col):
	if dimensions["first_move"]==False:
		if board[row][col]==-99:
			count=0
			while count!=6:
				button[row][col].flash()
				count+=1
			button[row][col].configure(text='X', fg="white", font="bold", relief=GROOVE)
			for i in range (dimensions["height"]):
				for j in range(dimensions["width"]):
					if board[i][j]!=-99:
						button[i][j].configure(bg="white", fg="white", relief=SUNKEN, state=NORMAL)
					else:
						button[i][j].configure(text='X', fg="white", bg="black", font=("arial", 13, "bold"), relief=RAISED)
			messagebox.showinfo("Game over.", "You Lose!!!")
			dimensions["first_move"]=True
			window.config(cursor="arrow")
			pack_up()
		else: showClues(row, col)
	else:
		dimensions["first_move"]=False
		put_mines(row,col)

	
def showClues(row, col):
	color={1:"gray42",2:"gray31",3:"gray21",4:"gray11",5:"gray9",6:"gray6",7:"gray3",8:"gray1"} 
	n=0
	tiles=[[i,j] for i in range (row-1, row+2)
		for j in range (col-1, col+2)
		if (0<=i<=(dimensions["height"]-1) and 0<=j<=(dimensions["width"]-1)) and (i,j)!=(row,col)]
	for i in range (len(tiles)):
		c,d=tiles[i][0],tiles[i][1]
		if board[c][d]==-99:
			n+=1
	board[row][col]=n
	if n>0: 
		button[row][col].configure(text=n, bg=color[n], width=2, height=1, fg="white", relief=SUNKEN)
	elif n==0:
		button[row][col].configure(bg="gray", text="", relief=SUNKEN)
		for i in range (len(tiles)):
			c,d=tiles[i][0],tiles[i][1]
			if board[c][d]==-1 and button[c][d]["state"]=="normal":
				showClues(c, d)
	check_win()
	
def check_win():
	emptyspace=False
	for i in range(len(board)):
		for j in range (len(board[i])):
			if board[i][j]==-1:
				emptyspace=True
				break
		if emptyspace==True:
			break
	else: 
		for i in range(dimensions["height"]):
			for j in range (dimensions["width"]):
				if board[i][j]==-99:
					button[i][j].configure(bg="yellow")
				button[i][j].pack()
		messagebox.showinfo("Congratulations!", "You cleared the field!")
		for i in range(len(board)):
			frame[i].pack_forget()
			for j in range(len(board[0])):
				button[i][j].destroy()
		dimensions["first_move"]=True
		pack_up()
		show_menu()

def call_continue():
	i=0
	flags_used=0
	fr=open("save.txt","r")
	for line in fr:
		board[i]={}
		button[i]={}
		frame[i]=Frame(newgame_frame,bg="black")
		frame[i].pack()
		tiles=line[:-2].split("|")
		for j in range(len(tiles)):
			attribute=tiles[j].split(":")
			board[i][j]=int(attribute[0])
			button[i][j]=Button(frame[i], text=attribute[1], bg=attribute[2], font=attribute[3], fg=attribute[4], state=attribute[5], width=2, height=1, command=lambda row=i, col=j: check_position(row, col))
			if button[i][j]["fg"]=="grey" or button[i][j]["state"]=="disabled": flags_used+=1
			button[i][j].bind("<Button-3>", put_flag)
			button[i][j].pack(side=LEFT)
		i+=1
	j=len(tiles)
	dimensions["height"], dimensions["width"], =i,j
	if (i,j)==(8,8): dimensions["mines"]=10
	elif (i,j)==(16, 16): dimensions["mines"]=40
	else: dimensions["mines"]=99
	dimensions["first_move"]==False
	fr.close()
	menu_frame.grid_forget()
	letterframe.grid_forget()
	optionframe.grid_forget()
	config_window()
	flagcount.set(dimensions["mines"]-flags_used)
	info.pack(side=RIGHT)
	back.pack(side=LEFT)
	newgame_frame.pack(pady=30)

def put_flag(event):
	if event.widget["state"]=="normal" and event.widget["text"]=="?":
		print("Here")
		event.widget.configure(fg="grey", state=DISABLED)
		flagcount.set(flagcount.get()-1)
	elif event.widget["state"]=="disabled":
		event.widget.configure(fg="black",state=NORMAL)
		flagcount.set(flagcount.get()+1)	

def pack_up():
	if dimensions["first_move"]==True: clear_save() #when the player has either won or lost already
	else: 
		save_state()
		dimensions["first_move"]=True
	for i in range(dimensions["height"]):
		frame[i].pack_forget()
		for j in range(dimensions["width"]):
			button[i][j].destroy()
	back.pack_forget()
	info.pack_forget()
	newgame_frame.pack_forget()
	board.clear()
	button.clear()
	show_menu()

def save_state():
	fw=open("save.txt", "w")
	for i in range(dimensions["height"]):
		for j in range (dimensions["width"]):
			fw.write(str(board[i][j])+":"+str(button[i][j]["text"])+":"+button[i][j]["bg"]+":"+button[i][j]["font"]+":"+button[i][j]["fg"]+":"+button[i][j]["state"]+"|")
		fw.write("\n")
	fw.close()

def clear_save():
	fr=open("save.txt", "w")
	fr.write("")
	fr.close()
	
def about_topics():
	about = Toplevel()
	about.configure(bg="black")
	about.title("About")
	lblframe=LabelFrame(about, text="A few questions?", bg="black", font=11 ,fg="white")
	about_message="\n" + "Q: How do I win?" + "\n"+ "	Easy! All you have to do is to clear the minefield without exploding to pieces. When you step on a tile, three things may happen. One, it will reveal a digit which tells you how many of the tiles adjacent to you contain a bomb. Two, it will clear up along with other adjacent tiles until they encounter a tile next to a bomb." + "\n" + "Three, it may explode; you stepped on a mine. Yikes!" + "\n" + "	Your goal is to click the tiles until you are left only with the mines. You may also use flags to mark the tiles you think contain bombs." + "\n" + "\n" + "Q: Who are you?" + "\n" + "	Who, me? Well, I programmed this game. I'm satisfied with it because I know it works and so far, I have resolved every bug I've encountered. I don't know if there are more. Do you like the style? Minimalism is my thing. Although I'm not sure if the application is as efficient as one might have hoped. That's why I've decided to take higher Computer Science courses next semester. I want to make apps that not only work but are also efficient. I'm also interested in learning about abstract data types."  + "\n" + "\n" + "							Iking"+"\n"+"							05-17-18"

	msg = Message(lblframe, text=about_message, bg="black", font=12, fg="white")
	msg.pack()
	lblframe.pack()
	button = Button(about, text="OK, thanks!", command=about.destroy, bg="black", fg="white", font=12, height=2)
	button.pack()

def exit_game():
	if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
		if dimensions["first_move"]==False: save_state()
		window.destroy()

#Interface Elements
newgame_frame=Frame(window, bg="black")
menu_frame=Frame(window, bg="black")
menu_frame=Frame(window, bg="black")
letterframe=Frame(menu_frame, width=9)
optionframe=Frame(menu_frame, bg="black")
lvl_frame=Frame(window, bg="black")
caption=Label(lvl_frame, text="Choose level of difficulty.", font=("courier", 11))
info=Label(newgame_frame, bg="grey25", height=2,fg="white", font=("arial", 12, "bold"), textvariable=flagcount)
back=Button(newgame_frame, text="<", bg="grey25", height=2, fg="white", font=("arial", 12, "bold"), command=pack_up)
lvl_button=[]
frame={}


window.protocol("WM_DELETE_WINDOW", exit_game) #modified protocol
	
show_menu()

window.mainloop()
