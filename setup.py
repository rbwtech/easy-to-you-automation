"""
Setup script for easy-to-you-automation package
"""

from setuptools import setup, find_packages
import os

# Read README file
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Professional IonicCube decoder using easytoyou.eu with enhanced performance and reliability"

# Read requirements
requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
try:
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    requirements = [
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.0',
        'lxml>=4.9.3',
    ]

setup(
    name="easy-to-you-automation",
    version="2.0.0",
    author="RBW-Tech",
    author_email="radipta111@gmail.com",
    description="Professional IonicCube decoder using easytoyou.eu with enhanced performance and reliability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rbwtech/easy-to-you-automation",
    project_urls={
        "Bug Tracker": "https://github.com/rbwtech/easy-to-you-automation/issues",
        "Documentation": "https://github.com/rbwtech/easy-to-you-automation/blob/main/README.md",
        "Source Code": "https://github.com/rbwtech/easy-to-you-automation",
        "Homepage": "https://triatech.net",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "Topic :: Security :: Cryptography", 
        "Topic :: System :: Archiving",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ]
    },
    entry_points={
        "console_scripts": [
            "easy-to-you=easytoyou.cli:main",
        ],
    },
    keywords=[
        "ioncube", "decoder", "php", "encryption", "decryption", 
        "easytoyou", "automation", "batch-processing", "web-scraping"
    ],
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    platforms=["any"],
)
