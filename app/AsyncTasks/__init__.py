
#########################################################################################
# Library include
import pathlib

#########################################################################################

path: str = './app/AsyncTasks/'
path_obj: pathlib.Path = pathlib.Path(path)
list_of_files: list = []

# Getting all file names without .py from the directory
for file in path_obj.iterdir():
    file_name: str = file.name
    if(file_name.endswith('.py') and file_name != '__init__.py'):
        file_name = file_name[:-3]
        list_of_files.append(file_name)


# Import all files
__all__ = list_of_files
