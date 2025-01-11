from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="orion_interview",
    version="0.1.0",
    description="A simple forum project with FastAPI backend and Streamlit frontend",
    author="Alexandru Necula",
    packages=find_packages(where="orion_interview"),
    package_dir={"": "orion_interview"},
    install_requires=requirements,
)
