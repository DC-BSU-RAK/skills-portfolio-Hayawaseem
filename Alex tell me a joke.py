import tkinter as tk
import random
import os
import winsound  # for playing click.wav

class JokeTellerApp:
    def __init__(self, master):
        self.master = master
        master.title("Alexa Tell Me a Joke")
        master.geometry("900x600")  # Bigger window
        master.minsize(900, 600)
        master.config(bg='#FFF9F0')  # Soft cream background

        # Background animation 
        self.bg_canvas = tk.Canvas(master, width=900, height=600, highlightthickness=0, bg='#FFF9F0')
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.bubbles = []
        self.create_bubbles()
        self.animate_bubbles()
        
        # Path to jakes file 
        script_dir = os.path.dirname(__file__)
        self.file_path = os.path.join(script_dir, 'resources', 'randomJokes.txt')

        self.jokes = self.load_jokes()
        self.current_joke = None
        self.punchline_chars = ""
        self.punchline_index = 0
        self.animation_id = None
        self.pulse_id = None

        # GUI Elements
        self.base_font_size = 16
        self.setup_label = tk.Label(master, text="Press 'Alexa tell me a Joke' to begin!",
                                    wraplength=850, font=('Roboto', self.base_font_size+4, 'italic'),
                                    bg='#FFF9F0', fg='#333333', pady=30)
        self.setup_label.pack()

        # Punchline Box
        self.punchline_frame = tk.Frame(master, bg="#FFF1C1", bd=2, relief=tk.RIDGE, padx=15, pady=15)
        self.punchline_frame.pack(pady=15)

        self.punchline_label = tk.Label(self.punchline_frame, text="", wraplength=820,
                                        font=('Roboto', 22, 'bold'), fg='#444444',
                                        bg="#FFF1C1", pady=10)
        self.punchline_label.pack()

        # Additional info label
        self.info_label = tk.Label(master, text="Your joke assistant is ready!",
                                   font=('Roboto', 16, 'italic'), fg='#7C6C8C',
                                   bg='#FFF9F0', pady=15)
        self.info_label.pack()

        # Button Frame
        self.button_frame = tk.Frame(master, bg='#FFF9F0')
        self.button_frame.pack(pady=40)

        button_font = ('Roboto', 14, 'bold')
        button_padx = 20
        button_pady = 10

        self.buttons = {}

        # Buttons
        self.joke_button = tk.Button(self.button_frame, text="Alexa tell me a Joke",
                                     command=lambda: [self.play_click_sound(), self.tell_joke()],
                                     bg='#FFB6B9', fg='white', font=button_font,
                                     relief=tk.FLAT, padx=button_padx, pady=button_pady, borderwidth=0)
        self.joke_button.pack(side=tk.LEFT, padx=10)
        self.buttons[self.joke_button] = {'bg': '#FFB6B9', 'activebg': '#FF9AA2', 'padx': button_padx, 'pady': button_pady}
        self.bind_hover_events(self.joke_button)

        self.punchline_button = tk.Button(self.button_frame, text="Show Punchline",
                                          command=lambda: [self.play_click_sound(), self.show_punchline()],
                                          state=tk.DISABLED,
                                          bg='#F6E2B3', fg='white', font=button_font,
                                          relief=tk.FLAT, padx=button_padx, pady=button_pady, borderwidth=0)
        self.punchline_button.pack(side=tk.LEFT, padx=10)
        self.buttons[self.punchline_button] = {'bg': '#F6E2B3', 'activebg': '#F1D48A', 'padx': button_padx, 'pady': button_pady}
        self.bind_hover_events(self.punchline_button)

        self.next_button = tk.Button(self.button_frame, text="Next Joke",
                                     command=lambda: [self.play_click_sound(), self.tell_joke()],
                                     state=tk.DISABLED,
                                     bg='#B3E5FC', fg='white', font=button_font,
                                     relief=tk.FLAT, padx=button_padx, pady=button_pady, borderwidth=0)
        self.next_button.pack(side=tk.LEFT, padx=10)
        self.buttons[self.next_button] = {'bg': '#B3E5FC', 'activebg': '#81D4FA', 'padx': button_padx, 'pady': button_pady}
        self.bind_hover_events(self.next_button)

        self.quit_button = tk.Button(master, text="Quit",
                                     command=lambda: [self.play_click_sound(), master.quit()],
                                     bg='#FF8A80', fg='white', font=button_font,
                                     relief=tk.FLAT, padx=button_padx, pady=button_pady, borderwidth=0)
        self.quit_button.pack(pady=20)
        self.buttons[self.quit_button] = {'bg': '#FF8A80', 'activebg': '#FF5252', 'padx': button_padx, 'pady': button_pady}
        self.bind_hover_events(self.quit_button)

# Click sound
    def play_click_sound(self):
        """Plays click.wav from resources folder."""
        try:
            click_path = os.path.join(os.path.dirname(__file__), 'resources', 'click.wav')
            winsound.PlaySound(click_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            pass

    # Background Bubble
    def create_bubbles(self):
        colors = ['#FFE0E6', '#FFF0B3', '#B3E5FC', '#FFF1C1']  # soft pastel bubbles
        for _ in range(25):
            x = random.randint(0, 900)
            y = random.randint(0, 600)
            size = random.randint(30, 100)
            color = random.choice(colors)
            bubble = self.bg_canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
            speed = random.uniform(0.2, 0.8)
            self.bubbles.append((bubble, size, speed))

    def animate_bubbles(self):
        for bubble, size, speed in self.bubbles:
            self.bg_canvas.move(bubble, 0, -speed)
            x1, y1, x2, y2 = self.bg_canvas.coords(bubble)
            if y2 < 0:
                new_x = random.randint(0, 900)
                self.bg_canvas.coords(bubble, new_x, 620, new_x + size, 620 + size)
        self.master.after(30, self.animate_bubbles)

    # Button hover effects
    def bind_hover_events(self, widget):
        widget.bind("<Enter>", lambda event: self.on_hover(widget, True))
        widget.bind("<Leave>", lambda event: self.on_hover(widget, False))

    def on_hover(self, widget, is_entering):
        config = self.buttons[widget]
        if is_entering:
            widget.config(bg=config['activebg'], padx=config['padx'] + 5, pady=config['pady'] + 2)
        else:
            widget.config(bg=config['bg'], padx=config['padx'], pady=config['pady'])

    # Pluse animation 
    def pulse_label(self, step=0):
        if self.pulse_id is None:
            return
        max_step = 5
        duration = 50
        if step < max_step:
            new_size = self.base_font_size + step
            self.setup_label.config(font=('Roboto', new_size, 'italic'))
            step += 1
            self.pulse_id = self.master.after(duration, lambda: self.pulse_label(step))
        elif step < max_step * 2:
            new_size = self.base_font_size + (max_step * 2) - step
            self.setup_label.config(font=('Roboto', new_size, 'italic'))
            step += 1
            self.pulse_id = self.master.after(duration, lambda: self.pulse_label(step))
        else:
            self.setup_label.config(font=('Roboto', self.base_font_size, 'italic'))
            self.pulse_id = None

    # Joke Loading 
    def load_jokes(self):
        jokes = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '?' in line:
                        setup, punchline = line.split('?', 1)
                        jokes.append((setup.strip() + '?', punchline.strip()))
            if not jokes:
                jokes.append(("Why did the developer go broke?", "Because he used up all his cache!"))
            return jokes
        except FileNotFoundError:
            self.setup_label.config(text=f"Error: Joke file not found at {self.file_path}", fg='red')
            return [("Could not load jokes!", "Ensure 'randomJokes.txt' is in the 'resources' folder.")]
        except Exception as e:
            self.setup_label.config(text=f"Error loading jokes: {e}", fg='red')
            return [("Loading Error!", f"Details: {e}")]

    # Joke Logic
    def tell_joke(self):
        if self.animation_id:
            self.master.after_cancel(self.animation_id)
            self.animation_id = None
        if self.pulse_id:
            self.master.after_cancel(self.pulse_id)
            self.pulse_id = None
        if not self.jokes:
            return
        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.info_label.config(text="Here's a new joke for you!")
        self.punchline_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)
        self.joke_button.pack_forget()
        self.next_button.pack(side=tk.LEFT, padx=10)
        self.pulse_label(1)

    def animate_punchline(self):
        if self.punchline_index < len(self.punchline_chars):
            current_text = self.punchline_label.cget("text")
            self.punchline_label.config(text=current_text + self.punchline_chars[self.punchline_index])
            self.punchline_index += 1
            self.animation_id = self.master.after(50, self.animate_punchline)
        else:
            self.animation_id = None

    def show_punchline(self):
        if self.current_joke:
            _, punchline = self.current_joke
            self.punchline_chars = punchline
            self.punchline_index = 0
            self.punchline_label.config(text="")
            self.animate_punchline()
            self.punchline_button.config(state=tk.DISABLED)


# Main Execution
if __name__ == "__main__":
    # Ensure resources folder exists
    resource_dir = os.path.join(os.path.dirname(__file__), 'resources')
    os.makedirs(resource_dir, exist_ok=True)

    # Initialize Tkinter root window
    root = tk.Tk()

    # Add Icon
    icon_path = os.path.join(resource_dir, 'joke.ico')  # Path to your icon
    try:
        root.iconbitmap(icon_path)  # Set window icon
    except Exception as e:
        print(f"Icon could not be loaded: {e}")

    # Launch the app
    app = JokeTellerApp(root)
    root.mainloop()
