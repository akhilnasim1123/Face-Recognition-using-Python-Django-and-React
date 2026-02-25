# Face Recognition System using Python, Django, and React

This repository contains a full-stack web application designed for Face Recognition. It is built using **React** for the user interface, **Django REST Framework** for the backend API, and **OpenCV** + **Machine Learning** models for the core face recognition capabilities.

## 🚀 Technologies Used

### Frontend
- **React 18:** Component-based UI formulation.
- **PrimeReact, PrimeFlex & PrimeIcons:** UI component library, utility-first CSS framework, and icons.
- **React Router DOM:** Used for seamless client-side routing.
- **Axios:** Handles HTTP requests from the React frontend to the Django backend.
- **SweetAlert2:** Provides customized, beautiful alert dialogs.

### Backend
- **Python 3.x:** Core programming language.
- **Django 4.1:** High-level Python web framework.
- **Django REST Framework (DRF):** A powerful and flexible toolkit for building RESTful APIs.
- **OpenCV (`opencv-python`):** Open-source computer vision library used for processing images and facial recognition.
- **Hugging Face Hub:** Interactions with advanced machine learning models.
- **Django CORS Headers:** Manages Cross-Origin Resource Sharing.

## 📁 Project Structure

```
├── backend/
│   ├── admin_section/          # App for managing administrative operations
│   ├── backend/                # Main Django configuration & settings (core)
│   ├── face_recognition_logic/ # Contains OpenCV and AI models logic for detecting and recognizing faces
│   ├── registration/           # Handles user authentication, management, and registration
│   ├── manage.py               # Django's command-line utility for administrative tasks
│   └── requirements.txt        # Detailed Python dependencies required for the backend
└── frontend/
    ├── public/                 # Static assets (HTML, icons)
    ├── src/                    # React components, contexts, routing and application state
    ├── package.json            # Node.js dependencies and project scripts
    └── README.md               # Standard Create-React-App configuration docs
```

## ⚙️ Setup Instructions

### Backend Setup (Django)

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (Optional but highly recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```
   The backend API will be accessible at `http://127.0.0.1:8000/`.

### Frontend Setup (React)

1. **Open a new terminal and navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   The frontend app will launch in your default browser at `http://localhost:3000/`. It will automatically proxy and communicate with your running Django server.

## 🌟 Key Features
- **Secure Authentication:** Complete registration and login system.
- **Advanced Face Recognition:** Leverages Python and OpenCV to interactively identify faces.
- **Intuitive Dashboard:** A responsive, interactive user interface crafted with PrimeReact.
- **Separation of Concerns:** Clear segmentation between the Frontend UI and Backend Logic.
