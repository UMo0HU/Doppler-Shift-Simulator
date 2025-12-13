from tkinter import *
import tkinter.font as tkFont
from input_validation import InputValidator
from doppler_shift_simulator import DopplerSimulator

# Colors
taupe_grey = "#7a6563"
light_bronze = "#d3a588"
toasted_almond = "#c88e6a"
sand_duno = "#ece2d0"
parchment = "#f9f6f1"
silver = "#d1c8c7"

# Units
conversions = ["Hz", "MHz", "GHz"]
speed_units = ["m/s", "km/h"]

# Window Setup
window = Tk()
window.geometry("720x620")
window.resizable(False, False)
window.title("Doppler Shifter Simulator")
window.config(background=taupe_grey)

icon = PhotoImage(file="./smartphone.png")
window.iconphoto(True, icon)

# Fonts
try:
    error_custom_font = tkFont.Font(family="Source Sans Pro", size=12)
    label_custom_font = tkFont.Font(family="Source Sans Pro", size=16, weight="bold")
    button_custom_font = tkFont.Font(family="Source Sans Pro", size=24, weight="bold")
except:
    print("Source Sans Pro not found, using Helvetica fallback.")
    error_custom_font = tkFont.Font(family="Helvetica", size=12)
    label_custom_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
    button_custom_font = tkFont.Font(family="Helvetica", size=24, weight="bold")

# Labels
fc_label = Label(window, text="Carrier Frequency", font=label_custom_font, fg=sand_duno, bg=taupe_grey)
fc_label.place(x=27, y=51)

speed_label = Label(window, text="Speed", font=label_custom_font, fg=sand_duno, bg=taupe_grey)
speed_label.place(x=362.5, y=51)

angle_label = Label(window, text="Angle (deg)", font=label_custom_font, fg=sand_duno, bg=taupe_grey)
angle_label.place(x=547, y=51)

# Input Fields
fc_input = Entry(window, font=button_custom_font, width=8,
                 bg=light_bronze, fg=parchment, border=0)
fc_input.place(x=45, y=85)

speed_input = Entry(window, font=button_custom_font, width=6,
                    bg=light_bronze, fg=parchment, border=0)
speed_input.place(x=345, y=85)

angle_input = Entry(window, font=button_custom_font, width=6,
                    bg=light_bronze, fg=parchment, border=0)
angle_input.place(x=550, y=85)

# Error Labels
fc_error = Label(window, text="", font=error_custom_font, fg="red", bg=taupe_grey)
fc_error.place(x=25, y=130)

speed_error = Label(window, text="", font=error_custom_font, fg="red", bg=taupe_grey)
speed_error.place(x=335, y=130)

angle_error = Label(window, text="", font=error_custom_font, fg="red", bg=taupe_grey)
angle_error.place(x=545, y=130)

# Frequency Unit Conversion
X = IntVar()
conversion_frame = Frame(window, bg=silver, padx=20, pady=15)
conversion_frame.place(x=27, y=160)

for index in range(len(conversions)):
    Radiobutton(
        conversion_frame,
        text=conversions[index],
        variable=X,
        value=index,
        indicatoron=0,
        font=label_custom_font,
        bg=silver,
        fg=taupe_grey
    ).pack(side=LEFT, padx=3)

# Speed Unit Conversion
speed_unit = IntVar()
speed_unit_frame = Frame(window, bg=silver, padx=20, pady=15)
speed_unit_frame.place(x=310, y=160)

for index in range(len(speed_units)):
    Radiobutton(
        speed_unit_frame,
        text=speed_units[index],
        variable=speed_unit,
        value=index,
        indicatoron=0,
        font=label_custom_font,
        bg=silver,
        fg=taupe_grey
    ).pack(side=LEFT, padx=3)

# Results Frame
result_frame = Frame(window, bg=silver, width=342, height=230, padx=20, pady=15)
result_frame.place(x=27, y=260)

lambda_label = Label(result_frame, text="λ = 0m", font=label_custom_font, fg=taupe_grey, bg=silver, anchor='w', pady=5)
lambda_label.pack(fill='both')

fd_label = Label(result_frame, text="Doppler shift (fD) = 0Hz", font=label_custom_font, fg=taupe_grey, bg=silver, anchor='w', pady=5)
fd_label.pack(fill='both')

recieved_freq_label = Label(result_frame, text="Received Frequency = 0Hz", font=label_custom_font, fg=taupe_grey, bg=silver, anchor='w', pady=5)
recieved_freq_label.pack(fill='both')

tc_label = Label(result_frame, text="Coherence Time (Tc) = 0s", font=label_custom_font, fg=taupe_grey, bg=silver, anchor='w', pady=5)
tc_label.pack(fill='both')

classification_label = Label(result_frame, text="classification = ", font=label_custom_font, fg=taupe_grey, bg=silver, anchor='w', pady=5)
classification_label.pack(fill='both')

# Calculation Function
def calculate():
    fc_val = fc_input.get()
    speed_val = speed_input.get()
    angle_val = angle_input.get()

    fc_is_valid, fc_error_msg, fc = InputValidator.validate_fc(fc_val, X.get())
    speed_is_valid, speed_error_msg, speed = InputValidator.validate_speed(speed_val)
    angle_is_valid, angle_error_msg, angle = InputValidator.validate_angle(angle_val)

    # Show errors
    fc_error.config(text=fc_error_msg)
    speed_error.config(text=speed_error_msg)
    angle_error.config(text=angle_error_msg)

    if fc_is_valid and speed_is_valid and angle_is_valid:

        if speed_unit.get() == 1:
            speed = speed / 3.6

        lam, fd, received_freq, tc, classification = DopplerSimulator.compute_doppler(fc, speed, angle)

        lambda_label.config(text=f"λ = {lam:.3f}m")
        sign = "+" if fd >= 0 else "-"
        fd_label.config(text=f"Doppler shift (fD) = {sign}{abs(fd):.2f}Hz")
        recieved_freq_label.config(text=f"Received Frequency = {received_freq:.2f}Hz")
        tc_label.config(text=f"Coherence Time (Tc) = {tc:.4f}s")
        classification_label.config(text=f"classification = {classification}")

# Plot Function
def plot():
    fc_val = fc_input.get()
    speed_val = speed_input.get()
    angle_val = angle_input.get()

    fc_is_valid, fc_error_msg, fc = InputValidator.validate_fc(fc_val, X.get())
    speed_is_valid, speed_error_msg, speed = InputValidator.validate_speed(speed_val)
    angle_is_valid, angle_error_msg, angle = InputValidator.validate_angle(angle_val)

    # Show errors
    fc_error.config(text=fc_error_msg)
    speed_error.config(text=speed_error_msg)
    angle_error.config(text=angle_error_msg)

    if fc_is_valid and speed_is_valid and angle_is_valid:

        if speed_unit.get() == 1:
            speed = speed / 3.6

        DopplerSimulator.plot_fd_angle(fc, speed)
        DopplerSimulator.plot_fd_speed(fc, angle)

# Buttons
calculate_button = Button(
    window, text="Calculate",
    fg=parchment, activeforeground=parchment,
    bg=light_bronze, activebackground=toasted_almond,
    font=button_custom_font, bd=0, command=calculate
)
calculate_button.place(x=27, y=500)

plot_button = Button(
    window, text="Plot",
    fg=parchment, activeforeground=parchment,
    bg=light_bronze, activebackground=toasted_almond,
    font=button_custom_font, bd=0, padx=45, command=plot
)
plot_button.place(x=250, y=500)

window.mainloop()
