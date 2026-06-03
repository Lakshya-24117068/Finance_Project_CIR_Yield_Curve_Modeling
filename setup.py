from setuptools import setup, find_packages

setup(
    name="Finance_Project_CIR_Yield_Curve_Modeling",
    version="0.1.0",
    author="Lakshya-24117068",
    description="Stochastic Interest Rate Modelling and Prediction using the Cox-Ingersoll-Ross (CIR) Model",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.23.0",
        "pandas>=1.5.0",
        "scipy>=1.9.0",
        "scikit-learn>=1.1.0",
        "matplotlib>=3.6.0",
    ],
    python_requires=">=3.8",
)
