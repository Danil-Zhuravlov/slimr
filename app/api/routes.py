from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO
from ..models.schemas import SaleResponse
from ..processing.data_cleaning import clean_sales_data

# create an router instance to use endpoints in main.py
router = APIRouter()

# endpoint to upload the file with csv data
@router.post("/upload-csv", response_model=SaleResponse)
async def upload_csv(file: UploadFile = File(...)):
    # Validate file extension
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
        
        # Validate required columns
        required_columns = ['date', 'product_id', 'quantity', 'price', 'cost']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Data cleaning
        df = clean_sales_data(df)
        
        # Shows to user what data have we received
        return SaleResponse(
            filename=file.filename,
            row_count=len(df),
            columns=df.columns.tolist(),
            sample_data=df.to_dict('records')
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing CSV file: {str(e)}"
        )
