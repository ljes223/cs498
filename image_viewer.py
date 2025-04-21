# image_viewer.py - Main application window and page selection

import tkinter as tk
from tkinter import ttk, messagebox
from coloring_canvas import ColoringCanvas

class ImageViewer:
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager
        self.current_page_id = None
        
        # Configure main window
        self.root.geometry("800x700")
        
        # Create main frames
        self.create_menu_frame()
        self.create_content_frame()
    
    def create_menu_frame(self):
        """Create the menu frame with page selection"""
        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Page selection dropdown
        ttk.Label(self.menu_frame, text="Select Page:").pack(side=tk.LEFT, padx=5)
        
        self.page_var = tk.StringVar()
        self.page_combo = ttk.Combobox(self.menu_frame, textvariable=self.page_var, state='readonly')
        self.page_combo.pack(side=tk.LEFT, padx=5)
        self.page_combo.bind('<<ComboboxSelected>>', self.on_page_selected)
        
        self.refresh_page_list()
    
    def create_content_frame(self):
        """Create the frame for displaying coloring pages"""
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Welcome message
        self.welcome_label = ttk.Label(self.content_frame, 
                                      text="Welcome! Select a coloring page to begin.",
                                      font=('Arial', 16))
        self.welcome_label.pack(pady=20)
    
    def refresh_page_list(self):
        """Refresh the list of available coloring pages"""
        pages = self.db_manager.get_all_coloring_pages()
        page_names = [f"{page[1]} ({page[2] or 'General'})" for page in pages]
        self.page_combo['values'] = page_names
        self.pages_data = pages  # Store page data for reference
    
    def on_page_selected(self, event):
        """Handle page selection"""
        selected_index = self.page_combo.current()
        if selected_index >= 0:
            page_data = self.pages_data[selected_index]
            self.current_page_id = page_data[0]
            self.load_coloring_page(page_data)
    
    def load_coloring_page(self, page_data):
        """Load the selected coloring page"""
        page_id, name, category, image_path, difficulty = page_data
        
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create coloring canvas
        canvas_frame = ColoringCanvas(self.content_frame, image_path, self.db_manager, page_id)
        canvas_frame.pack(fill=tk.BOTH, expand=True)