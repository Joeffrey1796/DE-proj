import tkinter as tk
import sympy as sp
import re
from tkinter import messagebox

# ========================= CORE FUNCTIONS ===========================

def check_homogeneity(M, N, x, y):
    """ Check if the differential equation is homogeneous and determine the degree. """
    t = sp.symbols('t')
    
    # Substitute x and y with t*x and t*y
    M_t = M.subs({x: t * x, y: t * y})
    N_t = N.subs({x: t * x, y: t * y})
    
    # Simplify the expressions
    M_t_simplified = sp.simplify(M_t)
    N_t_simplified = sp.simplify(N_t)
    
    print("Simplified M_t:", M_t_simplified)
    print("Simplified N_t:", N_t_simplified)

    # Check scaling behavior using log to identify the degree of t
    degree_M = sp.simplify(sp.log(M_t_simplified) / sp.log(t)).simplify()
    degree_N = sp.simplify(sp.log(N_t_simplified) / sp.log(t)).simplify()

    print(f"Degree of M_t: {degree_M}")
    print(f"Degree of N_t: {degree_N}")

    # Check if the degrees match
    if degree_M == degree_N:
        return f"HOMOGENEOUS, DEGREE: {degree_M}"
    return "NOT HOMOGENEOUS"



def check_exactness(M, N, x, y):
    """ Check if the differential equation is exact by comparing partial derivatives. """
    # Compute the partial derivatives
    M_y = sp.diff(M, y)
    N_x = sp.diff(N, x)
    
    # Print the partial derivatives for debugging
    print("Partial derivative of M with respect to y:", M_y)
    print("Partial derivative of N with respect to x:", N_x)
    
    # Simplify the difference between the two partial derivatives
    difference = sp.simplify(M_y - N_x)
    
    # Print the simplified difference for debugging
    print("Simplified difference (M_y - N_x):", difference)
    
    # Return the result based on the comparison
    return "EXACT" if difference == 0 else "NOT EXACT"


def preprocess_input(expr):
    """ Process input for implicit multiplication, exponentiation, and functions. """
    # Replace ^ with ** for exponentiation
    expr = expr.replace('^', '**')

    # Add * between numbers and variables, variables and functions, etc.
    expr = re.sub(r'([0-9])([xy])', r'\1*\2', expr)  # Add * between number and variable
    expr = re.sub(r'([xy])([0-9])', r'\1*\2', expr)  # Add * between variable and number
    expr = re.sub(r'([xy])([xy])', r'\1*\2', expr)  # Add * between two variables
    expr = re.sub(r'([xy])([a-zA-Z])', r'\1*\2', expr)  # Add * between variables and functions (general case)
    
    expr = re.sub(r'(\b[a-zA-Z]+\([^\)]*\))(\b[a-zA-Z]+\()', r'\1*\2', expr)

    # Add * between numbers and parentheses if needed
    expr = re.sub(r'([0-9])\(', r'\1*(', expr)  # Add * between number and parenthesis
    expr = re.sub(r'([xy])\(', r'\1*(', expr)   # Add * between variable and parenthesis
    
    print(expr)

    return expr




def parse_input(equation_input):
    """ Parse user input into M(x, y) and N(x, y). """
    equation_input = equation_input.replace(" ", "")  # Remove spaces
    
    # Remove '= 0' if it exists at the end of the equation
    equation_input = re.sub(r'\s*=\s*0$', '', equation_input)

    match = re.match(r'^(.*)dx\+?(.*)dy$', equation_input)
    if match:
        return match.group(1), match.group(2)
    raise ValueError("INVALID INPUT. Use the format: M(x,y)dx + N(x,y)dy")


def analyze_equation(equation_input):
    """ Analyze the input equation for homogeneity and exactness. """
    x, y = sp.symbols('x y')  # Define symbols for x and y
    try:
        print("Valid 1: Parsing the equation")
        M_input, N_input = parse_input(equation_input)  # Parse input into M and N
        print("Valid 2: Parsed successfully")
        
        # Debugging parsed inputs
        print("Parsed M_input:", M_input)
        print("Parsed N_input:", N_input)
        
        # Preprocess the inputs for implicit multiplication and exponentiation
        M_input = preprocess_input(M_input)
        N_input = preprocess_input(N_input)
        print("Valid 3: Preprocessing complete")
        
        # Debugging preprocessed inputs
        print("Preprocessed M_input:", M_input)
        print("Preprocessed N_input:", N_input)
        
        # Attempt to sympify the expressions
        try:
            M = sp.sympify(M_input)
            N = sp.sympify(N_input)
            print("Valid 4: Sympification successful")
        except Exception as e:
            print(f"Error during sympify: {e}")
            raise ValueError(f"Invalid input detected after preprocessing: {e}")
        
        # Debugging sympified expressions
        print("Sympified M:", M)
        print("Sympified N:", N)
        
        # Check for homogeneity and exactness
        exactness = check_exactness(M, N, x, y)
        print("\n" * 2)  # Debugging separator
        homogeneity = check_homogeneity(M, N, x, y)
        return f"{homogeneity} | {exactness}"

    except Exception as e:
        print("Error:", e)
        return str(e)



# ========================= GUI DESIGN ===========================

def create_main_window():
    """ Initialize the main window of the application. """
    window = tk.Tk()
    window.title("Differential Equation Analyzer")
    window.geometry("700x500")
    window.configure(bg="#2c3e50")  # Dark Blue Background
    return window

def show_error(message):
    """ Show an error message using a popup. """
    messagebox.showerror("Error", message)

def show_result(message):
    """ Display results in a message popup. """
    messagebox.showinfo("Result", message)

def on_submit(entry_field):
    """ Handle the Submit button click event. """
    equation_input = entry_field.get()
    if not equation_input:
        show_error("Please enter an equation in the form: M(x,y)dx + N(x,y)dy")
        return
    result = analyze_equation(equation_input)
    show_result(result)

def setup_gui(window):
    """ Set up the GUI components for the main application. """
    title_label = tk.Label(
        window, text="DIFFERENTIAL EQUATION ANALYZER", bg="#2c3e50", fg="#ecf0f1",
        font=("Helvetica", 24, "bold"), pady=20
    )
    title_label.pack()

    description_label = tk.Label(
        window, text="Enter your equation in the format: M(x,y)dx + N(x,y)dy",
        bg="#2c3e50", fg="#bdc3c7", font=("Helvetica", 14)
    )
    description_label.pack(pady=10)

    entry_field = tk.Entry(window, font=("Courier", 18), width=40, bg="#ecf0f1", fg="#2c3e50")
    entry_field.pack(pady=20)

    button_frame = tk.Frame(window, bg="#2c3e50")
    button_frame.pack(pady=20)

    submit_button = tk.Button(
        button_frame, text="CHECK", font=("Helvetica", 14, "bold"), bg="#27ae60", fg="white",
        activebackground="#2ecc71", width=12, height=2,
        command=lambda: on_submit(entry_field)
    )
    submit_button.grid(row=0, column=0, padx=10)

    clear_button = tk.Button(
        button_frame, text="CLEAR", font=("Helvetica", 14, "bold"), bg="#e74c3c", fg="white",
        activebackground="#c0392b", width=12, height=2,
        command=lambda: entry_field.delete(0, tk.END)
    )
    clear_button.grid(row=0, column=1, padx=10)

    exit_button = tk.Button(
        button_frame, text="EXIT", font=("Helvetica", 14, "bold"), bg="#3498db", fg="white",
        activebackground="#2980b9", width=12, height=2,
        command=window.quit
    )
    exit_button.grid(row=0, column=2, padx=10)

    return entry_field

# ========================= MAIN APPLICATION ===========================

def main():
    """ Main application loop. """
    window = create_main_window()
    setup_gui(window)
    window.mainloop()

if __name__ == "__main__":
    main()