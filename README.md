This is a prototype of a full-stack URL Shortener application, using FastAPI and
React.

### 🔧 Setup:

1. Ensure you have Node.js and Python installed
2. Clone the repo: `git clone https://github.com/georgemarsh1809/InfoSumTask`
3. For the Back End:
    - From the root directory, navigate to the backend folder: `cd backend`
    - Create and activate virtual environment:
        - Create: (On Mac) `python3 -m venv .venv` (on Windows, change `python3`
          to `python`)
        - Activate: `source .venv/bin/activate` (on Windows,
          `.venv\Scripts\activate`)
    - Install dependencies:
        - `pip3 install -r requirements.txt` (may have to change `pip3` to `pip`
          on Windows)
    - Run the FastAPI server: `uvicorn main:app --reload`

-   It should be available at: http://localhost:8000

4. For the Front End:
    - In a new terminal, from the root directory, navigate to the frontend folder: `cd frontend`
    - In `/frontend/`, run `npm i` to install all necessary dependencies
    - Then, run `npm run dev` to start the React app. Open the prompted URL to
      check the FE renders.

-   It should run on: http://localhost:5173 (or similar, depending on Vite
    config)

##

### 🧪 To Run The Tests:

1. Make sure you have `pytest` and `fastapi` installed. \
   They should have installed when you ran `pip3 install -r requirements.txt`. \
    If not, run: `pip3 install fastapi pytest httpx==0.24.1 `
2. Navigate to the backend folder: \
   `cd backend`
3. Run: `pytest key_tests.py `


### Implementation Notes
#### 📋 Project Requirements :
"The program should perform the following:
- Allow specification of the files to process
- Calculate and display the following:
  - The count of the keys in each file
  - The count of the distinct keys in each file
  - The count of the overlap of distinct keys between the two files (distinct overlap)
  - The product of the overlap of all keys between the files (overlap product)
- Overlap Product is defined as the sum of the products of the overlapping keys, 
- e.g.
  - Dataset 1: A B C D D E F F
  - Dataset 2: A C C D F F F X Y
  - Distinct Overlap = A C D F = 4
  - Overlap Product = A C C D D F F F F F F = 11"

#### 🛠️ Tech:

-   I built the solution to the initial logic in Python, then I used FastAPI to implement a REST API that would serve the data to the UI
-   I built a simple UI using React as a way to more easily demo the features of the solution, and to highlight my proficiency with JavaScript/HTML/CSS.

####  🧠 My Approach 
- I started this project by creating some simple User Stories which helped me split up the requirements of the task:
  - US1: As a user,\
  I want to be able to upload 2 CSV files,  
  so they can be processed to produce the desired metrics.
  - US2: As a user, I want to be able to find out the following info about the CSVs: \
    - The count of the keys in each file
    - The count of distinct keys in each file
    - The count of the overlap of keys (intersection)
    - The overlap product of the keys intersection
- I then wrote a Python function for each metric defined in the requirements. This didn't take too long, and I got every function generating the required result pretty quickly, but I noticed the function to generate the overlap product was very slow.
I researched some faster ways to loop over intersections and discovered the Counter method in the `collections` module. The explanation for why this is so much faster can be found in the code comments.
- Once I was happy with the logic I wanted to implement a better way to specify the CSV files and demo the features,  so I created a simple REST API with FastAPI, and split the logic out into a `services` file. I then created a simple React UI which hits the API I built, triggering the backend services and performing the logic on the provided CSVs.
- As a way to validate the above requirements were met, I also used Pytest to create some simple Unit Tests for each function. With this, I assert that only valid keys are processed, and by using basic sample data, that each function returns the expected metric.

#### 💭 Assumptions:
-  Keys that are missing ("", in the CSVs), are to be ignored and not counted in the final calculations.


