import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='mediconnect.db'):
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                location TEXT,
                emergency_contact TEXT,
                medical_history TEXT,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'patient',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')

        # Doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                rating REAL,
                status TEXT DEFAULT 'available',
                experience TEXT,
                location TEXT,
                languages TEXT,
                consultation_fee REAL DEFAULT 0,
                available BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                status TEXT DEFAULT 'scheduled',
                reason TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES users (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')

        # Symptom analyses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS symptom_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                symptoms TEXT,
                analysis TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES users (id)
            )
        ''')

        # Insert default doctors if not exists
        cursor.execute("SELECT COUNT(*) FROM doctors")
        if cursor.fetchone()[0] == 0:
            doctors_data = [
                ('Dr. Sarah Johnson', 'General Medicine', 4.8, 'online', '15 years', 'Manila', 'English,Tagalog', 500, 1),
                ('Dr. Michael Chen', 'Cardiology', 4.9, 'available', '12 years', 'Cebu', 'English,Mandarin', 800, 1),
                ('Dr. Maria Santos', 'Pediatrics', 4.7, 'online', '8 years', 'Davao', 'Tagalog,English,Visayan', 400, 1),
                ('Dr. James Rodriguez', 'Dermatology', 4.6, 'available', '10 years', 'Manila', 'English,Spanish', 600, 1),
                ('Dr. Robert Kim', 'Orthopedics', 4.7, 'offline', '14 years', 'Quezon City', 'English,Korean', 700, 0),
                ('Dr. Elena Cruz', 'Gynecology', 4.8, 'online', '11 years', 'Makati', 'English,Tagalog,Spanish', 550, 1),
                ('Dr. David Wong', 'Neurology', 4.9, 'available', '16 years', 'Manila', 'English,Mandarin,Cantonese', 900, 1),
                ('Dr. Anna Reyes', 'Psychiatry', 4.6, 'offline', '9 years', 'Cebu', 'English,Tagalog,Visayan', 650, 0),
                ('Dr. Carlos Mendoza', 'Ophthalmology', 4.7, 'online', '13 years', 'Davao', 'English,Spanish', 450, 1),
                ('Dr. Fatima Al-Sayed', 'Internal Medicine', 4.8, 'available', '17 years', 'Quezon City', 'English,Arabic', 550, 1),
                ('Dr. Hiroshi Tanaka', 'Surgery', 4.9, 'offline', '20 years', 'Makati', 'English,Japanese', 1000, 0),
                ('Dr. Sofia Patel', 'Endocrinology', 4.7, 'online', '12 years', 'Manila', 'English,Hindi', 600, 1),
                ('Dr. Ahmed Hassan', 'Urology', 4.6, 'available', '14 years', 'Quezon City', 'English,Arabic', 650, 1),
                ('Dr. Lisa Wong', 'Dermatology', 4.8, 'offline', '9 years', 'Makati', 'English,Mandarin,Cantonese', 550, 0),
                ('Dr. Ricardo Santos', 'Cardiology', 4.9, 'online', '18 years', 'Cebu', 'English,Spanish,Visayan', 850, 1),
                ('Dr. Priya Sharma', 'Pediatrics', 4.7, 'available', '11 years', 'Davao', 'English,Hindi,Tagalog', 450, 1),
                ('Dr. Thomas Mueller', 'Orthopedics', 4.8, 'offline', '16 years', 'Manila', 'English,German', 750, 0),
                ('Dr. Maria Gonzalez', 'Gynecology', 4.6, 'online', '13 years', 'Quezon City', 'English,Spanish,Tagalog', 500, 1),
                ('Dr. Kenji Nakamura', 'Neurology', 4.9, 'available', '15 years', 'Makati', 'English,Japanese', 800, 1)
            ]

            cursor.executemany('''
                INSERT INTO doctors (name, specialty, rating, status, experience, location, languages, consultation_fee, available)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', doctors_data)

        # Insert default doctor users if not exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'doctor'")
        if cursor.fetchone()[0] == 0:
            doctor_users_data = [
                ('Dr. Sarah Johnson', 45, 'Female', 'sarah.johnson@mediconnect.com', '+63 912 345 6789', 'Manila', '', '', 'doctor123', 'doctor'),
                ('Dr. Michael Chen', 42, 'Male', 'michael.chen@mediconnect.com', '+63 923 456 7890', 'Cebu', '', '', 'doctor123', 'doctor'),
                ('Dr. Maria Santos', 38, 'Female', 'maria.santos@mediconnect.com', '+63 934 567 8901', 'Davao', '', '', 'doctor123', 'doctor'),
                ('Dr. James Rodriguez', 40, 'Male', 'james.rodriguez@mediconnect.com', '+63 945 678 9012', 'Manila', '', '', 'doctor123', 'doctor'),
                ('Dr. Robert Kim', 48, 'Male', 'robert.kim@mediconnect.com', '+63 956 789 0123', 'Quezon City', '', '', 'doctor123', 'doctor'),
                ('Dr. Elena Cruz', 41, 'Female', 'elena.cruz@mediconnect.com', '+63 967 890 1234', 'Makati', '', '', 'doctor123', 'doctor'),
                ('Dr. David Wong', 50, 'Male', 'david.wong@mediconnect.com', '+63 978 901 2345', 'Manila', '', '', 'doctor123', 'doctor'),
                ('Dr. Anna Reyes', 37, 'Female', 'anna.reyes@mediconnect.com', '+63 989 012 3456', 'Cebu', '', '', 'doctor123', 'doctor'),
                ('Dr. Carlos Mendoza', 44, 'Male', 'carlos.mendoza@mediconnect.com', '+63 990 123 4567', 'Davao', '', '', 'doctor123', 'doctor'),
                ('Dr. Fatima Al-Sayed', 52, 'Female', 'fatima.alsayed@mediconnect.com', '+63 901 234 5678', 'Quezon City', '', '', 'doctor123', 'doctor')
            ]

            cursor.executemany('''
                INSERT INTO users (full_name, age, gender, email, phone, location, emergency_contact, medical_history, password, role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', doctor_users_data)

        conn.commit()
        conn.close()

    # User management methods
    def create_user(self, user_data):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (full_name, age, gender, email, phone, location, emergency_contact, medical_history, password, role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['full_name'],
                user_data['age'],
                user_data['gender'],
                user_data['email'],
                user_data.get('phone'),
                user_data['location'],
                user_data.get('emergency_contact'),
                user_data.get('medical_history'),
                user_data['password'],
                user_data.get('role', 'patient')
            ))

            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None  # Email already exists
        finally:
            conn.close()

    def authenticate_user(self, email, password):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, full_name, age, gender, email, phone, location, emergency_contact, medical_history, role
            FROM users WHERE email = ? AND password = ?
        ''', (email, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            # Update last login
            self.update_last_login(user[0])
            return {
                'id': user[0],
                'full_name': user[1],
                'age': user[2],
                'gender': user[3],
                'email': user[4],
                'phone': user[5],
                'location': user[6],
                'emergency_contact': user[7],
                'medical_history': user[8],
                'role': user[9]
            }
        return None

    def update_last_login(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

    def update_user(self, user_id, user_data):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users SET
                full_name = ?, age = ?, gender = ?, email = ?, phone = ?,
                location = ?, emergency_contact = ?, medical_history = ?
            WHERE id = ?
        ''', (
            user_data['full_name'],
            user_data['age'],
            user_data['gender'],
            user_data['email'],
            user_data.get('phone'),
            user_data['location'],
            user_data.get('emergency_contact'),
            user_data.get('medical_history'),
            user_id
        ))

        conn.commit()
        conn.close()

    def get_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        users = cursor.fetchall()
        conn.close()

        return users

    def delete_user(self, user_id):
        """Delete a user and all related records"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Delete related records first (cascade delete)
            # Delete symptom analyses
            cursor.execute('DELETE FROM symptom_analyses WHERE patient_id = ?', (user_id,))
            
            # Delete appointments
            cursor.execute('DELETE FROM appointments WHERE patient_id = ?', (user_id,))
            
            # Delete the user
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            return False

    # Doctor management methods
    def get_all_doctors(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM doctors ORDER BY name')
        doctors = cursor.fetchall()
        conn.close()

        # Convert to dict format for compatibility
        doctor_list = []
        for doc in doctors:
            doctor_list.append({
                'id': doc[0],
                'name': doc[1],
                'specialty': doc[2],
                'rating': doc[3],
                'status': doc[4],
                'experience': doc[5],
                'location': doc[6],
                'languages': doc[7].split(',') if doc[7] else [],
                'consultation_fee': doc[8],
                'available': bool(doc[9])
            })

        return doctor_list

    def update_doctor_status(self, doctor_id, status, available):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('UPDATE doctors SET status = ?, available = ? WHERE id = ?',
                      (status, available, doctor_id))

        conn.commit()
        conn.close()

    def add_doctor(self, doctor_data):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO doctors (name, specialty, rating, status, experience, location, languages, consultation_fee, available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            doctor_data['name'],
            doctor_data['specialty'],
            doctor_data['rating'],
            doctor_data['status'],
            doctor_data['experience'],
            doctor_data['location'],
            ','.join(doctor_data['languages']),
            doctor_data['consultation_fee'],
            doctor_data['available']
        ))

        doctor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return doctor_id

    def update_doctor(self, doctor_id, doctor_data):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE doctors SET
                name = ?, specialty = ?, experience = ?, location = ?,
                languages = ?, consultation_fee = ?, status = ?, available = ?
            WHERE id = ?
        ''', (
            doctor_data['name'],
            doctor_data['specialty'],
            doctor_data['experience'],
            doctor_data['location'],
            ','.join(doctor_data['languages']),
            doctor_data['consultation_fee'],
            doctor_data['status'],
            doctor_data['available'],
            doctor_id
        ))

        conn.commit()
        conn.close()

    # Appointment management methods
    def create_appointment(self, patient_id, doctor_id, appointment_date, appointment_time, reason="", notes=""):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (patient_id, doctor_id, appointment_date, appointment_time, reason, notes))

        appointment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return appointment_id

    def get_user_appointments(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT a.*, d.name as doctor_name, d.specialty
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.patient_id = ?
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        ''', (user_id,))

        appointments = cursor.fetchall()
        conn.close()

        return appointments

    def get_all_appointments(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT a.*, u.full_name as patient_name, d.name as doctor_name, d.specialty
            FROM appointments a
            JOIN users u ON a.patient_id = u.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        ''')

        appointments = cursor.fetchall()
        conn.close()

        return appointments

    def update_appointment_status(self, appointment_id, status):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('UPDATE appointments SET status = ? WHERE id = ?', (status, appointment_id))

        conn.commit()
        conn.close()

    # Symptom analysis methods
    def add_symptom_analysis(self, patient_id, symptoms, analysis):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO symptom_analyses (patient_id, symptoms, analysis)
            VALUES (?, ?, ?)
        ''', (patient_id, symptoms, analysis))

        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return analysis_id

    def get_user_analyses(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM symptom_analyses WHERE patient_id = ? ORDER BY timestamp DESC', (user_id,))

        analyses = cursor.fetchall()
        conn.close()

        return analyses

    def get_all_symptom_analyses_with_patients(self):
        """Get all symptom analyses with patient information for admin"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT sa.id, sa.patient_id, sa.symptoms, sa.analysis, sa.timestamp,
                   u.full_name, u.age, u.gender, u.email
            FROM symptom_analyses sa
            JOIN users u ON sa.patient_id = u.id
            ORDER BY sa.timestamp DESC
        ''')

        analyses = cursor.fetchall()
        conn.close()

        return analyses

    def get_symptom_analytics_data(self):
        """Get symptom analysis data with patient demographics for analytics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT sa.id, sa.symptoms, sa.analysis, sa.timestamp,
                   u.age, u.gender
            FROM symptom_analyses sa
            JOIN users u ON sa.patient_id = u.id
            ORDER BY sa.timestamp DESC
        ''')

        analyses = cursor.fetchall()
        conn.close()

        return analyses

    # Analytics methods
    def get_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get various stats
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]

        # Get active today (users who logged in today)
        cursor.execute('SELECT COUNT(*) FROM users WHERE DATE(last_login) = DATE("now")')
        active_today = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM doctors WHERE available = 1')
        available_doctors = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM appointments')
        total_appointments = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM symptom_analyses')
        total_analyses = cursor.fetchone()[0]

        conn.close()

        return {
            'total_users': total_users,
            'active_today': active_today,
            'available_doctors': available_doctors,
            'total_appointments': total_appointments,
            'total_analyses': total_analyses
        }
