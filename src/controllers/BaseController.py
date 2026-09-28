
from helpers.config import get_settings
import os
import random 
import string

class BaseController:
    def __init__(self):
        # Load the environment configuration once so all controllers share the same settings.
        self.settings = get_settings()
        # Resolve the project root and the folder where uploaded files are stored.
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets", "files")

    # Generate a random string to create unique file names and avoid collisions.
    def generate_random_string(self, length:int = 12) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))