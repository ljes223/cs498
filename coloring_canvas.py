# coloring_canvas.py - Enhanced coloring functionality with overlay

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageOps
import numpy as np

class ColoringCanvas(ttk.Frame):
    def __init__(self, parent, image_path, db_manager, page_id):
        super().__init__(parent)
        self.db_manager = db_manager
        self.page_id = page_id
        self.image_path = image_path
        
        # Canvas setup
        self.canvas_width = 600
        self.canvas_height = 600
        
        # Drawing state
        self.colors = {
            'red': '#FF0000',
            'blue': '#0000FF',
            'green': '#008000',
            'yellow': '#FFFF00',
            'purple': '#800080',
            'orange': '#FFA500',
            'pink': '#FFC0CB',
            'brown': '#8B4513'
        }
        self.current_color = 'red'
        self.drawing = False
        self.brush_size = 5
        self.drawing_tag = 'drawing'  # Initialize drawing tag
        
        self.setup_ui()
        self.load_image_with_overlay()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Create single canvas for both drawing and overlay
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.grid(row=0, column=0, padx=5, pady=5)
        
        # Control panel
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, pady=5)
        
        # Color buttons
        color_frame = ttk.Frame(control_frame)
        color_frame.pack(side=tk.LEFT, padx=5)
        
        for color_name, color_value in self.colors.items():
            btn = tk.Button(color_frame, bg=color_value, width=3, 
                          command=lambda c=color_name: self.select_color(c))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Tool buttons
        tool_frame = ttk.Frame(control_frame)
        tool_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(tool_frame, text='Eraser', command=self.erase_mode).pack(side=tk.LEFT, padx=2)
        ttk.Button(tool_frame, text='Reset', command=self.reset_canvas).pack(side=tk.LEFT, padx=2)
        
        # Brush size control
        size_frame = ttk.Frame(control_frame)
        size_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(size_frame, text="Brush Size:").pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=5)
        ttk.Scale(size_frame, from_=1, to=20, variable=self.size_var, orient=tk.HORIZONTAL,
                 command=self.update_brush_size).pack(side=tk.LEFT)
        
        # Create questions panel
        self.questions_panel = ttk.LabelFrame(self, text="Questions")
        self.questions_panel.grid(row=0, column=1, sticky='n', padx=5, pady=5)
        
        self.load_questions()
        
        # Bind mouse events to canvas
        self.canvas.bind('<Button-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_draw)
    
    def load_image_with_overlay(self):
        """Load image and create overlay effect"""
        try:
            # Open and resize the original image
            image = Image.open(self.image_path)
            image.thumbnail((self.canvas_width, self.canvas_height), Image.LANCZOS)
            
            # Convert to RGBA for transparency
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Create a white background image for drawing
            self.background_image = Image.new('RGB', (self.canvas_width, self.canvas_height), 'white')
            
            # Paste the resized image on the canvas for reference
            x_offset = (self.canvas_width - image.width) // 2
            y_offset = (self.canvas_height - image.height) // 2
            
            # Convert the original image to PhotoImage for display
            self.original_image_tk = ImageTk.PhotoImage(image)
            
            # Create a mask of the dark lines
            gray_image = image.convert('L')
            threshold = 50  # Pixels darker than this are considered lines
            mask = np.array(gray_image)
            self.line_mask = mask < threshold  # Boolean mask where True indicates line pixels
            
            # Store image dimensions for later use
            self.image_bounds = (x_offset, y_offset, x_offset + image.width, y_offset + image.height)
            
            # Display the image on canvas
            self.canvas.create_image(x_offset, y_offset, image=self.original_image_tk, anchor=tk.NW, tags='overlay')
            
            # Note: drawing_tag is already initialized in __init__
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def load_questions(self):
        """Load questions for the current page"""
        questions = self.db_manager.get_questions_for_page(self.page_id)
        
        # Store answer variables for reset functionality
        self.answer_vars = []
        
        for i, question in enumerate(questions):
            q_id, page_id, question_text, correct_answer, color_section = question
            
            # Create question frame
            q_frame = ttk.Frame(self.questions_panel)
            q_frame.pack(fill=tk.X, pady=5)
            
            # Question label
            ttk.Label(q_frame, text=f"{i+1}. {question_text}", wraplength=200).pack(anchor='w')
            
            # Answer entry
            answer_var = tk.StringVar()
            self.answer_vars.append(answer_var)  # Store for reset
            entry = ttk.Entry(q_frame, textvariable=answer_var)
            entry.pack(fill=tk.X, padx=5)
            
            # Check button
            ttk.Button(q_frame, text="Check", 
                      command=lambda a=answer_var, c=correct_answer: self.check_answer(a, c)).pack()
    
    def check_answer(self, answer_var, correct_answer):
        """Check if the answer is correct"""
        if answer_var.get().strip().lower() == correct_answer.lower():
            tk.messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            tk.messagebox.showinfo("Incorrect", "That's not quite right. Try again!")
    
    def start_draw(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
    
    def draw(self, event):
        if self.drawing:
            color = 'white' if self.current_color == 'eraser' else self.colors.get(self.current_color, 'black')
            
            # Draw on canvas with a lower-level drawing element
            self.canvas.create_oval(
                event.x - self.brush_size, event.y - self.brush_size,
                event.x + self.brush_size, event.y + self.brush_size,
                fill=color, outline=color, tags=self.drawing_tag
            )
            
            # Re-raise the overlay image to stay on top
            self.canvas.tag_raise('overlay')
            
            self.last_x = event.x
            self.last_y = event.y
    
    def stop_draw(self, event):
        self.drawing = False
    
    def select_color(self, color):
        self.current_color = color
    
    def erase_mode(self):
        self.current_color = 'eraser'
    
    def reset_canvas(self):
        # Delete only the drawing elements, keep the overlay
        self.canvas.delete(self.drawing_tag)
        
        # Clear all answer entries
        if hasattr(self, 'answer_vars'):
            for answer_var in self.answer_vars:
                answer_var.set('')  # Clear the text
    
    def update_brush_size(self, value):
        self.brush_size = int(float(value))