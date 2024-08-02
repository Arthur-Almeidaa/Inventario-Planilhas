import tkinter
import customtkinter as ctk
from settings import *
from data import Data
from PIL import Image
from tkinter import messagebox
import webbrowser
import pyautogui
import win32api
import win32con


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent,
                         width=WINDOW_WIDTH,
                         height=WINDOW_HEIGHT - 75,
                         fg_color=MAIN_FRAME_COLOR)

        self.selected_buttons = set()
        self.place(relx=0, rely=0)
        self.button_text = ctk.StringVar()

        # ----// Images \\----
        self.images = {
            "word": ctk.CTkImage(Image.open(IMAGE_WORD), size=IMAGE_SIZE),
            "excel": ctk.CTkImage(Image.open(IMAGE_EXCEL), size=IMAGE_SIZE),
            "button": ctk.CTkImage(Image.open(IMAGE_BUTTON), size=IMAGE_SIZE)
        }

        self.create_buttons()

    def create_buttons(self):
        self.data = Data('dados.json')
        i = 0

        for link, url in self.data.data.items():
            self.button_text.set(link)

            idx_url = url.rfind('.')

            # ----// Botões Planilha \\----
            self.button = ctk.CTkButton(self, text=self.button_text.get(),
                                        width=BUTTON_WIDTH,
                                        height=BUTTON_HEIGHT,
                                        fg_color=MAIN_FRAME_COLOR,
                                        text_color=MAIN_FRAME_COLOR,
                                        font=ctk.CTkFont(size=1),
                                        image=self.set_image(url, idx_url)
                                        )

            self.button.grid(row=i // 6, column=i % 6, padx=20, pady=29)

            self.name_label = ctk.CTkLabel(self, text=self.button_text.get(), fg_color=MAIN_FRAME_COLOR,
                                           font=ctk.CTkFont(size=12))
            self.name_label.grid(row=i // 6, column=i % 6, sticky='n', pady=((BUTTON_WIDTH // 15) / 5),
                                 padx=BUTTON_HEIGHT / 4)

            # Bindings
            self.button.bind('<Button-1>', lambda event, btn=self.button: self.on_click(event, btn))
            self.button.bind('<Double-Button-1>', lambda event, url_b=url: webbrowser.open(url_b))
            i += 1

    def on_click(self, event, button):
        ctrl_pressed = event.state & 0x0004
        self.update_button_state(button, ctrl_pressed)
        self.after(10, lambda: self.verify())

    def update_button_state(self, button, ctrl_pressed):
        if ctrl_pressed:
            self.handle_ctrl_click(button)
        else:
            self.handle_normal_click(button)

    def handle_ctrl_click(self, button):
        if button not in self.selected_buttons:
            self.select_button(button)
        else:
            self.deselect_buttons()

    def handle_normal_click(self, button):
        if button not in self.selected_buttons:
            self.deselect_buttons()
            self.select_button(button)
        else:
            self.deselect_buttons()
            if self.current_button == button:
                self.current_button = None

    def select_button(self, button):
        button.configure(fg_color=SELECT_BUTTON_COLOR)
        self.selected_buttons.add(button)
        self.current_button = button

    def verify(self):
        if self.current_button is not None:
            if win32api.GetAsyncKeyState(win32con.VK_RBUTTON) & 0x8000:
                self.right_click(self.current_button)

            if win32api.GetAsyncKeyState(win32con.VK_DELETE) & 0x8000:
                self.remove_button_func(self.data)

            self.after(100, self.verify)

    def deselect_button(self, button):
        button.configure(fg_color=MAIN_FRAME_COLOR)
        self.selected_buttons.remove(button)

    def deselect_buttons(self):
        for button in list(self.selected_buttons):
            self.deselect_button(button)

    def right_click(self, current_button):
        menu = tkinter.Menu(self, tearoff=False)
        menu.add_command(label="Renomear",
                         command=lambda: self.rename_button_func(current_button.cget('text'), self.data,
                                                                 current_button))
        menu.add_command(label='Remover',
                         command=lambda: self.remove_button_func(self.data))
        x, y = pyautogui.position()
        menu.post(x, y)

    def set_image(self, url, idx):
        ext = url.split('.')[-1].lower()
        if ext == 'xlsx':
            return self.images['excel']
        elif ext in ['doc', 'docx']:
            return self.images['word']
        else:
            return self.images['button']

    def remove_button_func(self, data):
        if len(self.selected_buttons) > 0:
            for button in self.selected_buttons:
                button_text = button.cget('text')
                data.remove_data(button_text)
                self.update_buttons()

            self.current_button = None
            self.selected_buttons.clear()

    def update_buttons(self):
        for widget in self.grid_slaves():
            widget.destroy()
        self.create_buttons()

    def rename_button_func(self, button_text, data, button):
        self.selected_buttons.discard(button)
        self.current_button = None

        entry_stringvar = ctk.StringVar()
        entry = ctk.CTkEntry(self, width=90, textvariable=entry_stringvar, bg_color=MAIN_BUTTON_COLOR)

        for idx, (link, url) in enumerate(data.data.items(), start=1):
            if button_text in link:
                row = (idx - 1) // 5
                col = (idx - 1) % 5
                entry.grid(row=row, column=col)
                break

        def set_name(event):
            new_name = entry.get()
            idx_space = new_name.rfind(' ', 0)
            if len(new_name) >= 21 and idx_space < 0:
                messagebox.showinfo(title='Aviso', message='Nome muito grande')

            elif len(new_name) >= 21 and idx_space > 0:
                new_name = new_name.replace(' ', '\n')

            if new_name and new_name != button_text:
                data.rename_data(old_key=button_text, new_key=new_name)
                self.update_buttons()

        entry.bind('<Return>', lambda event: set_name(event))
        entry.focus_set()
