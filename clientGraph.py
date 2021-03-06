import tkinter as tk
from tkinter import ttk
from tkinter import *
from client import Client
from tkinter import scrolledtext

class MainWindow(tk.Tk):    
    def __init__(self, *args, **kwargs):          
        tk.Tk.__init__(self, *args, **kwargs)
        #window config
        self.title("TCh4t")
        self.iconbitmap("logo.ico")
        self.menuBar()
        self.mainContainer()   
        self.showFrame(HomeFrame)

    def mainContainer(self):
        container = tk.Frame()  
        container.pack(expand=YES)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}  
        for F in (HomeFrame, TchatBoxFrame):  
            frame = F(container, self)
            frame.configure(bg='#41B77F')
            self.frames[F] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    def passDataDialog(self, text):
        self.frames[self.pages[1]].get_text(text)

    def menuBar(self):
        menu_bar = Menu(self)
        #premier menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quitter", command=self.quit)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        #configurer (ajouter la menu bar)
        self.config(menu=menu_bar)



class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.createWidgets()

    #initialisation de tous les composants
    def createWidgets(self):
        self.createTitreInput()
        self.createUsernameInput()
        self.createServerInput()
        self.createPortInput()
        self.createValidateButton()

    def createTitreInput(self):
        label_title = Label(self, text="TCh4t", font=("Courrier", 40), bg='#41B77F',
                            fg='white')
        label_subtitle = Label(self,text="Bienvenue sur la messagerie en ligne !", font=("Courrier", 20),bg='#41B77F',
                            fg='white')
        label_title.pack(pady=(80,0))
        label_subtitle.pack(pady=(0,20))

    def createUsernameInput(self):
        label_username = Label(self, text="Pseudo", font=("Courrier", 25), bg='#41B77F',
                               fg='white')
        label_username.pack()
        self.username_entry = Entry(self, font=("Helvetica", 20), bg='#4065A4', fg='white')
        self.username_entry.pack()

    def createServerInput(self):
        label_server = Label(self, text="Serveur", font=("Courrier", 25), bg='#41B77F',
                               fg='white')
        label_server.pack()
        self.server_entry = Entry(self, font=("Helvetica", 20), bg='#4065A4', fg='white')
        self.server_entry.pack()
    
    def createPortInput(self):
        label_port = Label(self, text="Port", font=("Courrier", 25), bg='#41B77F',
                               fg='white')
        label_port.pack()
        self.port_entry = Entry(self, font=("Helvetica", 20), bg='#4065A4', fg='white')
        self.port_entry.pack()

    def createValidateButton(self):
        validate_button = Button(self, text="Entrer", font=("Courrier", 25), bg='white', fg='#41B77F', 
            command=lambda: self.sendText({'username': self.username_entry.get(),'server': self.server_entry.get(),'port': int(self.port_entry.get())}))
        validate_button.pack(pady=25)

    #permet d'appeler plusieurs fonction pour un command
    # def combine_funcs(*funcs):
    #     def combined_func(*args, **kwargs):
    #         for f in funcs:
    #             f(*args, **kwargs)
    #     return combined_func

    
    def sendText(self, text):
        self.controller.frames[TchatBoxFrame].setData(text)
        self.controller.frames[TchatBoxFrame].getData(text)
        self.controller.showFrame(TchatBoxFrame)
        


class TchatBoxFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.createWidgets()

    #initialisation de tous les composants
    def createWidgets(self):
        self.chatBox()
        self.textBox()
        self.sendButton()
        self.exitButton()

    def chatBox(self):
        self.chat_box = scrolledtext.ScrolledText(self, state='disabled')
        self.chat_box.configure(font=("Courrier", 16))
        self.chat_box.grid(column=0, row=1, sticky='w', columnspan=4,padx=20) 

    def labelUsers(self,username):
        label_users = Label(self, text=username, font=("Courrier", 10), bg='#41B77F',
                               fg='white')
        label_users.grid(column=4, row=0, padx=(10,10), pady=(20,0))     

    def textBox(self):
        self.text_box = ttk.Entry(self)
        self.text_box.grid(column=0, row=2,sticky="NSEW",pady=10,padx=(20,0))
    
    def sendButton(self):
        btn_send = Button(self, text="Envoyer", font=("Courrier", 10), bg="#4065A4", fg="white", command=lambda: self.sendMsg({
                                                            'msg': self.text_box.get(),
                                                           }))                                                 
        btn_send.grid(column=1,row=2, pady=10)

    def exitButton(self):    
        btn_exit = ttk.Button(self, text="Quitter", command=self.quit)
        btn_exit.grid(column=4,row=2,padx=(0,20))

    #obtenir les informations user
    def getData(self,data):
        username = data['username']
        self.labelUsers(username)

    def setData(self, data):
        self.client = Client(data['username'], data['server'], data['port'])
        self.client.listen(self.handle)

    def sendMsg(self, data):
        self.client.send(data['msg'])

    def handle(self, msg):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(tk.END, msg + '\n')
        self.chat_box.configure(state='disabled')

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()