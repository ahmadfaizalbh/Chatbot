import os
from jinja2 import Template

class Load_templates:
    def __init__(self, local_folder_path="/workspaces/Chatbot/chatbot/local", main_folder=None, language=None):
        self.template_files = self.load_from_folder(local_folder_path, main_folder, language)

    def load_from_folder(self, local_folder_path, main_folder=None, language=None):
        if main_folder:
            folder_path = main_folder
        else:
            folder_path = local_folder_path

        if language:
            folder = os.path.join(folder_path, language)
            template_files = {}
            for file_name in os.listdir(folder):
                if file_name.endswith('.template'):
                    file_path = os.path.join(folder, file_name)
                    with open(file_path, 'r') as f:
                        template_content = f.read()
                        template_files[language] = template_content
            return template_files
        else:
            template_files = {}
            for directory in os.listdir(folder_path):
                directory_path=os.path.join(folder_path,directory)
                for file_name in os.listdir(directory_path):
                    if file_name.endswith('.template'):
                        file_path = os.path.join(directory_path, file_name)
                        with open(file_path, 'r') as f:
                            template_content = f.read()
                            template_files[directory] = template_content
            return template_files

"""
# Example usage
instance = Chat()
print(instance.template_files)

instance = Chat(language="de")
print(instance.template_files)

instance = Chat(main_folder = "path/to/main/folder")
print(instance.template_files)

instance = Chat(main_folder = "path/to/main/folder",language="de")
print(instance.template_files)
"""