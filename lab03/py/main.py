from tkinter.constants import W
from pathlib import Path
from lib import code_meaning, do_work
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as msgbox


_key: str = ""
_input: str = ""


def set_key(label: tk.Label) -> None:
    global _key
    _key = tkf.askopenfilename()
    label.config(text=f'Key file: {_key}')


def set_input(label: tk.Label) -> None:
    global _input
    _input = tkf.askopenfilename()
    label.config(text=f'Input file: {_input}')


def try_start(option: tk.StringVar) -> None:
    if _key == "":
        msgbox.showerror(
            title="Error!",
            message = "Please specify key.",
        )
        return
    if _input == "":
        msgbox.showerror(
            title="Error!",
            message="Please specify input file.",
        )
        return
    
    output: str = tkf.asksaveasfilename(
        confirmoverwrite=True,
        defaultextension=".gost",
    )
    op = option.get().lower()

    print(output)

    result = do_work(
        path=f"{Path(__file__).parent.absolute()}\\lib\\GOST.exe",
        op=op,
        key=_key,
        input=_input,
        output=output,
    )

    if result != 0:
        msgbox.showerror(
            title=f"Error during {op}ion",
            message=f"Failed to {option.get().lower()} file: {code_meaning(result)}",
        )
    else:
        msgbox.showinfo(
            title="Success!",
            message=f"Operation completed successfully!",
        )


def setup_gui() -> tk.Tk:
    window = tk.Tk(
        className=" Valder's Encryptor&Decryptor",
    )
    window.rowconfigure([0,1,2], weight=1)
    window.columnconfigure([0], weight=1)

    frmInstructions = tk.Frame(
        master=window,
        height=50,
    )
    frmInstructions.grid(row=0, column=0, sticky='news')

    instructions = tk.Label(
        master=frmInstructions,
        text='Welcome! Please choose operation, key file, input file and output files.'
    )
    instructions.pack()

    keyLabel = tk.Label(
        master=frmInstructions,
        text='Key file: -',
    )
    keyLabel.pack()

    inputLabel = tk.Label(
        master=frmInstructions,
        text='Input file: -',
    )
    inputLabel.pack()

    frmSettings = tk.Frame(
        master=window,
        height=150,
    )
    frmSettings.rowconfigure([0], weight=1)
    frmSettings.columnconfigure([0, 1, 2], weight=1)
    frmSettings.grid(row=1, column=0, sticky='news')

    buttonKey = tk.Button(
        master=frmSettings,
        text="Open Key File",
        command=lambda: set_key(keyLabel),
    )
    buttonKey.grid(row=0, column=0, sticky='news')

    buttonInput = tk.Button(
        master=frmSettings,
        text="Open Input File",
        command=lambda: set_input(inputLabel),
    )
    buttonInput.grid(row=0, column=1, sticky='news')

    var = tk.StringVar(frmSettings)
    var.set('Encrypt')
    options = {'Encrypt', 'Decrypt'}
    dropDown = tk.OptionMenu(
        frmSettings,
        var,
        *options,
    )
    dropDown.grid(row=0, column=2, sticky='news')

    frmFooter = tk.Frame(
        master=window,
        height=30,
    )
    frmFooter.grid(row=2, column=0, sticky='news')

    button = tk.Button(
        master=frmFooter,
        text='Start',
        command=lambda: try_start(var),
    )
    button.pack(fill=tk.Y)

    return window


if __name__ == "__main__":
    window = setup_gui()
    window.mainloop()
