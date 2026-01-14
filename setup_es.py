import shutil
import os

# Define source and destination
source_dir = r"c:\Users\FernandoLopez-Martin\Documents\build_with_Claude"
dest_dir = os.path.join(source_dir, "es")

# Directories and files to copy
dirs_to_copy = ["modules", "exercises", "projects"]
files_to_copy = ["README.md", "QUICKSTART.md", "MISSING_CONTENT_REPORT.md", "context.md"]

def setup_spanish_course():
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created directory: {dest_dir}")
    else:
        print(f"Directory already exists: {dest_dir}")

    # Copy directories
    for d in dirs_to_copy:
        src = os.path.join(source_dir, d)
        dst = os.path.join(dest_dir, d)
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst) # Clean start to ensure exact copy
            shutil.copytree(src, dst)
            print(f"Copied directory: {d} -> es/{d}")
        else:
            print(f"Warning: Source directory not found: {d}")

    # Copy files
    for f in files_to_copy:
        src = os.path.join(source_dir, f)
        dst = os.path.join(dest_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied file: {f} -> es/{f}")
        else:
            print(f"Warning: Source file not found: {f}")

if __name__ == "__main__":
    setup_spanish_course()
