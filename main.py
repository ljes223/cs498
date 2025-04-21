# main.py - Entry point for the application

import tkinter as tk
from image_viewer import ImageViewer
from database_manager import DatabaseManager

def main():
    root = tk.Tk()
    root.title("Educational Coloring Book")
    
    # Initialize database manager
    db_manager = DatabaseManager()
    
    # Create main application
    app = ImageViewer(root, db_manager)
    
    root.mainloop()

if __name__ == "__main__":
    main()