from models import *
'''
Code entry point - Run this file.
'''


if __name__=='__main__':
    p=Parser(working_dir="test_data\\", debug=True)
    # USAA = BankInfo('USAA')
    WF = BankInfo('Wells Fargo')
    # Ally = BankInfo('Ally')
    # CO = BankInfo('Capital One')
    # banks = [USAA, WF, Ally, CO]
    # p.add_banks(banks)
    p.add_bank(WF)
    p.update_local() #Control function
    p.export_csv(output_path = 'output\\results.csv', period = ['2021-01-01','2021-12-31'])
