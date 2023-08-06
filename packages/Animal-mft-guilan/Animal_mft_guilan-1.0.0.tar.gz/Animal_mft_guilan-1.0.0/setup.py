import setuptools

setuptools.setup(
    name="Animal_mft_guilan",
    version="1.0.0",
    long_description=open("README.md").read(),
    packages=setuptools.find_packages(exclude=["Quiz 1.py", "Quiz 2(Midterm).py", "Quiz 3.py", "Quiz 4(Final).py"])
)