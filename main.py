import os
import codecs
import chardet
import Tkinter as tk
from tkFileDialog import askopenfilenames


class Encoder(object):
    def __init__(self):
        self.__filenames = None
        self.__block_size = 4096

    def set_filenames(self, filenames):
        self.__filenames = filenames

    def encode(self):
        for filename in self.__filenames:
            __file = codecs.open(filename, 'r', self.__predict_encoding(filename))
            __tmp_filename = "__tmp__"
            __tmp_file = codecs.open(__tmp_filename, "w", "utf-8")

            while True:
                contents = __file.read(self.__block_size)
                if not contents:
                    break
                __tmp_file.write(contents)

            self.__close_files([__file, __tmp_file])
            __file = open(filename, "w")
            __tmp_file = open(__tmp_filename, "r")
            __file.write(__tmp_file.read())
            self.__close_files([__file, __tmp_file])
            os.remove(__tmp_filename)

    def __close_files(self, files):
        for file in files:
            file.close()

    def __predict_encoding(self, filename):
        with open(filename, 'rb') as f:
            rawdata = b''.join(f.read())
        return chardet.detect(rawdata)['encoding']


class Application(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.__master = master
        self.__screen_width = master.winfo_screenwidth()
        self.__screen_height = master.winfo_screenheight()
        self.__encoder = Encoder()
        self.pack()
        self.__setup_ui()

    def __setup_ui(self):
        self.__master.geometry("{}x{}+{}+{}".format(self.__screen_width / 2, self.__screen_height / 2,
                                                    self.__screen_width / 4, self.__screen_height / 4))
        self.__master.resizable(0, 0)
        self.__master.title("Subtitle Encoder")
        self.__quit_button = tk.Button(text="Quit", font=("Arial", 20), command=self.quit)
        self.__quit_button.place(relx=0.85, rely=0.85)
        self.__choose_file_button = tk.Button(text="Open", font=("Arial", 20), command=self.__open_file_dialog)
        self.__choose_file_button.place(relx=0.45, rely=0.85)
        self.__convert_button = tk.Button(text="Convert", font=("Arial", 20),
                                          command=self.__encoder.encode,state=tk.DISABLED)
        self.__convert_button.place(relx=0.03, rely=0.85)
        message = "Press Open to choose single or multiple files to convert to utf-8"
        self.__message = tk.Label(text=message, font=("Arial", 14))
        self.__message.place(relx=0.3, rely=0.5, x=-len(message) * 2, y=-50)

    def __open_file_dialog(self):
        self.__filenames = askopenfilenames(initialdir=".", title="Select Subtitle Files",
                                            filetypes=(("str files", "*.srt"), ("all files", "*.*")))
        self.__encoder.set_filenames(filenames=self.__filenames)
        if len(self.__filenames) > 0:
            self.__convert_button["state"] = tk.NORMAL


def main():
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
    root.destroy()


if __name__ == '__main__':
    main()
