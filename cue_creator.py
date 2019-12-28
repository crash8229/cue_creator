import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os


class CueCreator:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Cue Creator')

        self.mode = tk.StringVar()
        self.mode.set('1')

        radio_frame = tk.Frame(self.root).grid(row=0)
        tk.Radiobutton(radio_frame, text='Mode 1 (PC)', variable=self.mode, value='1').grid(row=0, column=1, sticky='e')
        tk.Radiobutton(radio_frame, text='Mode 2 (PSX)', variable=self.mode, value='2').grid(row=0, column=3, stick='w')

        file_frame = tk.Frame(self.root).grid(row=2)
        tk.Label(file_frame, text='File(s):').grid(row=2, column=0, sticky='e')
        self.filename = tk.Text(file_frame, height=10, width=100)
        self.filename.grid(row=2, column=1, columnspan=3, sticky='nsew')
        tk.Button(file_frame, text='...', command=self.dialog, width=5, height=1).grid(row=2, column=4, sticky='ew')
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=4)
        self.root.grid_columnconfigure(3, weight=4)
        self.root.grid_columnconfigure(4, weight=1)

        button_frame = tk.Frame(self.root).grid(row=2)
        tk.Button(button_frame, text='Create CUE file', command=self.create_cue).grid(column=2)

        self.root.after(1, self.size)
        self.root.mainloop()

    def size(self):
        if self.root.winfo_screenheight() > self.root.winfo_height()\
                and self.root.winfo_screenwidth() > self.root.winfo_width():
            self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

    def dialog(self):
        files = filedialog.askopenfilenames(title="Select file",
                                            filetypes=(("bin files", "*.bin"), ("all files", "*.*")))
        filenames = str()
        if isinstance(files, tuple):
            self.filename.delete(1.0, tk.END)
            for file in reversed(files):
                file = file.strip()
                if file is not str():
                    filenames = ''.join([filenames, file, '\n'])
            self.filename.insert(1.0, filenames)

    def create_cue(self):
        files = self.filename.get(1.0, tk.END)
        files = files.strip()
        files = files.split('\n')
        for file in files:
            path, name = os.path.split(file)
            cuename = ''.join([name.split('.')[0], '.cue'])
            cuefile = os.path.join(path, cuename)
            if os.path.isfile(cuefile):
                message = ''.join(['The file \"', cuename, '\" already exists. Do you want to override it?'])
                if not messagebox.askyesno(title='File exists!', message=message):
                    continue
            cuefile = open(cuefile, 'w')
            text = ''.join(['FILE \"', name, '\" BINARY\nTRACK 01 MODE', self.mode.get(), '/2352\nINDEX 01 00:00:00\n'])
            cuefile.write(text)
            cuefile.close()
        messagebox.showinfo(title='Status', message='Done!')



CueCreator()
