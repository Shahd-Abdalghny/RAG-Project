from fastapi import FastAPI , APIRouter ,Depends , UploadFile ,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from controllers import DataController ,ProjectController ,ProcessController
from models import ResponseSignal
import aiofiles
import os
import logging
from .schemes.data import ProcessRequest
logger = logging.getLogger("uvicorn.error")

# Data router handles file upload endpoints for project-specific documents.
data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ["api_v1", "data"],
)

data_controller = DataController()

# Upload a file into the project folder and return a generated file identifier.
@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,file: UploadFile
                      , app_settings : Settings = Depends(get_settings)):
        # Step 1: check file extension and byte limit before saving anything.
        is_valid , message = data_controller.validate_uploaded_file(file)
        
        if not is_valid:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": message}
            )
        
        # Step 2: create or access the project folder and prepare a unique storage path.
        project_path = ProjectController().get_project_path(project_id) 
        file_path ,file_id = data_controller.generate_unique_file_path(original_filename=file.filename, project_id=project_id)
        try:
            # Step 3: stream the uploaded file in chunks to avoid loading the full content in memory.
            async with aiofiles.open(file_path, 'wb') as f:
                while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": ResponseSignal.FILE_UPLOAD_FAILED.value}
            )
        
        # Step 4: respond with success information for the uploaded file.
        return JSONResponse(
            content={"message":ResponseSignal.FILE_UPLOAD_SUCCESS.value ,
                     "file_id": file_id
                     }
        )
        
@data_router.post("/process/{project_id}")
async def process_data(project_id: str, process_request: ProcessRequest):
    file_id = process_request.project_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id)
    file_chunks = process_controller.process_file_content(file_content, file_id, chunk_size, overlap_size)
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSignal.PROCESSING_FAILED.value}
        )
        
    # return JSONResponse(
    #     content={"message": ResponseSignal.PROCESSING_SUCCESS.value,
    #                 "chunks": [file_chunk.page_content for file_chunk in file_chunks],
    #                 }
    # )
    return file_chunks

