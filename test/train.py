import os


print(f"path file is { os.path.abspath(__file__)} ")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
print(f"path file is { os.path.dirname(os.path.dirname(os.path.abspath(__file__)))} ")

print(BASE_DIR)