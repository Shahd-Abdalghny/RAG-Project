
from fileinput import filename

from controllers.BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # 1 MB in bytes

    # Validate the uploaded file against the allowed content types and size limits.
    def validate_uploaded_file(self,file:UploadFile):
        
        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False ,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value 
         
        if file.size > self.settings.FILE_MAX_SIZE * self.size_scale:
            return False ,ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True ,ResponseSignal.FILE_VALIDATED_SUCCESS.value

    # Build a unique file path inside the target project folder to avoid overwrites.
    def generate_unique_file_path(self,original_filename:str ,project_id:str):
        random_filename = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        clean_filename = self.get_clean_filename(original_filename)
        new_file_path = os.path.join(project_path, f"{random_filename}_{clean_filename}")
        while os.path.exists(new_file_path):
            random_filename = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{random_filename}_{clean_filename}")
        
        return new_file_path , random_filename

    # Remove unsafe characters from the original file name so it can be saved safely.
    def get_clean_filename(self,orig_file_name:str):
        clean_filename = re.sub(r'[^\w.]', '', orig_file_name.strip())
        clean_filename = clean_filename.replace(" ", "_")  # Replace spaces with underscores
        
        return clean_filename
            