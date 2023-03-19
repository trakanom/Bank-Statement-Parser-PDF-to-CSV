import re
param_dict = {
    "Wells Fargo":{
        "columns":['Date','Check Number', 'Description', 'Deposits/Credits', 'Withdrawals/Debits', 'Ending daily balance'],
        "checksum_cols":['Deposits/Credits', 'Withdrawals/Debits', 'Ending daily balance'],
        "col_dims":[x*72 for x in [1.35,2.03,5.26, 6.26, 7.19]],
        "dims":{'top':1.64*72,'left':.8*72, 'right':7.9*72, 'bottom':9.78*72},
        "extra_pages":[1,-2], #left and right boundaries of useful tables
        'account_check': lambda x: x[0][0][0],
        'account_match': "Initiate Business Checking SM", #Testing variable
        'account_number': lambda x:  re.search(re.compile(r'Account number\:(\d{8})'), x).group(1), #might need a map function here.
        'statement_period': None, # regex to locate the date of statement. TBD
    },
    #
    # "Ally":{
    #     "columns":[None, None, None],
    #     "checksum_cols":[None, None],
    #     "col_dims":[x*72 for x in [None, None, None]],
    #     "dims":{'top':None,'left':None, 'right':None, 'bottom':None},
    #     "extra_pages":[None, None],
    #     'account_check': lambda x: x[0][0][0],
    #     'account_match': None,
    #     'account_number': lambda x:  re.search(re.compile(r'Account number\:(\d{8})'), x).group(1), #might need a map function here.
    #     'statement_period': None,
    # },
    # "Capital One":{
    #     "columns":[None, None, None],
    #     "checksum_cols":[None, None],
    #     "col_dims":[x*72 for x in [None, None, None]],
    #     "dims":{'top':None,'left':None, 'right':None, 'bottom':None},
    #     "extra_pages":[None, None],
    #     'account_check': lambda x: x[0][0][0],
    #     'account_match': None,
    #     'account_number': lambda x:  re.search(re.compile(r'Account number\:(\d{8})'), x).group(1), #might need a map function here.
    #     'statement_period': None,
    # },
    # "USAA":{
    #     "columns":[None, None, None],
    #     "checksum_cols":[None, None],
    #     "col_dims":[x*72 for x in [None, None, None]],
    #     "dims":{'top':None,'left':None, 'right':None, 'bottom':None},
    #     "extra_pages":[None, None],
    #     'account_check': lambda x: x[0][0][0],
    #     'account_match': None,
    #     'account_number': lambda x:  re.search(re.compile(r'Account number\:(\d{8})'), x).group(1), #might need a map function here.
    #     'statement_period': None,
    # },
    
}
