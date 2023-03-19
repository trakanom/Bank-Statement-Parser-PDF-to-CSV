'''
Unused code to understand the data structures and variables involved.
'''
Bank_Metadata = {
    "Info_Page":int(), #How many pages of preamble and info pages before transactions show up?
    "Useless_Pages": int(), #How many useless pages are at the end of each PDF?
    "Txn_Pages":[range()], #Range between Info_Page and Useless_Pages. ex: range(Info_Page+1, Page_Count-Useless_Pages)
    'column_title':{ #matches columns names to appropriate variables
        'Date':str(), #Convert to datetime: yyyy-mm-dd
        'Description':str(), #clean column leakage
        'Amount':str(), #clean from string by removing ["$",",","-"]
        'Txn_In':str(),
        'Txn_Out':str(),
        'Ending_Balance':str(),
    },
    'dims':{ #values are in 1/72 of an inch. (Inches * 72)
        'top':float(),
        'left':float(),
        'right':float(),
        'bottom':float(),
    },
    'column_dims':[float() for item in ['column_title']], #right-side borders of columns. (Inches * 72)
}

Txn_Entry ={
    "TxnID":int(),
    "AccountID":int(),
    "Date":str(), #yyyy-mm-dd
    "Type": [type for type in ['debit','credit','transfer','fee','interest']],
    "Description":str(),
    "Amount":float()
}

Statement = {
    "AccountID":int(),
    "Period":int(), #yyyymm
    "Month":int(), #mm
    "Year":int(), #yyyy
    "Transactions":[Txn_Entry],
    "Metadata":{
        'total_in':float(),
        'total_out':float(),
        'ending_balance':float(),
    }
}
