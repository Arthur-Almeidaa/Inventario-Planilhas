import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from settings import *
from data import *
from PIL import Image


class FooterFrame(ctk.CTkFrame):

    def __init__(self, parent, main_frame):
        super().__init__(master=parent,
                         height=WINDOW_HEIGHT / 5,
                         width=WINDOW_WIDTH)

        self.data = Data('dados.json')
        self.grid(row=4, column=0, sticky='sw')
        self.configure(fg_color=FOOTER_FRAME_COLOR)

        self.logo = ctk.CTkImage(Image.open('images/logo.jpg'), size=(200, 75))
        self.add_icon = ctk.CTkImage(Image.open('images/add.png'), size=(25, 25))

        panel = ctk.CTkLabel(self, image=self.logo, text='')
        panel.place(relx=0.75, rely=0.3)

        self.main_frame = main_frame

        self.create_widgets()

    def create_widgets(self):
        # ----// Entry \\----
        add_spreadsheet_entry = ctk.CTkEntry(self, placeholder_text=r'URL')
        add_spreadsheet_entry.place_configure(x=(WINDOW_WIDTH / 5), y=(WINDOW_HEIGHT / 5) / 2)

        # ----// Label \\----
        add_spreadsheet_label = ctk.CTkLabel(self, text='Adicionar Planilha', height=15, text_color=TEXT_COLOR,
                                             font=ctk.CTkFont('<Helvetica>', size=14))
        add_spreadsheet_label.place_configure(x=(WINDOW_WIDTH / 5) + 4, y=(WINDOW_HEIGHT / 5) / 3 - 5)

        # ----// Buttons \\----
        add_spreadsheet_button = ctk.CTkButton(self, height=25, width=25, text='+', fg_color=MAIN_BUTTON_COLOR,
                                               font=ctk.CTkFont('<Helvetica>', size=14),
                                               command=lambda: self.add_spreadsheet_json(add_spreadsheet_entry))

        add_spreadsheet_button.bind('<Enter>',
                                    lambda event, btn=add_spreadsheet_button: btn.configure(fg_color=HOLD_BUTTON_COLOR))
        add_spreadsheet_button.bind('<Leave>',
                                    lambda event, btn=add_spreadsheet_button: btn.configure(fg_color=MAIN_BUTTON_COLOR))

        add_spreadsheet_button.place_configure(x=(WINDOW_WIDTH / 5) + (WINDOW_WIDTH / 6) + 20,
                                               y=(WINDOW_HEIGHT / 5) / 2)

        filedialog_button = ctk.CTkButton(self, height=4, width=4, image=self.add_icon, fg_color=FOOTER_FRAME_COLOR,
                                          text='',
                                          command=lambda: self.filedialog_button_func())
        filedialog_button.place_configure(x=(WINDOW_WIDTH / 5) + (WINDOW_WIDTH / 6) + 65,
                                          y=(WINDOW_HEIGHT / 5) / 2 - 3)

        filedialog_button.bind('<Enter>',
                               lambda event, btn=filedialog_button: btn.configure(fg_color=MAIN_FRAME_COLOR))
        filedialog_button.bind('<Leave>',
                               lambda event, btn=filedialog_button: btn.configure(fg_color=FOOTER_FRAME_COLOR))
        filedialog_button.bind('<Button-1>',
                               lambda event, btn=filedialog_button: btn.configure(fg_color=FOOTER_FRAME_COLOR))

    def add_spreadsheet_json(self, spreadsheet_entry):
        new_url = spreadsheet_entry.get()

        self.data.add_data(new_url)
        self.main_frame.update_buttons()
        spreadsheet_entry.delete(0, tk.END)

    def filedialog_button_func(self):
        file_path = filedialog.askopenfilename()
        self.data.add_data(file_path)
        self.main_frame.update_buttons()
