# database_manager.py - Manages coloring pages and questions database

import sqlite3
import os
import json

class DatabaseManager:
    def __init__(self, db_path='coloring_book.db'):
        self.db_path = db_path
        self.initialize_database()
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table for coloring pages with unique constraint
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS coloring_pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    image_path TEXT NOT NULL,
                    difficulty TEXT,
                    UNIQUE(name, image_path)
                )
            ''')
            
            # Table for questions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page_id INTEGER,
                    question_text TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    color_section TEXT,
                    FOREIGN KEY (page_id) REFERENCES coloring_pages(id),
                    UNIQUE(page_id, question_text)
                )
            ''')
            
            conn.commit()
    
    def add_coloring_page(self, name, image_path, category=None, difficulty=None):
        """Add a new coloring page to the database, ignoring duplicates"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO coloring_pages (name, category, image_path, difficulty)
                    VALUES (?, ?, ?, ?)
                ''', (name, category, image_path, difficulty))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # If duplicate, return the existing page's ID
                cursor.execute('''
                    SELECT id FROM coloring_pages WHERE name = ? AND image_path = ?
                ''', (name, image_path))
                result = cursor.fetchone()
                return result[0] if result else None
    
    def add_question(self, page_id, question_text, correct_answer, color_section=None):
        """Add a question to a coloring page, ignoring duplicates"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO questions (page_id, question_text, correct_answer, color_section)
                    VALUES (?, ?, ?, ?)
                ''', (page_id, question_text, correct_answer, color_section))
                conn.commit()
            except sqlite3.IntegrityError:
                # Silently ignore duplicate questions
                pass
    
    def get_all_coloring_pages(self):
        """Retrieve all coloring pages"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM coloring_pages')
            pages = cursor.fetchall()
            return pages
    
    def get_questions_for_page(self, page_id):
        """Get all questions for a specific coloring page"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM questions WHERE page_id = ?', (page_id,))
            questions = cursor.fetchall()
            return questions
    
    def clear_database(self):
        """Clear all data from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM questions')
            cursor.execute('DELETE FROM coloring_pages')
            conn.commit()
            print("Database cleared successfully!")
    
    def remove_coloring_page(self, page_id):
        """Remove a specific coloring page and its questions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM questions WHERE page_id = ?', (page_id,))
            cursor.execute('DELETE FROM coloring_pages WHERE id = ?', (page_id,))
            conn.commit()