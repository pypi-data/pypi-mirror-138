from setuptools import setup,find_packages

setup(
    name='megstudio',
    version='0.0.4',
    packages=find_packages(),
    url='https://github.com/pypa/sampleproject',
    license='MIT',
    author='Renyang',
    author_email='renyang@megvii.com',
    description='megstudio package',
    long_description_content_type="text/markdown",
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)