from datetime import datetime as dt
from operator import concat
from sre_parse import expand_template
import pandas as pd
import numpy as np
import tabula as tb
import re
import os
from CONFIG import param_dict


class BankInfo:
    def __init__(self, bank_name):
        self.name = bank_name
        self.metadata = param_dict[bank_name]
        self.columns = self.metadata["columns"]
        self.dims = self.metadata["dims"]
        self.col_dims = self.metadata["col_dims"]
        self.extra_pages = self.metadata["extra_pages"]
        self.account_check = self.metadata["account_check"]
        self.account_match = self.metadata["account_match"]
        self.account_number = self.metadata["account_number"]
        self.statement_period = self.metadata["statement_period"]

    def get_meta(self):
        return self.metadata

    def check_account(self, file_df):

        # print(file_df)
        print(
            "Checking account",
            self.account_check(file_df),
            self.account_match,
            self.account_check(file_df) == self.account_match,
        )
        return self.account_check(file_df) == self.account_match

    def get_account_number(self, file_df):
        print("Getting account number")
        for index, row in file_df.iterrows():
            for entry in row:
                try:
                    account_number = self.account_number(entry)
                    print(account_number)
                    return self.account_number(file_df)
                except:
                    pass

    def get_period(self, file_df):
        print("Getting statement period")
        return None
        return self.statement_period(file_df)

    def clean(self, file_df, metadata_dict):
        return file_df, metadata_dict


class Parser:
    def __init__(self, working_dir=None, debug=None):
        """
        Initialize databases, buckets, etc.
        """
        ...
        self.working_dir = "data\\" if working_dir == None else working_dir
        self.debug = False if debug is None else debug
        self.transactions = pd.DataFrame(
            columns=["date", "account", "description", "amount"]
        )
        self.read_files = set()
        self.banks = {}

        if self.debug:
            print(f"Class Initialized at {dt.now()}")

    def add_bank(self, bank_obj):
        self.banks[bank_obj.name] = bank_obj

    def add_banks(self, bank_obj_iter):
        for bank in bank_obj_iter:
            self.add_bank(bank)

    def update_local(self, input_dir=None):
        """
        Control function.
        Scans an input directory and loads parsed data to the database.
        Load -> Classify -> Parse -> Clean -> Transform -> Load -> Export
        """
        input_dir = self.working_dir + "input\\" if input_dir == None else input_dir
        file_list = os.listdir(input_dir)
        for file_name in file_list:
            file_path = input_dir + file_name
            statement_metadata = self.classify_statement(
                file_path
            )  # classify the statement
            statement_data = self.parse_txns(
                file_path, statement_metadata
            )  # get raw transactions
            cleaned_data, more_statement_metadata = self.clean_inputs(
                statement_data, statement_metadata
            )  # clean, gather checksum data
            statement_metadata.update(
                more_statement_metadata
            )  # add checksum data to metadata
            validated_data = self.validate_data(
                cleaned_data, statement_metadata
            )  # validate against checksums

            if statement_metadata["valid"] == True:
                self.load_db(validated_data)  # load db
            else:
                print(f"Data validation error for {file_path}")
        # export

    def classify_statement(self, file_path):  # Classify.  file_name --> return metadata
        """
        Input: file_path
        Output: bank, account number, statement period, file_path, page_count

        """
        # load file
        # parse with Guess=True
        # use identification rules to determine which bank the statement is for

        info_page = tb.read_pdf(
            file_path,
            stream=True,
            guess=False,
            pages="all",
            multiple_tables=True,
            pandas_options={"header": None},
            silent=True,
        )

        matching_bank = None
        for bank in self.banks.keys():
            if self.banks[bank].check_account(info_page):
                matching_bank = self.banks[bank]
                break

        if matching_bank == None:
            statement_metadata = {"Error": "No matching bank", "file_path": file_path}
        else:
            account_number = matching_bank.get_account_number(info_page[0])
            statement_period = matching_bank.get_period(info_page[0])
            page_count = len(info_page)
            statement_metadata = {
                "bank": matching_bank,
                "accountID": account_number,
                "page_count": page_count,
                "statement_period": statement_period,
                "file_path": file_path,
            }
        return statement_metadata

    def parse_txns(self, file_path, statement_metadata):  # Parse
        print("Parsing transactions", file_path, statement_metadata)
        scan_min_offset = statement_metadata["bank"].extra_pages[0] + 1
        scan_max_offset = (
            statement_metadata["page_count"] + statement_metadata["bank"].extra_pages[1]
        )
        scan_range = list(range(scan_min_offset, scan_max_offset))
        print(statement_metadata["bank"].dims, statement_metadata["bank"].col_dims)
        txn_list = tb.read_pdf(
            file_path,
            stream=True,
            guess=True,
            pages=scan_range,
            multiple_tables=True,
            area=statement_metadata["bank"].dims,
            columns=statement_metadata["bank"].col_dims,
            pandas_options={"header": None},
            silent=False,
        )
        txn_all = pd.concat(txn_list)
        # txn_list.columns = statement_metadata['bank'].columns
        return txn_list

    def clean_inputs(self, statement_data, statement_metadata):  # Clean
        ...
        # tbd
        # standard cleaning
        # clean up rows by appending spillover to previous line (descriptions only)
        # standardize date format
        # remove extra symbols (spillover, currency formatting)
        # specialized cleaning and extracting of checksum data
        cleaned_data, checksum_data = statement_metadata["bank"].clean(
            statement_data, statement_metadata
        )  # tbd

        return cleaned_data, checksum_data

    def validate_data(self, cleaned_data, statement_metadata):
        statement_metadata.update({"valid": True})
        return cleaned_data, statement_metadata

    def load_db(self, validated_data):
        # tbd:
        pd.merge(self.transactions, validated_data, how="outer", on="date")  # tbd

    def export_csv(self, output_path=None, period=None):
        # tbd:
        output_df = self.transactions.query(
            f"{period[0]}<= date <= {period[1]}", engine="python"
        )  # tbd
        output_df.to_csv(output_path)


if __name__ == "__main__":
    # For testing:
    p = Parser(working_dir="test_data\\", debug=True)
    USAA = BankInfo("USAA")
    WF = BankInfo("Wells Fargo")
    Ally = BankInfo("Ally")
    CO = BankInfo("Capital One")
    banks = [USAA, WF, Ally, CO]
    p.add_banks(banks)
    p.update_local()
    p.export_csv(output_path="output\\results.csv", period=["2021-01-01", "2021-12-31"])
