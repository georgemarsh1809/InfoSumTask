from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
import csv
import io
from fastapi.middleware.cors import CORSMiddleware
from services import is_valid_udprn, key_count, distinct_key_count, get_overlap_count, calculate_overlap_product

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
async def process_csvs(file1: UploadFile = File(...), 
                       file2: UploadFile = File(...), 
                       file1KeyColumn: int = Form(...), 
                       file2KeyColumn: int = Form(...), 
                       delimiter: str = ','):
    
    # Read file contents 
    file1_raw = (await file1.read()).decode("windows-1252")
    file2_raw = (await file2.read()).decode("windows-1252")

     # Parse CSVs
    file1_contents = csv.reader(io.StringIO(file1_raw), delimiter=delimiter)
    file2_contents = csv.reader(io.StringIO(file2_raw), delimiter=delimiter)

    # Skip over CSV field header:
    next(file1_contents, None)
    next(file2_contents, None)

    # Initialise empty key arrays 
    file1_keys = []
    file2_keys = []

    # Iterate over each file and, if the key is valid, add it to the respective array | catch any invalid keys

    for row in file1_contents:
        try:
            key = row[file1KeyColumn - 1].strip()
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Column index {file1KeyColumn} out of range for file1 row: {row}"
            )
        
        # Validate the key format
        if is_valid_udprn(key):
            file1_keys.append(key)

    for row in file2_contents:
        try:
            key = row[file2KeyColumn - 1].strip()
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Column index {file2KeyColumn} out of range for file2 row: {row}"
            )
        
        if is_valid_udprn(key):
            file2_keys.append(key)

    # Parse to the backend services to process the keys and return the required information
    file1_key_count, file2_key_count = key_count(file1_keys, file2_keys)
    file1_distinct_key_count, file2_distinct_key_count = distinct_key_count(file1_keys, file2_keys)
    overlap_count = get_overlap_count(file1_keys, file2_keys)
    overlap_product = calculate_overlap_product(file1_keys, file2_keys)

    return {
        "file1_key_count": file1_key_count,
        "file2_key_count": file2_key_count,
        "file1_distinct_key_count": file1_distinct_key_count,
        "file2_distinct_key_count": file2_distinct_key_count,
        "overlap_count": overlap_count,
        "overlap_product": overlap_product
    }


