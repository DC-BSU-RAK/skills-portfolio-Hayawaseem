import tkinter as tk
import random
import os
import winsound  # For playing click.wav

class JokeTellerApp:
    def __init__(self, master):
        self.master = master
        master.title("Alexa Tell Me a Joke")
        master.geometry("600x400")
        master.config(bg='#E0F7FA')

        # --- Set window icon ---
        icon_path = os.path.join(os.path.dirname(__file__), 'joke.ico')
        if os.path.exists(icon_path):
            try:
                master.iconbitmap(icon_path)  # For .ico
            except:
                pass  # fallback: ignore if it fails

        # Determine the path to the randomJokes.txt file
        script_dir = os.path.dirname(__file__)
        self.file_path = os.path.join(script_dir, 'resources', 'randomJokes.txt')

        self.jokes = self.load_jokes()
        self.current_joke = None
        self.punchline_chars = ""
        self.punchline_index = 0
        self.animation_id = None
        self.setup_pulse_id = None
        self.punchline_pulse_id = None

        # --- GUI Elements Setup ---

        # 1. Setup Label
        self.base_font_size = 16
        self.setup_label = tk.Label(master, text="Press 'Alexa tell me a Joke' to begin!",
                                    wraplength=550, font=('Roboto', self.base_font_size, 'italic'),
                                    bg='#E0F7FA', fg='#333333', pady=20)
        self.setup_label.pack()

        # 2. Punchline Label (styled as a box)
        self.punchline_label = tk.Label(
            master,
            text="",
            wraplength=550,
            font=('Roboto', 18, 'bold'),
            fg='#00796B',
            bg='#B2DFDB',
            bd=2,
            relief=tk.SOLID,
            padx=10, pady=10
        )
        self.punchline_label.pack(pady=10)

        # --- Button Frame ---
        self.button_frame = tk.Frame(master, bg='#E0F7FA')
        self.button_frame.pack(pady=30)

        button_font = ('Roboto', 12, 'bold')
        button_padx = 15
        button_pady = 8
        self.buttons = {}

        # 3. Main Joke Button
        self.joke_button = tk.Button(
            self.button_frame,
            text="Alexa tell me a Joke",
            command=lambda: [self.play_click_sound(), self.tell_joke()],
            bg='#00BCD4', fg='white', font=button_font,
            relief=tk.FLAT, padx=button_padx, pady=button_pady, borderwidth=0
        )
        self.joke_button.pack(side=tk.LEFT, padx=10)
        self.buttons[self.joke_button] = {'bg': '#00BCD4', 'activebg': '#00ACC1', 'padx': 15, 'pady': 8}
        self.bind_hover_events(self.joke_button)

        # 4. Show Punchline Button
        self.punchline_button = tk.Button(
            self.button_frame,
            text="Show Punchline",
            command=lambda: [self.play_click_sound(), self.show_punchline()],
            state=tk.DISABLED,
            bg='#8BC34A', fg='white', font=button_font,
            relief=tk.FLAT, padx=button_padx, pady=button_pady, borderwidth=0
        )
        self.punchline_button.pack(side=tk.LEFT, padx=10)
        self.buttons[self.punchline_button] = {'bg': '#8BC34A', 'activebg': '#7CB342', 'padx': 15, 'pady': 8}
        self.bind_hover_events(self.punchline_button)

        # 5. Next Joke Button
        self.next_button = tk.Button(
            self.button_frame,
            text="Next Joke",
            command=lambda: [self.play_click_sound(), self.tell_joke()],
            state=tk.DISABLED,
            bg='#FFC107', fg='white', font=button_font,
            relief=tk.FLAT, padx=button_padx, pady=button_pady, borderwidth=0
        )
        self.next_button.pack(side=tk.LEFT, padx=10)
        self.buttons[self.next_button] = {'bg': '#FFC107', 'activebg': '#FFB300', 'padx': 15, 'pady': 8}
        self.bind_hover_events(self.next_button)

        # 6. Quit Button
        self.quit_button = tk.Button(
            master,
            text="Quit",
            command=lambda: [self.play_click_sound(), master.quit()],
            bg='#F44336', fg='white', font=button_font,
            relief=tk.FLAT, padx=button_padx, pady=button_pady, borderwidth=0
        )
        self.quit_button.pack(pady=20)
        self.buttons[self.quit_button] = {'bg': '#F44336', 'activebg': '#D32F2F', 'padx': 15, 'pady': 8}
        self.bind_hover_events(self.quit_button)

    # --- Click Sound ---
    def play_click_sound(self):
        sound_path = os.path.join(os.path.dirname(__file__), 'click.wav')
        if os.path.exists(sound_path):
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    # --- Hover Animations ---
    def bind_hover_events(self, widget):
        widget.bind("<Enter>", lambda event: self.on_hover(widget, True))
        widget.bind("<Leave>", lambda event: self.on_hover(widget, False))

    def on_hover(self, widget, is_entering):
        config = self.buttons[widget]
        if is_entering:
            widget.config(bg=config['activebg'], padx=config['padx'] + 5, pady=config['pady'] + 2)
        else:
            widget.config(bg=config['bg'], padx=config['padx'], pady=config['pady'])

    # --- Pulse Animations ---
    def pulse_setup_label(self, step=0):
        if self.setup_pulse_id is None:
            return
        max_step = 5
        duration = 50
        if step < max_step:
            new_size = self.base_font_size + step
            self.setup_label.config(font=('Roboto', new_size, 'italic'))
            step += 1
            self.setup_pulse_id = self.master.after(duration, lambda: self.pulse_setup_label(step))
        elif step < max_step * 2:
            new_size = self.base_font_size + (max_step * 2) - step
            self.setup_label.config(font=('Roboto', new_size, 'italic'))
            step += 1
            self.setup_pulse_id = self.master.after(duration, lambda: self.pulse_setup_label(step))
        else:
            self.setup_label.config(font=('Roboto', self.base_font_size, 'italic'))
            self.setup_pulse_id = None

    def pulse_punchline_label(self, step=0):
        if self.punchline_pulse_id is None:
            return
        max_step = 3
        duration = 50
        if step < max_step:
            self.punchline_label.config(font=('Roboto', 18 + step, 'bold'))
            step += 1
            self.punchline_pulse_id = self.master.after(duration, lambda: self.pulse_punchline_label(step))
        elif step < max_step * 2:
            self.punchline_label.config(font=('Roboto', 18 + (max_step * 2) - step, 'bold'))
            step += 1
            self.punchline_pulse_id = self.master.after(duration, lambda: self.pulse_punchline_label(step))
        else:
            self.punchline_label.config(font=('Roboto', 18, 'bold'))
            self.punchline_pulse_id = None

    # --- Joke Logic ---
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
            return [("Could not load jokes!", "Please ensure 'randomJokes.txt' is in the 'resources' folder.")]
        except Exception as e:
            self.setup_label.config(text=f"An error occurred while loading jokes: {e}", fg='red')
            return [("Loading Error!", f"Details: {e}")]

    def tell_joke(self):
        if self.animation_id:
            self.master.after_cancel(self.animation_id)
            self.animation_id = None
        if self.setup_pulse_id:
            self.master.after_cancel(self.setup_pulse_id)
            self.setup_pulse_id = None
        if self.punchline_pulse_id:
            self.master.after_cancel(self.punchline_pulse_id)
            self.punchline_pulse_id = None

        if not self.jokes:
            return

        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke

        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")

        self.punchline_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)

        self.joke_button.pack_forget()
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.setup_pulse_id = 1
        self.pulse_setup_label()

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

            self.punchline_pulse_id = 1
            self.pulse_punchline_label()

# --- Main execution ---
if __name__ == "__main__":
    resource_dir = os.path.join(os.path.dirname(__file__), 'resources')
    os.makedirs(resource_dir, exist_ok=True)

    dummy_file_path = os.path.join(resource_dir, 'randomJokes.txt')
    new_joke_content = """Why did the chicken cross the road?To get to the other side.
What happens if you boil a clown?You get a laughing stock.
What do you call a fake noodle?An impasta.
I told my wife she was drawing her eyebrows too high.She looked surprised.
What do you call a fish with no eyes?Fsh.
Why don't scientists trust atoms?Because they make up everything.
What's orange and sounds like a parrot?A carrot.
What do you call a lazy kangaroo?Pouch potato.
How do you organize a space party?You planet.
Did you hear about the invisible man who lost his wife?He couldn't see her marrying anyone else.
What's a vampire's favorite fruit?A neck-tarine.
I'm reading a book about anti-gravity.It's impossible to put down!
Why don't skeletons fight each other?They don't have the guts.
What do you call a snowman with a six-pack?An abdominal snowman.
Why was the math book sad?Because it had too many problems.
What do you call cheese that isn't yours?Nacho cheese.
Why can't you hear a Pterodactyl go to the bathroom?Because the 'P' is silent.
Why did the bicycle fall over?Because it was two tired.
What did the triangle say to the circle?You’re pointless.
What did the husband pen say to the wife pen?You’re always write.
Who makes money by driving their customers away?Uber drivers.
"""
    with open(dummy_file_path, 'w', encoding='utf-8') as f:
        f.write(new_joke_content)

    root = tk.Tk()
    app = JokeTellerApp(root)
    root.mainloop()
