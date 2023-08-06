from setuptools import setup


setup(
    name='vault_sync',
    version='0.1.0',
    description='Synchronization for Hashicorp vault key-value stores',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "hvac",
        "pydantic",
        "click",
    ],
    tests_require=[
        "coveralls",
        "flake8"
        "flake8-html",
        "pytest",
        "pytest-cov",
    ],
    url='https://gitlab.com/solvinity/vault-sync',
    author='Vincent van Beek',
    author_email='shared-services@solvinity.com',
    license="MIT",
    package_data={},
    packages=['vault_sync'],
    scripts=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Libraries",
    ],
    test_suite="tests",
    zip_safe=True,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'vault-sync = vault_sync.vault_sync:main',
        ],
    },
)
