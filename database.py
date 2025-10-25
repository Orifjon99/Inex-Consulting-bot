"""
SQLite Database handler for INEX CONSULTING Bot
"""
import sqlite3
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from config import DB_PATH

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """Create database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language TEXT DEFAULT 'uz',
                is_subscribed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Meeting dates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meeting_dates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Registrations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                fullname TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                company TEXT NOT NULL,
                meeting_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")

    # ========== USER METHODS ==========

    def add_user(self, user_id: int, username: str = None,
                 first_name: str = None, last_name: str = None,
                 language: str = 'uz'):
        """Add new user or update existing"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (user_id, username, first_name, last_name, language)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name
        ''', (user_id, username, first_name, last_name, language))

        conn.commit()
        conn.close()
        logger.info(f"User {user_id} added/updated")

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def set_user_language(self, user_id: int, language: str):
        """Update user language"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users SET language = ? WHERE user_id = ?
        ''', (language, user_id))

        conn.commit()
        conn.close()
        logger.info(f"User {user_id} language set to {language}")

    def set_user_subscribed(self, user_id: int, subscribed: bool = True):
        """Set user subscription status"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users SET is_subscribed = ? WHERE user_id = ?
        ''', (1 if subscribed else 0, user_id))

        conn.commit()
        conn.close()
        logger.info(f"User {user_id} subscription status: {subscribed}")

    def get_user_language(self, user_id: int) -> str:
        """Get user language preference"""
        user = self.get_user(user_id)
        return user['language'] if user else 'uz'

    # ========== MEETING DATES METHODS ==========

    def add_meeting_date(self, date: str):
        """Add new meeting date"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO meeting_dates (date) VALUES (?)
            ''', (date,))
            conn.commit()
            logger.info(f"Meeting date added: {date}")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Date already exists: {date}")
            return False
        finally:
            conn.close()

    def get_active_meeting_dates(self) -> List[str]:
        """Get all active meeting dates (including booked ones)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT date FROM meeting_dates
            WHERE is_active = 1
            ORDER BY date
        ''')

        dates = [row['date'] for row in cursor.fetchall()]
        conn.close()
        return dates

    def get_available_meeting_dates(self) -> List[str]:
        """Get only available (not booked) meeting dates"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get dates that are active AND not in registrations
        cursor.execute('''
            SELECT md.date
            FROM meeting_dates md
            WHERE md.is_active = 1
            AND md.date NOT IN (
                SELECT meeting_date FROM registrations
            )
            ORDER BY md.date
        ''')

        dates = [row['date'] for row in cursor.fetchall()]
        conn.close()
        return dates

    def get_booked_meeting_dates(self) -> List[str]:
        """Get booked (registered) meeting dates"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT meeting_date
            FROM registrations
            ORDER BY meeting_date
        ''')

        dates = [row['meeting_date'] for row in cursor.fetchall()]
        conn.close()
        return dates

    def remove_meeting_date(self, date: str):
        """Deactivate meeting date"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE meeting_dates SET is_active = 0 WHERE date = ?
        ''', (date,))

        conn.commit()
        conn.close()
        logger.info(f"Meeting date removed: {date}")

    def delete_meeting_date(self, date: str):
        """Permanently delete meeting date"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM meeting_dates WHERE date = ?', (date,))

        conn.commit()
        conn.close()
        logger.info(f"Meeting date deleted: {date}")

    # ========== REGISTRATION METHODS ==========

    def add_registration(self, user_id: int, fullname: str, phone: str,
                        address: str, company: str, meeting_date: str) -> int:
        """Add new registration"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO registrations (user_id, fullname, phone, address, company, meeting_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, fullname, phone, address, company, meeting_date))

        registration_id = cursor.lastrowid
        conn.commit()
        conn.close()
        logger.info(f"Registration added: ID {registration_id}, User {user_id}")
        return registration_id

    def get_registrations(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get all registrations"""
        conn = self.get_connection()
        cursor = conn.cursor()

        query = '''
            SELECT r.*, u.username, u.first_name, u.last_name
            FROM registrations r
            LEFT JOIN users u ON r.user_id = u.user_id
            ORDER BY r.created_at DESC
        '''

        if limit:
            query += f' LIMIT {limit}'

        cursor.execute(query)
        registrations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return registrations

    def get_user_registration(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user's registration"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM registrations
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_registrations_count(self) -> int:
        """Get total registrations count"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) as count FROM registrations')
        count = cursor.fetchone()['count']
        conn.close()
        return count

    def get_registrations_by_date(self, meeting_date: str) -> List[Dict[str, Any]]:
        """Get registrations for specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT r.*, u.username, u.first_name, u.last_name
            FROM registrations r
            LEFT JOIN users u ON r.user_id = u.user_id
            WHERE r.meeting_date = ?
            ORDER BY r.created_at DESC
        ''', (meeting_date,))

        registrations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return registrations

    # ========== CLEAR METHODS ==========

    def clear_all_registrations(self) -> int:
        """Delete all registrations and return count"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get count before deleting
        cursor.execute('SELECT COUNT(*) as count FROM registrations')
        count = cursor.fetchone()['count']

        # Delete all
        cursor.execute('DELETE FROM registrations')

        conn.commit()
        conn.close()
        logger.info(f"Cleared {count} registrations from database")
        return count

    def clear_all_meeting_dates(self) -> int:
        """Delete all meeting dates and return count"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get count before deleting
        cursor.execute('SELECT COUNT(*) as count FROM meeting_dates')
        count = cursor.fetchone()['count']

        # Delete all
        cursor.execute('DELETE FROM meeting_dates')

        conn.commit()
        conn.close()
        logger.info(f"Cleared {count} meeting dates from database")
        return count


# Create database instance
db = Database()
