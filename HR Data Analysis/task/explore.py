import pandas as pd
import requests
import os


# scroll down to the bottom to implement your solution

def concat_datasets(data_one, data_two):
    return pd.concat([data_one, data_two])


def loading_and_reindexing():
    office_A = pd.read_xml('../Data/A_office_data.xml')
    office_B = pd.read_xml('../Data/B_office_data.xml')
    hr_data = pd.read_xml('../Data/hr_data.xml')

    office_A = office_A.astype({'employee_office_id': str})
    office_A['employee_office_id'] = 'A' + office_A['employee_office_id']
    office_A.set_index('employee_office_id', inplace=True)

    office_B = office_B.astype({'employee_office_id': str})
    office_B['employee_office_id'] = 'B' + office_B['employee_office_id']
    office_B.set_index('employee_office_id', inplace=True)

    hr_data.set_index('employee_id', inplace=True)

    return office_A, office_B, hr_data


def merge_data(AB, HR):
    return AB.merge(HR, indicator=True, left_index=True, right_index=True)


if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    office_A, office_B, hr_data = loading_and_reindexing()

    concated_AB = concat_datasets(office_A, office_B)
    merged_AB_HR = merge_data(concated_AB, hr_data)
    merged_AB_HR.drop(columns='_merge', inplace=True)
    merged_AB_HR.sort_index(inplace=True)

    print(list(merged_AB_HR.index))
    print(list(merged_AB_HR.columns))

    # write your code here
