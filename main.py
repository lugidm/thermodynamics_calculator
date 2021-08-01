import tkinter as tk
from tkinter import ttk
from operator import pow, truediv, mul, add, sub

operators = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '^': pow
}


list_of_variables = ["T[K]", "p[bar]", "V[m^3]"]
list_of_transitions = ["isobar", "isotherm", "isochor", "adiabat"]
list_of_constants = ["Molar Mass [g/mol]", "n [mol]", "Mass [g]", u'R\u209B', u'R\u2098', u'\u03BA', u'c\u209A',
                     u'c\u1D65']
dictionary_of_constants = dict()


def interpret_as_num(plain: str):
    if plain.isdigit():
        return float(plain)
    for c in operators.keys():
        left, operator, right = plain.partition(c)
        if operator in operators:
            return operators[operator](interpret_as_num(left), interpret_as_num(right))



def inputListForOneState(frame: tk.Frame, state: int):
    entries = []
    color = '#%02x%02x%02x' % (138 * state % 255, 44502 * state % 256, 98202 * state % 256)
    title = tk.Label(frame, text="State " + str(state))
    frame.config(bg=color)
    title.grid(row=0, sticky=tk.NSEW, pady=5)
    entries_frame = tk.Frame(frame, bg=color)
    for v in range(len(list_of_variables)):
        l = tk.Label(entries_frame, text=list_of_variables[v])
        e = tk.Entry(entries_frame, text="----")
        l.grid(row=v, column=0)
        e.grid(row=v, column=1)
        entries.append(e)
    entries_frame.grid(row=1, sticky=tk.NSEW, pady=5)
    return entries


def createTransitionChooser(frame: tk.Frame, variable: tk.IntVar):
    for t in range(len(list_of_transitions)):
        r = tk.Radiobutton(frame, text=list_of_transitions[t], variable=variable, value=t)
        r.pack()


def calculateConstants(event=None):
    """Mass - specific constants"""
    if dictionary_of_constants[list_of_constants[2]].get() != "":
        mu = interpret_as_num(dictionary_of_constants[list_of_constants[2]].get().replace(',', '.'))
        if dictionary_of_constants[list_of_constants[0]].get() != "":
            m = interpret_as_num(dictionary_of_constants[list_of_constants[0]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[1]].set(str(mu/m))
        elif dictionary_of_constants[list_of_constants[1]].get() != "":
            n = interpret_as_num(dictionary_of_constants[list_of_constants[1]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[0]].set(str(mu / n))
    elif dictionary_of_constants[list_of_constants[1]].get() != "":
        n = interpret_as_num(dictionary_of_constants[list_of_constants[1]].get().replace(',', '.'))
        if dictionary_of_constants[list_of_constants[0]].get() != "":
            m = interpret_as_num(dictionary_of_constants[list_of_constants[0]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[2]].set(str(n * m))
    """Boltzmann (R) specific constant """
    if dictionary_of_constants[list_of_constants[0]].get() != "":
        m = interpret_as_num(dictionary_of_constants[list_of_constants[0]].get().replace(',', '.'))
        if dictionary_of_constants[list_of_constants[3]].get() != "":
            r_s = interpret_as_num(dictionary_of_constants[list_of_constants[3]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[4]].set(str(r_s * m))
        elif dictionary_of_constants[list_of_constants[4]].get() != "":
            r_m = interpret_as_num(dictionary_of_constants[list_of_constants[4]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[3]].set(str(r_m / m))
    elif dictionary_of_constants[list_of_constants[3]].get() != "":
        r_s = interpret_as_num(dictionary_of_constants[list_of_constants[3]].get().replace(',', '.'))
        if dictionary_of_constants[list_of_constants[4]].get() != "":
            r_m = interpret_as_num(dictionary_of_constants[list_of_constants[4]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[0]].set(str(r_m / r_s))
    """Thermal capacity specific constants"""
    """R_s = c_p - c_v"""
    if dictionary_of_constants[list_of_constants[3]].get() != "":
        r_s = interpret_as_num(dictionary_of_constants[list_of_constants[3]].get().replace(',', '.'))
        if dictionary_of_constants[list_of_constants[6]].get() != "":
            c_p = interpret_as_num(dictionary_of_constants[list_of_constants[6]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[7]].set(str(c_p * r_s))
        elif dictionary_of_constants[list_of_constants[7]].get() != "":
            c_v = interpret_as_num(dictionary_of_constants[list_of_constants[7]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[6]].set(str(r_s + c_v))
    elif dictionary_of_constants[list_of_constants[6]].get() != "" and \
            dictionary_of_constants[list_of_constants[7]].get() != "":
        c_p = interpret_as_num(dictionary_of_constants[list_of_constants[6]].get().replace(',', '.'))
        c_v = interpret_as_num(dictionary_of_constants[list_of_constants[7]].get().replace(',', '.'))
        dictionary_of_constants[list_of_constants[3]].set(str(c_p - c_v))
        dictionary_of_constants[list_of_constants[5]].set(str(c_p / c_v))
    """k = c_p / c_v"""
    if dictionary_of_constants[list_of_constants[5]].get() != "":
        k = interpret_as_num(dictionary_of_constants[list_of_constants[5]].get().replace(',', '.'))
        if dictionary_of_constants[list_of_constants[6]].get() != "":
            c_p = interpret_as_num(dictionary_of_constants[list_of_constants[6]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[7]].set(str(c_p / k))
        elif dictionary_of_constants[list_of_constants[7]].get() != "":
            c_v = interpret_as_num(dictionary_of_constants[list_of_constants[7]].get().replace(',', '.'))
            dictionary_of_constants[list_of_constants[6]].set(str(k * c_v))


def createConstantsTab(frame: tk.Frame):
    fr_inputs = tk.Frame(frame)
    fr_mol = tk.LabelFrame(fr_inputs, text="Masses", bg='#fcba03')
    for i in range(3):
        tk.Label(fr_mol, text=list_of_constants[i]).grid(row=i, column=0)
        entry = tk.Entry(fr_mol, textvariable=dictionary_of_constants[list_of_constants[i]])
        entry.grid(row=i, column=1)
        entry.bind('<Return>', calculateConstants, add='-')
    fr_mol.grid(row=0, column=0, padx=4, pady=4)
    fr_r = tk.LabelFrame(fr_inputs, text="Gas Constants", bg='#32a852')
    for i in range(3, 5):
        tk.Label(fr_r, text=list_of_constants[i]).grid(row=i-2, column=0)
        entry = tk.Entry(fr_r, textvariable=dictionary_of_constants[list_of_constants[i]])
        entry.grid(row=i-2, column=1)
        entry.bind('<Return>', calculateConstants, add='-')
    fr_r.grid(row=0, column=1, padx=4, pady=4)
    fr_c = tk.LabelFrame(fr_inputs, text="Thermal Capacity", bg='#eb856e')
    for i in range(5, 8):
        tk.Label(fr_c, text=list_of_constants[i]).grid(row=i - 5, column=0)
        entry = tk.Entry(fr_c, textvariable=dictionary_of_constants[list_of_constants[i]])
        entry.grid(row=i - 5, column=1)
        entry.bind('<Return>', calculateConstants, add='-')
    fr_c.grid(row=0, column=2, padx=4, pady=4)
    fr_inputs.pack()

    bt_calc = tk.Button(frame, text='calculate', command=calculateConstants)
    bt_calc.pack()
    frame.focus_set()


def main():
    master = tk.Tk()
    master.title("Monas Calculator")

    for key in list_of_constants:
        dictionary_of_constants[key] = tk.StringVar()

    tab_control = ttk.Notebook(master)
    tab1 = tk.Frame(tab_control)
    createConstantsTab(tab1)
    tab2 = tk.Frame(tab_control)

    frame_1 = tk.Frame(master=tab2)
    labels_1 = inputListForOneState(frame_1, 1)
    frame_transition_1_2 = tk.Frame(master=tab2)
    transition_var_1_2 = tk.IntVar()
    createTransitionChooser(frame_transition_1_2, transition_var_1_2)
    frame_2 = tk.Frame(master=tab2)
    labels_2 = inputListForOneState(frame_2, 2)

    frame_2.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)
    frame_transition_1_2.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)
    frame_1.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

    tab_control.add(tab1, text='Constants')
    tab_control.add(tab2, text='Transitions')
    tab_control.grid(row=0, column=0, sticky=tk.NSEW)
    tk.Button(master, text='Quit', command=master.quit).grid(row=1, column=0, sticky=tk.S, pady=4)

    tk.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
