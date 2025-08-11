This is a prototype of a full-stack URL Shortener application, using FastAPI and
React.

🔧 Setup: Ensure you have Node.js and Python installed Clone the repo: git clone
https://github.com/georgemarsh1809/URLShortener For the Back End: From the root
directory, navigate to the backend folder: cd backend Create and activate
virtual environment: Create: (On Mac) python3 -m venv .venv (on Windows, change
python3 to python) Activate: source .venv/bin/activate (on Windows,
.venv\Scripts\activate) Install dependencies: pip3 install -r requirements.txt
(may have to change pip3 to pip on Windows) Run the FastAPI server: uvicorn
main:app --reload It should be available at: http://localhost:8000 For the Front
End: From the root directory, navigate to the frontend folder: cd frontend In
/frontend/, run npm i to install all necessary dependencies Then, run npm run
dev to start the React app. Open the prompted URL to check the FE renders. It
should run on: http://localhost:5173 (or similar, depending on Vite config) 🧪
To Run The Tests: Make sure you have pytest, httpx (v0.24.1), and fastapi
installed. They should have installed when you ran pip3 install -r
requirements.txt. If not, run: pip3 install fastapi pytest httpx==0.24.1
Navigate to the backend folder: cd backend Simply run: pytest
