import chatbot
from chatbot.load_templates import Load_templates

#example usage
instance = Load_templates()
print(instance.template_files)

#example usage
instance = Load_templates(language="de")
print(instance.template_files)

#example usage
"""
instance = Load_templates(main_folder,language="en")
print(instance.template_files)

instance = Load_templates(main_folder)
print(instance.template_files)
"""