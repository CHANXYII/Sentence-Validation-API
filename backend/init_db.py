"""
Database initialization and table creation script.
Run this script to create all tables in your MySQL database.
"""

from config.database import engine, Base
from models.models import Vocabulary, PracticeSubmission


def init_db():
    """Create all tables in the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def seed_sample_data():
    """Add some sample vocabulary words for testing"""
    from config.database import SessionLocal
    
    db = SessionLocal()
    
    # Check if data already exists
    existing_count = db.query(Vocabulary).count()
    if existing_count > 0:
        print(f"Database already has {existing_count} vocabulary words. Skipping seed.")
        db.close()
        return
    
    # Sample vocabulary words
    sample_words = [
        Vocabulary(word="library", definition="A place where books are kept for reading or borrowing", difficulty_level="Beginner"),
        Vocabulary(word="magnificent", definition="Extremely beautiful, elaborate, or impressive", difficulty_level="Intermediate"),
        Vocabulary(word="serendipity", definition="The occurrence of events by chance in a happy or beneficial way", difficulty_level="Advanced"),
        Vocabulary(word="study", definition="The devotion of time and attention to acquiring knowledge", difficulty_level="Beginner"),
        Vocabulary(word="collaborate", definition="Work jointly on an activity or project", difficulty_level="Intermediate"),
    ]
    
    try:
        db.add_all(sample_words)
        db.commit()
        print(f"Added {len(sample_words)} sample vocabulary words!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_sample_data()
