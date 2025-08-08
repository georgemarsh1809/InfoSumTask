from fastapi import FastAPI, UploadFile, File
import csv
import io
from fastapi.middleware.cors import CORSMiddleware
from services import key_count, distinct_key_count, get_overlap, calculate_overlap_product

# Create API server
app = FastAPI() 

# Configure CORS to allow requests from React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/process-csvs/")
async def process_csvs(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # Read file contents 
    file1_raw = (await file1.read()).decode("utf-8")
    file2_raw = (await file2.read()).decode("utf-8")

    # Parse CSVs using csv.reader
    file1_contents = csv.reader(io.StringIO(file1_raw))
    file2_contents = csv.reader(io.StringIO(file2_raw))

    # Skip over CSV field header:
    next(file1_contents, None)
    next(file2_contents, None)

    # Initialise empty key arrays 
    file1_keys = []
    file2_keys = []

    # Iterate over each file and, if its the key is not empty, add it to the respective array 
    for row in file1_contents:
        if row[0] != "":
            file1_keys.append(row[0])

    for row in file2_contents:
        if row[0] != "":
            file2_keys.append(row[0])

    # Parse to the backend services to process the keys and return the required information
    file1_key_count, file2_key_count = key_count(file1_keys, file2_keys)
    file1_distinct_key_count, file2_distinct_key_count = distinct_key_count(file1_keys, file2_keys)
    overlap_count = get_overlap(file1_keys, file2_keys)
    overlap_product = calculate_overlap_product(file1_keys, file2_keys)

    return {
        "file1_key_count": file1_key_count,
        "file2_key_count": file2_key_count,
        "file1_distinct_key_count": file1_distinct_key_count,
        "file2_distinct_key_count": file2_distinct_key_count,
        "overlap_count": overlap_count,
        "overlap_product": overlap_product
    }


