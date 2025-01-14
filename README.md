# ATTENDO Smart Classroom Management System

## Overview
The Smart Classroom Management System is a cloud-based web application designed to enhance classroom operations by enabling seamless client-host connections and QR-based attendance systems. This lightweight version focuses specifically on enabling teachers to log into smart devices and take attendance efficiently.

---

## Features
- **QR-Based Authentication:** Teachers can log in to smart board devices using dynamically generated QR codes.
- **QR-Based Attendance:** Teachers can generate a QR code for students to scan and mark their attendance. Anti-proxy mechanisms ensure only valid devices are used.
- **Real-Time Notifications:** Supports WebSocket-based notifications for updates such as attendance confirmation.

---

## Tech Stack
### Frontend
- **React**: For building a responsive and interactive user interface.
- **JavaScript**: Core logic and client-side scripting.
- **HTML5 & CSS3**: For semantic structure and design.

### Backend
- **Django**: Web framework for handling server-side logic and APIs.
- **Django REST Framework (DRF)**: For building robust RESTful APIs.
- **Redis**: Caching and session management.
- **WebSockets**: Real-time communication between clients and server.

### Database
- **PostgreSQL**: Relational database management system.

---

## System Architecture
### Key Strategies
1. **QR Code Authentication**:
   - Dynamic QR codes are generated using Django REST Framework.
   - QR codes expire after a short duration for enhanced security.

2. **Proxy Avoidance in Attendance**:
   - Device-specific identifiers logged for students to ensure one attendance per device within a 5-minute window.
   - Redis used for session caching and cooldown tracking.

3. **WebSocket Integration**:
   - For real-time notifications and updates, e.g., confirming login or attendance success.

---

## Setup Instructions

### Prerequisites
- Python (>= 3.9)
- Node.js (>= 16.x)
- PostgreSQL

### Steps
1. Clone the Repository:
   ```bash
   git clone https://github.com/your-repo/smart-classroom.git
   cd smart-classroom
   ```

2. Set Up the Backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. Set Up the Frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. Configure PostgreSQL:
   - Update the `DATABASES` settings in `backend/settings.py` with your PostgreSQL credentials.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contributing
We welcome contributions! Please fork the repository and submit a pull request. For major changes, open an issue to discuss proposed changes first.

---

## Contact
For inquiries or support, please contact:
- **Name**:  Fredrick George F
- **Email**:  fredrick.george.f.25@gmail.com
- **GitHub**:  [Fredrick2503](https://github.com/Fredrick2503)


