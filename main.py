import customtkinter as ctk
from settings import *
from footer import FooterFrame
from main_frame import MainFrame


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Planilhas Exceed")
        self.geometry(f'{str(WINDOW_WIDTH)}x{str(WINDOW_HEIGHT)}')
        self.configure(fg_color=MAIN_FRAME_COLOR)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.resizable(width=False, height=False)

        self.iconbitmap('images/icone.ico')

        main_frame = MainFrame(self)

        FooterFrame(self, main_frame)


if __name__ == "__main__":
    app = App()
    app.mainloop()
