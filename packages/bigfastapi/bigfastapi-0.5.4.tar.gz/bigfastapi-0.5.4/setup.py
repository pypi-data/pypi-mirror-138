import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bigfastapi",                     # This is the name of the package
    version="0.5.4",                        # The initial release version
    author="BigFastAPI Team",                     # Full name of the author
    author_email="support@rijen.tech",
    description="Adding lots of functionality to FastAPI",
    long_description=long_description,   
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=['bigfastapi', 
                                                'bigfastapi.schemas', 
                                                'bigfastapi.models',
                                                'bigfastapi.db', 
                                                'bigfastapi.templates', 
                                                'bigfastapi.utils', 
                                                'bigfastapi.data']),  

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],                                  
    python_requires='>=3.9',               
    install_requires=['Jinja2', 'fastapi'],                 
    url='https://bigfastapi.com',
    keywords='fastapi, bigfastapi, auth',
    package_data={
        'bigfastapi': ['templates/*.*'],
        'bigfastapi': ['templates/email/*.*'],
        'bigfastapi': ['data/*.*']
    },
    include_package_data=True,
    project_urls={ 
        'Bug Reports': 'https://github.com/rijentech/bigfastapi',
        'Funding': 'https://bigfastapi.com',
        'Source': 'https://github.com/rijentech/bigfastapi',
    },
)