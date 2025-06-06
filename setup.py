from setuptools import setup, find_packages

setup(
    name="deepshell",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'langchain-core>=0.1.27',
        'langchain-google-genai>=0.0.11',
        'langchain-groq>=0.0.6',
        'google-ai-generativelanguage>=0.4.0',
        'google-generativeai>=0.3.2',
        'groq>=0.4.2',
        'requests',
        'PyYAML',
        'rich',
        'tqdm'
    ],
    package_data={
        'deepshell': ['*.css', '*.json.template'],
    },
    entry_points={
        'console_scripts': [
            'deepshell=main:main',
        ],
    },
    author="Gokulbarath",
    author_email="Gokul00060@gmail.com",
    description="AI-powered Terminal Copilot for Linux Systems",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gokul6350/DeepShell4",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: GTK",
    ],
) 