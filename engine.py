import pandas as pd
import numpy as np

def debug(*args):
    print('\n================ Debug ================\n')
    print(args)
    print('\n================ Debug ================\n')

def highlighter(x):
    if x['Num of Missing Values'] > 0:
        return ['background-color: #eb6a6a'] * 4
    else:
        return ['background-color: white'] * 4

def process(file_name = 'movies.csv'):
    df = pd.read_csv(f'static\data\{file_name}')
    cols = df.columns
    cats = []
    for i in cols:
        if df[i].dtype == 'int64':
            if df[i].nunique() == 2 and set(df[i].unique()) <= {0, 1}:
                cats.append('Binary')
            else:
                cats.append('Numerical / Discrete')
        elif df[i].dtype == 'float64':
            cats.append('Numerical / Continuous')
        else:
            if df[i].nunique() == 2:
                cats.append('Binary')
            else:
                cats.append('Categorical')

    
    data_miss = df.isna().sum()
    num_miss = data_miss.values
    perc_miss = np.round(num_miss / df.shape[0] * 100,2)
    table_df = df.head().to_html(index = False)


    data = {
        'Feature' : cols,
        'Category' : cats,
        'Num of Missing Values' : data_miss,
        '% of Missing Values' : perc_miss
    }
    data_df = pd.DataFrame(data)
    styled_df = data_df.style.apply(highlighter, axis = 1)
    styled_df.relabel_index(range(1,len(num_miss) + 1))
    data_df = styled_df.to_html(index = False)
    return {
            'table' : table_df,
            "table_name" : file_name,
            'data' : data_df,
            'Feature' : cols,
            'Category' : cats,
            'Num of Missing Values' : data_miss,
            '% of Missing Values' : perc_miss
            }


def fill_missing_vals(cols_info):
    pass


if __name__ == '__main__':
    data = process()
    print(data['cols_miss'])