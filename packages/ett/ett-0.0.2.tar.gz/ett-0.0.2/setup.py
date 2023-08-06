from setuptools import setup, find_packages
import ett

requirements = [
    'pynvml>=11.4.1'
]

setup(
    name='ett',
    version=ett.__version__,
    python_requires='>=3.6',
    author='ETT Developers',
    author_email='wellshark.net@gmail.com',
    description='Efficient Torch Tools',
    license='MIT-0',
    url='https://pypi.org/project/ett/',
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)