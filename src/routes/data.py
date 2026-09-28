from fastapi import FastAPI , APIRouter ,Depends , UploadFile ,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from controllers import DataController ,ProjectController
from models import ResponseSignal
import aiofiles
import os
import logging

logger = logging.getLogger("uvicorn.error")


data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ["api_v1", "data"],
)
data_controller = DataController()
@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,file: UploadFile
                      , app_settings : Settings = Depends(get_settings)):
        # validate file type and size
        is_valid , message = data_controller.validate_uploaded_file(file)
        
        if not is_valid:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": message}
            )
        
        # save the file to the project directory
        project_path = ProjectController().get_project_path(project_id) 
        file_path ,file_id = data_controller.generate_unique_file_path(original_filename=file.filename, project_id=project_id)   
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": ResponseSignal.FILE_UPLOAD_FAILED.value}
            )            
        
        return JSONResponse(
            content={"message":ResponseSignal.FILE_UPLOAD_SUCCESS.value ,
                     "file_id": file_id
                     } 
            
            
        )        