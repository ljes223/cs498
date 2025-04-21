# database_utility.py - Utilities for managing the database

from database_manager import DatabaseManager
import os

def reset_database():
    """Reset the database by deleting it and recreating with default data"""
    db = DatabaseManager()
    
    # Option 1: Clear all data from existing database
    db.clear_database()
    
    # Option 2: Delete the database file entirely (uncomment if needed)
    # if os.path.exists('coloring_book.db'):
    #     os.remove('coloring_book.db')
    #     print("Database file deleted.")
    
    # Recreate the database with default data
    populate_default_data()

def populate_default_data():
    """Populate the database with default coloring pages and questions"""
    db = DatabaseManager()
    
    # Add coloring pages (duplicates will be ignored)
    turtle_id = db.add_coloring_page(
        name="Sea Turtle",
        image_path="images/coloringPageTurtle.png",
        category="Animals",
        difficulty="Easy"
    )
    
    flower_id = db.add_coloring_page(
        name="Flowers",
        image_path="images/coloringPageFlowers.png",
        category="Nature",
        difficulty="Medium"
    )
    
    space_id = db.add_coloring_page(
        name="Rocket Ship",
        image_path="images/coloringPageSpace.png",
        category="Science",
        difficulty="Medium"
    )
    
    # Add questions (duplicates will be ignored)
    if turtle_id:
        db.add_question(
            page_id=turtle_id,
            question_text="What is the largest species of sea turtle?",
            correct_answer="leatherback",
            color_section="green"
        )
        
        db.add_question(
            page_id=turtle_id,
            question_text="How many types of sea turtles exist worldwide?",
            correct_answer="7",
            color_section="blue"
        )
    
    if flower_id:
        db.add_question(
            page_id=flower_id,
            question_text="What is the process by which plants make their own food?",
            correct_answer="photosynthesis",
            color_section="green"
        )
        
        db.add_question(
            page_id=flower_id,
            question_text="What part of a flower produces pollen?",
            correct_answer="stamen",
            color_section="yellow"
        )
    
    if space_id:
        db.add_question(
            page_id=space_id,
            question_text="What is the third planet from the sun?",
            correct_answer="earth",
            color_section="blue"
        )
        
        db.add_question(
            page_id=space_id,
            question_text="What force keeps planets in orbit around the sun?",
            correct_answer="gravity",
            color_section="red"
        )
    
    print("Default data populated successfully!")

def view_database_contents():
    """View all coloring pages and questions in the database"""
    db = DatabaseManager()
    
    pages = db.get_all_coloring_pages()
    print("\n=== Coloring Pages ===")
    for page in pages:
        print(f"ID: {page[0]}, Name: {page[1]}, Category: {page[2]}, Path: {page[3]}")
        
        questions = db.get_questions_for_page(page[0])
        if questions:
            print("  Questions:")
            for q in questions:
                print(f"    - {q[2]} (Answer: {q[3]})")
        else:
            print("  No questions")
        print()

if __name__ == "__main__":
    print("Database Utility Menu:")
    print("1. Reset database (clear all data)")
    print("2. Populate default data")
    print("3. View database contents")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        reset_database()
    elif choice == "2":
        populate_default_data()
    elif choice == "3":
        view_database_contents()
    else:
        print("Invalid choice")