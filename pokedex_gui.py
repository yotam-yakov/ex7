# pokedex_gui.py

import tkinter as tk
from PIL import Image, ImageTk
import os


def showPokedexGUI(pokeList):
    """
    Display each Pokemon in a simple Tkinter window with its Name, Type, HP,
    Attack, and optionally an image from the 'pokemons' folder.
    We allow horizontal resizing so each Pokemon 'frame' expands in width.
    """
    root = tk.Tk()
    root.title("My Pokedex GUI")

    # Create a canvas and a vertical scrollbar
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # This 'scrollable_frame' is where we'll place each Pokemon frame.
    scrollable_frame = tk.Frame(canvas)

    # A callback to update the scrollregion whenever 'scrollable_frame' changes size
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Actually place 'scrollable_frame' in the canvas
    # We'll store the canvas window ID so we can update its width on resize
    canvas_window = canvas.create_window(
        (0, 0), window=scrollable_frame, anchor="nw")

    # A callback to keep the scrollable_frame the same width as the canvas
    def on_canvas_configure(event):
        # Set the scrollable_frame width to match canvas' width
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", on_canvas_configure)

    # Mouse wheel handling
    def on_mouse_wheel(event):
        # On Windows/macOS: event.delta is typically ±120 per wheel step
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows/macOS
    # For Linux (buttons 4=up, 5=down):
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    if not pokeList:
        msg = tk.Label(scrollable_frame, text="No Pokemon in this Pokedex!")
        msg.pack(padx=10, pady=10)
    else:
        for poke in pokeList:
            # Create a frame for each Pokémon, fill horizontally, expand so it can grow
            frame = tk.Frame(scrollable_frame, bd=2,
                             relief='groove', padx=5, pady=5)
            frame.pack(side="top", fill="x", expand=True, padx=10, pady=5)

            # Pokemon text info
            info = (
                f"ID: {poke['ID']} | "
                f"Name: {poke['Name']} | "
                f"Type: {poke['Type']} | "
                f"HP: {poke['HP']} | "
                f"Attack: {poke['Attack']} | "
                f"Can Evolve: {poke['Can Evolve']}"
            )
            # The text label also fills horizontally and expands
            label = tk.Label(frame, text=info, anchor="w")
            label.pack(side="left", fill="x", expand=True)

            image_path = os.path.join("pokemons", f"{poke['ID'] + 251}.png")
            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img = img.resize((80, 80), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(img)
                    picLabel = tk.Label(frame, image=photo)
                    picLabel.photo = photo  # keep reference
                    picLabel.pack(side="right", padx=5)
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
                    # If error, we'll ignore and just not show the image

    root.mainloop()
