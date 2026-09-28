from .BaseController import BaseController
from fastapi import UploadFile
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    # Create and return the project-specific folder that stores all uploaded files.
    def get_project_path(self,project_id:str):
          project_dir = os.path.join(self.files_dir, project_id)
          
          if not os.path.exists(project_dir):
              os.makedirs(project_dir)
          return project_dir
