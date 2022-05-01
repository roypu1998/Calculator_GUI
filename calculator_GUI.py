from tkinter import *
from tkinter import messagebox
# Log the exception to file
import logging


# App class to create instance of Calculator
class App:
    def __init__(self, tkinter_root):
        self.tkinter_root = tkinter_root
        Calculator(self.tkinter_root, 3, 2)


# Calculator class
class Calculator:

    def __init__(self, parent, x, y):

        logging.basicConfig(filename='app.log', filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info('Logged in')

        # Font properties
        self.button_font = ('arial', 20, 'bold')
        self.entry_font = ('arial', 20, 'bold')
        self.parent = parent

        self.button_width = 4
        self.button_height = 1

        # The Frame building
        self.container = Frame(self.parent)
        self.container.grid(row=x, column=y)

        # Thinker's StringVar value
        self.string_var = StringVar()

        self.text_input = ''

        # Whether '=' button has been pressed
        self.calculated = False

        # Whether {'+','-','*','/','(',')'} button has been pressed
        self.operators_flag = False

        # Place the entry
        self.entry()

        # Create the operators buttons and place them
        # ('+','-','*','/','(',')','clear','.','del','=')
        self.initialize_buttons()

    def initialize_buttons(self):
        self.initialize_digits_buttons()

        # Initialize operators
        self.create_button('+', 1, 3, lambda: self.button_action_click('+'))
        self.create_button('-', 1, 4, lambda: self.button_action_click('-'))
        self.create_button('*', 2, 3, lambda: self.button_action_click('*'))
        self.create_button('/', 2, 4, lambda: self.button_action_click('/'))

        self.create_button('(', 3, 3, lambda: self.button_action_click('('))
        self.create_button(')', 3, 4, lambda: self.button_action_click(')'))

        self.create_button('=', 4, 1, lambda: self.button_equals_input(), 2)
        self.create_button('.', 4, 2, lambda: self.button_action_click('.'), 2)
        self.create_button(' del  ', 4, 3, lambda: self.button_delete_display())
        self.create_button('clear', 4, 4, lambda: self.button_clear_display())

    def initialize_digits_buttons(self):
        buttons = [str(num) for num in range(0, 10)]
        number_of_digits = 9

        for i in range(1, 5):
            for j in range(2, -1, -1):
                if i == 4 and (j == 1 or j == 2):
                    continue
                else:
                    self.digit_button(buttons[number_of_digits], i, j)
                    number_of_digits -= 1

    # Entry creation function
    def entry(self):
        text_display = Entry(self.container, font=self.entry_font, textvariable=self.string_var, bd=15, insertwidth=2,
                             bg="powder blue", justify='right', state=DISABLED)
        text_display.grid(columnspan=5)

    def digit_button(self, digit, x, y):
        Button(self.container, padx=16, pady=16, bd=5, fg="black", font=self.button_font,
               text=digit, bg="powder blue", command=lambda: self.button_click(int(digit))).grid(row=x, column=y)

    def create_button(self, button_text, x, y, action, button_width=5):
        Button(self.container, padx=16, pady=16, bd=5, fg="black", font=self.button_font,
               text=button_text, width=button_width, bg="powder blue", command=action).grid(row=x, column=y)

    # Action function to set numbers from numbers buttons on entry
    def button_click(self, numbers):
        # check flag to display output on entry like : '+{digit}' or '-{digit}'
        if self.calculated and not self.operators_flag:
            self.calculated = False
            self.button_clear_display()
        self.text_input = self.text_input + str(numbers)
        self.string_var.set(self.text_input)

    # Action function to set operators from operators buttons on entry
    def button_action_click(self, action):
        self.operators_flag = True
        self.text_input = self.text_input + str(action)
        self.string_var.set(self.text_input)

    # Action function to clear the entry
    def button_clear_display(self):
        self.text_input = ""
        self.string_var.set("")

    # Action function to delete one char from text on the entry
    def button_delete_display(self):
        if not self.calculated or self.operators_flag:
            try:
                self.text_input = self.text_input[:-1]
                self.string_var.set(self.text_input)
            except:
                self.text_input = ""
                logging.exception(f"Exception occurred", exc_info=True)

    # Action function to calculate the math exercise
    def button_equals_input(self):
        try:
            self.calculated = True
            calc = str(eval(self.text_input))
            logging.info(f'{self.text_input} = {calc}')
            self.string_var.set(calc)
            self.text_input = ""


        # if the string for example is : '3*5+4*4+' or '6+5(1+2)' it's give 'Syntax Error' on entry
        except:
            self.string_var.set("Syntax Error")
            self.text_input = ""
            logging.exception(f"Exception occurred", exc_info=True)



def main():
    # Initializing Tkinter
    tkinter_root = Tk()

    # Create the instance of the application class
    app = App(tkinter_root)

    # Set name of window 'Calculator'
    tkinter_root.title('Calculator')

    # When window get closed
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            tkinter_root.destroy()
            logging.basicConfig(filename='app.log', filemode='w',format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
            logging.warning('Logged out')

    tkinter_root.protocol("WM_DELETE_WINDOW", on_closing)

    # The mainloop receives events from the window system and dispatches them to the application
    tkinter_root.mainloop()



if __name__ == '__main__':
    main()
