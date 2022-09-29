from setuptools import setup, find_packages

setup(
    name='mockup',
    version='0.1.0',
    author='Pablo Iturrieta',
    author_email='pciturri@gfz-potsdam.de',
    license='LICENSE',
    description='Mock-up model for the Italy Experiment',
    install_requires=['numpy==1.21.5', 'matplotlib', 'pytest'],  # << Dependencies
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    url='https://git.gfz-potsdam.de/csep-group/rise_italy_experiment/models/mockup'
)
