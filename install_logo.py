import shutil, os

src  = os.path.join(os.getcwd(), "fast_movie_logo.png")
dest = os.path.join(os.getcwd(), "logo.png")

if not os.path.exists(src):
    print(f"❌ Source logo not found: {src}")
    exit()

shutil.copy2(src, dest)
print(f"Logo installed successfully → {dest}")
print("Refresh your browser to see the new logo!")
