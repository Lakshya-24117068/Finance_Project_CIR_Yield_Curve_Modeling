# Yield curve maturity tenors mapped to names and years
MATURITIES_MAP = {
    'ZC025YR': 0.25,   # 3 Months
    'ZC050YR': 0.50,   # 6 Months
    'ZC075YR': 0.75,   # 9 Months
    'ZC100YR': 1.00,   # 1 Year
    'ZC200YR': 2.00,   # 2 Years
    'ZC500YR': 5.00,   # 5 Years
    'ZC1000YR': 10.00, # 10 Years
    'ZC2000YR': 20.00, # 20 Years
    'ZC3000YR': 30.00  # 30 Years
}

TENORS = list(MATURITIES_MAP.keys())
MATURITY_YEARS = list(MATURITIES_MAP.values())
SHORT_RATE_PROXY = 'ZC025YR'
