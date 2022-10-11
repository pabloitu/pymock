from setuptools import setup, find_packages


setup(
    name='mockup',                  # Model name
    version='0.1.0',                
    author='Pablo Iturrieta',       
    author_email='pciturri@gfz-potsdam.de',
    license='LICENSE',
    description='Mock-up model for the Italy Experiment',
    install_requires=['numpy==1.21.5', 'matplotlib==3.4.3', 'pytest'],  # << Dependencies
    entry_points={
        # Usage to define a binary entry point:
        # 'console_scripts': [$binary_name = $module:$function]
        'console_scripts': ['run = run:run']
    },
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    url='https://git.gfz-potsdam.de/csep-group/rise_italy_experiment/models/mockup'
)
