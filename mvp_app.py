# MVP

import numpy as np
import tabula as tb
import pandas as pd
import os
import re,string
import sys
from dateutil.parser import parse
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


class Parser:
    def __init__(self,working_dir=None,debug=None):
        self.debug = debug if debug is not None else False
        self.working_dir = 'data\\' if working_dir is None else working_dir
    def update_from_local(self,file_path,data=None, debug=False):
    
        try:
            info_page = tb.read_pdf(
                file_path,
                stream=True,
                guess=False,
                pages='all',
                multiple_tables=True,
                pandas_options={
                    'header':None},
                silent=True
                )
            print(data['col_dims'])
            print('INFO LENGTH=',len(info_page))
            scan_min_offset = data['extra_pages'][0] + 1
            scan_max_offset = data['extra_pages'][1] + len(info_page)
            scan_range = list(range(scan_min_offset,scan_max_offset))
            
            print(scan_range)
            txn_list = tb.read_pdf(
                file_path,
                stream=True,
                guess=True,
                pages=scan_range,
                multiple_tables=True, 
                area=data['dims'][0],
                columns = data['col_dims'],
                pandas_options={
                    'header':None},
                silent=True
                )
        except Exception as e:
            print('The Error is',e)

        account = info_page[0][0][0]
        txns_df = txn_list
        account_number_filter = re.compile(r'Account number\:(\d{8})')
        for index,entry in info_page[0].iterrows():
            print(index, entry[0])
            account_check = re.search(account_number_filter, str(entry[0]))
            if account_check!=None:
                account_number = account_check.group(1)
                break
        
        print("ACCOUNT NUMBER", account_number)
        
        
        currency_filter = re.compile(r'\$?((\d{0,3},?)+)?\d{1,3}\.\d{2}')
        if account=="Initiate Business Checking SM": 
            description_col = data['columns'].index('Description')

            for df in txns_df:
                broken_rows = []
                for index,row in df.iterrows(): #removing row spillover and merging description into the previous row's entry
                    row_strikes = 0
                    if row[3:].isna().sum()>=3 and row[description_col]!="NaN":
                        try:
                            if debug|self.debug==True:
                                print(f"This is row {index}:\n{row}")
                                print("Prev descript",prev_description)
                                print("New description", new_descript)
                                ...
                            if df.iloc[index-1].isna().sum()==3:
                                prev_description = df.iloc[index-1][description_col]
                                new_descript = prev_description + " " + row[description_col]
                                df.iloc[index-1][description_col]=new_descript
                            broken_rows.append(index)
                        except:
                            broken_rows.append(index)
                    else: #cleaning paragraph text encountered in scraping
                        for col_num, col in enumerate(row[3:]):
                            if pd.isnull(df.iloc[index,col_num+3])==False:
                                print(col, re.match(currency_filter, str(col)))
                                
                                if re.match(currency_filter, str(col))==None:
                                    row_strikes+=1
                                    if row_strikes>=1:
                                        print(f"removing df[{index}]=\n{row}")
                                        broken_rows.append(index)
                                        break

                
                df.drop(broken_rows, inplace=True)
        else:
            print(account)
            
        
        new_txns_df = pd.concat(txns_df,axis=0, ignore_index=True).reindex() #compiling entire statement into a DF
        new_txns_df.replace(",|$","", regex=True, inplace=True) #cleaning format
        new_txns_df.columns=data['columns'] #adding column names
        
        Total_entry = new_txns_df.loc[new_txns_df['Date']=='Totals'] #extracting metadata for the Totals entries
        Final_entry = new_txns_df.loc[new_txns_df['Date'].str.contains("Ending")] #extracting metadata for the statement period and final account balance
        
        new_txns_df.drop([Total_entry.index[0], Final_entry.index[0]], inplace=True) #removing the rows extracted above
        
        print("TOTAL ENTRY",Total_entry, Final_entry)
        
        
        
        date_filter = re.compile(r'(\d{1,2}\/\d{2})')
        statement_end = re.search(date_filter, Final_entry.values[0][1]).group(1)
        
        
        metadata = {column_name:float(str(Total_entry[column_name].array[0])) for column_name in data['columns'][3:]} #Adding checksum values to dict
        metadata.update({
            "Account Number":account_number,
            "Account":account, 
            "Institution":None, #tbd
            data['columns'][-1]:float(Final_entry.values[0][-1]), #final account balance for checksums
            "Statement_Period":statement_end, 
            "Entries":len(new_txns_df)-1,
        })
        
        
        # metadata = {
        #     "Ending_Balance":ending_balance,
        #     "Totals":col_totals,
        # }

        
        
        print("FOUND\n", metadata)
        # new_txns_df.drop()
        # new_txns_df.concat(txns_df)
        if self.validate(metadata, new_txns_df):
            return metadata, new_txns_df
        else:
            print("ERROR")
            return None, None
            # print(df_list)
    def validate(self, metadata, df):
        metadata = metadata
        cols_to_not_check = ['Ending daily balance','Statement_Period','Account','Entries','Account Number']
        cols_to_check = [cols for cols in metadata.keys() if cols not in cols_to_not_check]
        print("CHECKSUM", cols_to_check)
        for col in cols_to_check:
            if df[col].astype('float').sum()==metadata[col]:
                print("PASS")
            else:
                return False
        # print(df[3:])
        return True

if __name__ == '__main__':
    test_file1 = "WF OffChk 12-31-21 Stmt.pdf"
    test_file2 = "CapOne Statement_122021_0612.pdf"
    working_dir = "test_data\\"
    input_dir = working_dir+"input\\"
    test_file_dir = input_dir+test_file1
    output_dir = working_dir+"output\\"
    
    p = Parser(working_dir=working_dir, debug=True)
    
    
    
    wf_data = {
    "columns":['Date','Check Number', 'Description', 'Deposits/Credits', 'Withdrawals/Debits', 'Ending daily balance'],
    "col_dims":[x*72 for x in [1.35,2.03,5.26, 6.26, 7.19]],
    "dims":[{'top':1.64*72,'left':.8*72, 'right':7.9*72, 'bottom':9.78*72}],
    "extra_pages":[1,-2] #left and right boundaries of useful tables
}
    cap_data = {
    "columns":['Trans Date','Post Date', 'Description', 'Amount'],
    "dims":{'top':40,'left':10, 'right':212, 'bottom':260}
}
    metadata, results = p.update_from_local(test_file_dir,data=wf_data)
    # account,results = p.update_from_local(input_dir+test_file2, data=cap_data)
    print("\n\n\n\n\n", metadata['Account'], metadata['Entries'], results, sep='\nNEWTABLE\n')
    # results = results
    
    # for n,results in enumerate(results):
    results.to_csv(output_dir+"{}.csv".format(metadata['Account'].replace(" ","_")))
