import re  # Import the regular expressions module
import tkinter as tk
from tkinter import messagebox
import sympy as sp

def check_homogeneity(M, N):
    x, y, λ = sp.symbols('x y λ', real=True)

    def is_homogeneous(func):
        if func == 0:
            return None
        func_scaled = func.subs({x: λ * x, y: λ * y}).simplify()
        degree_terms = sp.Poly(func_scaled, λ).monoms()
        degrees = {sum(m) for m in degree_terms}
        return degrees.pop() if len(degrees) == 1 else None

    M_degree = is_homogeneous(M)
    N_degree = is_homogeneous(N)

    if M_degree is not None and N_degree is not None and M_degree == N_degree:
        return True, M_degree
    return False, None



import sympy as sp

def check_exactness(M, N):
    x, y = sp.symbols('x y', real=True)  # Ensure they are treated as variables, not functions
    print("\n" * 3)
    print("exact debuggin: ")

    # Safeguard to ensure M and N are symbolic expressions
    M = sp.sympify(M)
    N = sp.sympify(N)

    print(f"Type of M: {type(M)}, Type of N: {type(N)}")
    print(f"M: {M}, N: {N}")

    x, y = sp.symbols('x y', real=True)  # Ensure x and y are symbols

    # Print symbolic variables to verify
    print(f"x: {x}, y: {y}")
    M = str(M)
    N = str(N)
    # Differentiate M with respect to y and N with respect to x
    
    dM_dy = sp.diff(M, y)  # Partial derivative of M with respect to y
    dN_dx = sp.diff(N, x)  # Partial derivative of N with respect to x

    print(f"Raw dM/dy: {dM_dy}, Raw dN/dx: {dN_dx}")

    # Simplify the differentiated expressions
    dM_dy = dM_dy.simplify()
    dN_dx = dN_dx.simplify()

    print(f"Simplified dM/dy: {dM_dy}, Simplified dN/dx: {dN_dx}")

    # Return whether the equation is exact (i.e., derivatives match)
    return dM_dy == dN_dx



def parse_input(equation_str):
    x, y = sp.symbols('x y', real=True)  # Ensure they are treated as variables, not functions
    
    print(f"x: {x}, y: {y}")  # Debugging symbolic variables

    # Normalize the input
    equation_str = equation_str.replace(" ", "")  # Remove all spaces
    equation_str = equation_str.replace("^", "**")  # Handle exponentiation

    # Temporarily replace `dx` and `dy` to protect them from regex modifications
    equation_str = equation_str.replace("dx", "_dx_").replace("dy", "_dy_")

    # Apply implicit multiplication rules
    equation_str = re.sub(r'(?<=\d)([a-zA-Z])', r'*\1', equation_str)  # Add multiplication after numbers
    equation_str = re.sub(r'([a-zA-Z])(?=[a-zA-Z])', r'\1*', equation_str)  # Add multiplication between variables

    # Restore `dx` and `dy`
    equation_str = equation_str.replace("_d*x_", "dx").replace("_d*y_", "dy")

    print(f"Normalized equation string: {equation_str}")  # Debugging

    try:
        # Ensure the equation contains `dx` or `dy`
        if "dx" not in equation_str and "dy" not in equation_str:
            raise ValueError("Invalid equation format: missing 'dx' or 'dy'.")

        # Split based on the "dx" and "dy" keywords
        parts = re.split(r'(?<![a-zA-Z])dx|(?<![a-zA-Z])dy', equation_str)
        print(f"Split parts: {parts}")  # Debugging
        if len(parts) < 2:
            raise ValueError("Invalid equation format: ensure the equation contains both M(x, y)dx and N(x, y)dy.")

        # Extract M and N by parsing the equation components
        M_part = parts[0]
        N_part = parts[1]
        print(f"M part: {M_part}, N part: {N_part}")  # Debugging

        M = sp.sympify(M_part)
        N = sp.sympify(N_part)
    except Exception as e:
        print(f"Parse Input Error: {e}")  # Debugging
        raise ValueError("Invalid input format. Ensure it's in the form 'M(x, y)dx + N(x, y)dy'.")
    
    print(f"M: {M} ,N: {N}")
    return M, N






def analyze_functions(equation_str):
    try:
        M, N = parse_input(equation_str)
        print(f"Type of M: {type(M)}, Type of N: {type(N)}")
        print(f"Parsed M: {M}, Parsed N: {N}")

    except ValueError as e:
        print("Analyze Function error")
        return str(e)

    is_homogeneous, degree = check_homogeneity(M, N)
    is_exact = check_exactness(M, N)

    return {
        "is_homogeneous": is_homogeneous,
        "degree": degree,
        "is_exact": is_exact
    }

def on_submit():
    equation_str = input_entry.get()
    try:
        result = analyze_functions(equation_str)
        homogeneous = "Yes" if result["is_homogeneous"] else "No"
        degree = result["degree"] if result["is_homogeneous"] else "N/A"
        exact = "Yes" if result["is_exact"] else "No"
        result_label.config(
            text=f"Homogeneous: {homogeneous}\nDegree: {degree}\nExact: {exact}",
            fg="white"
        )
    except Exception as e:
        print("On submit error")
        messagebox.showerror("Error", f"Invalid input: {str(e)}. Please ensure the equation is in the form 'M(x, y)dx + N(x, y)dy'.")


# Tkinter GUI
root = tk.Tk()
root.title("Differential Equation Analyzer")
root.geometry("600x400")  # Set window size to 600x400

# Dark theme colors
bg_color = "#2c2f33"
fg_color = "#ffffff"
entry_bg = "#23272a"
entry_fg = "#ffffff"
button_bg = "#7289da"
button_fg = "#ffffff"

root.configure(bg=bg_color)

# Title label
title_label = tk.Label(
    root, 
    text="Differential Equation Analyzer", 
    font=("Helvetica", 16, "bold"), 
    bg=bg_color, 
    fg=fg_color
)
title_label.pack(pady=20)

# Input frame
input_frame = tk.Frame(root, bg=bg_color)
input_frame.pack(pady=15)

input_label = tk.Label(
    input_frame, 
    text="Enter Equation (e.g., M(x, y)dx + N(x, y)dy):\n(x+y)dx + (x-y)dy", 
    font=("Helvetica", 12), 
    bg=bg_color, 
    fg=fg_color
)
input_label.grid(row=0, column=0, padx=5, pady=10)

input_entry = tk.Entry(
    input_frame, 
    font=("Helvetica", 12), 
    bg=entry_bg, 
    fg=entry_fg, 
    width=60,  # Increased width for larger window
    insertbackground=fg_color
)
input_entry.grid(row=1, column=0, padx=5, pady=10)

# Submit button
submit_button = tk.Button(
    root, 
    text="Analyze", 
    font=("Helvetica", 12), 
    bg=button_bg, 
    fg=button_fg, 
    command=on_submit
)
submit_button.pack(pady=15)

# Result label
result_label = tk.Label(
    root, 
    text="", 
    font=("Helvetica", 12), 
    bg=bg_color, 
    fg=fg_color
)
result_label.pack(pady=15)

# Run the application
root.mainloop()
