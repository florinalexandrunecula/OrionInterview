import subprocess
import os

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    testing_dir = os.path.join(current_dir, "testing")

    subprocess.run(["pytest", testing_dir])
    