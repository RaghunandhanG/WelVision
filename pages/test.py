import os
directory = r"C:\Users\Raghunandhan G\Desktop\WelVision\models"
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
print(directory)
print(files)