import os
import tkinter
import tkinter.messagebox
from tkinter import filedialog
import customtkinter
from datetime import datetime
from PIL import Image, ImageTk

import utils.db_update as db_update
import page_gen

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.file_path = None

        # configure window
        self.title("Museum")
        self.geometry(f"{900}x{500}")
        customtkinter.set_widget_scaling(1)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(resource_path("logo_mus.png")), size=(70, 70))
        self.logo_image_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.logo_image_label.grid(row=0, column=0, padx=20, pady=(50, 0))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text='Музей \n"Наша Перловка"',
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        # self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)

        self.text_box = customtkinter.CTkTextbox(master=self, activate_scrollbars=False)
        self.text_box.grid(row=1, column=2, padx=(0, 20), pady=(20, 0), sticky="nsew")
        self.text_box.insert("0.0", "КРАТКАЯ ИНСТРУКЦИЯ:"
                                    "\n1. Загрузите .xlsx файл. "
                                    "\n2. Если первое не помогло, "
                                    "\n    то закройте программу")

        self.open_button = customtkinter.CTkButton(self, text="Файл", command=self.open_file_dialog)
        self.open_button.grid(row=2, column=2, padx=(0, 20), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self,
                                                     fg_color="transparent",
                                                     border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Старт",
                                                     command=self.start_button_event)
        self.main_button_1.grid(row=3, column=2, padx=(0, 20), pady=(20, 20), sticky="nsew")

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def start_button_event(self):
        if self.file_path is None:
            print('Ничего не выбрано')
            self.open_toplevel()
        else:
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.xlsx':
                ...
                # db_update.new_data(filepath=self.file_path).new_data_()  # скрипт для апдейта бд
                # page_gen.Generate.pages()
                # конец
            else:
                print("неверный формат файла")
            print(self.file_path)

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename()
        # Здесь можно обработать выбранный файл
        if self.file_path:
            print("Выбранный файл:", self.file_path)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    app = App()
    app.mainloop()
