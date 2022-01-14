from numpy import empty
import pandas as pd
import os
import re
from glob import glob

def main():
    pass

# Modified variant of Tatyana's implementation
def read_ipc(folder_path):
    def remove_parentheses(text):
        pos = str(text).find(" (")
        if pos == -1:
            return text
        else:
            return text[0:pos]

    def capitalize_uppercase(text):
        if not text[0].islower():
            text = '; '.join(i.capitalize() for i in text.split('; '))
        return text;
    
    def parse_code(code):
        if len(code) < 14:
            return code
        else:
            symbol_section = code[0].upper()
            symbol_class = code[1:3]
            symbol_subclass = code[3].upper()
            symbol_main_group = str(int(code[4:8]))
            symbol_group = code[-6:]
            if symbol_group == '000000':
                symbol_group = '00'
            else:
                symbol_group = re.match('[0-9]*[1-9]', symbol_group).group()
                if(len(symbol_group)) < 2:
                    symbol_group = symbol_group + str(0)
            new_code = symbol_section + symbol_class + symbol_subclass + symbol_main_group + '/' + symbol_group
            return new_code
    
    def parse_in_explanation(text):
        found = re.search('[a-zA-Z][0-9]{2}[a-zA-Z][0-9]{10}', text)
        if found:
            new_code = parse_code(found.group())
            return re.sub('[a-zA-Z][0-9]{2}[a-zA-Z][0-9]{10}', new_code, text)
        else:
            return text

    folder_name = os.path.basename(folder_path)
    prefix = 'EN_ipc_section_'
    postfix = re.search('_title_list_[0-9]+', folder_name).group()
    file_paths = sorted(glob(folder_path + '/' + prefix + '*' + postfix + '.txt'))

    if not file_paths:
        print('There are no files to be read.')
        return None

    df = pd.DataFrame()
    for file_path in file_paths:
        section_df = pd.read_csv(file_path, sep='\t', lineterminator='\n', header=None, names=["code", "explanation"], na_values="")
        df = df.append(section_df)
    df.dropna(inplace=True)
    df.drop_duplicates(subset="code", keep="last", inplace=True)
    df["explanation"] = df["explanation"].apply(capitalize_uppercase)
    df["explanation"] = df["explanation"].apply(parse_in_explanation)
    df["code"] = df["code"].apply(parse_code)

    df = df.sort_values('code').set_index('code')

    return df['explanation'].to_dict()


if __name__ == '__main__':
    ipc_dict = read_ipc('notebooks/data/EN_ipc_title_list_20210101')
    print('')