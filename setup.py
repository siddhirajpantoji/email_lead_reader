from setuptools import setup, find_packages

setup(
    name="email_lead_reader",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'lead-reader=email_lead_reader.main:main'
        ],
    },
)