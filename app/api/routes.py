from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    # Check if file is CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400, 
            detail="Wrong file format. Please upload a CSV file"
        )
    
    try:
        # Read file content
        contents = await file.read()
        # Convert bytes to string
        csv_string = StringIO(contents.decode())
        # Read CSV into pandas DataFrame
        df = pd.read_csv(csv_string)
        
        return {
            "filename": file.filename,
            "row_count": len(df),
            "columns": df.columns.tolist()
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing CSV file: {str(e)}"
        )
