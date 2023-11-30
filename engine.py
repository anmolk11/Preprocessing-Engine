import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer

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


def fill_missing_vals(cols_info,file_name):
    df = pd.read_csv(f'static\data\{file_name}')
    with_mean = []
    with_mode = []
    with_median = []
    to_drop = []
    for k,v in cols_info.items():
        if v == 'Fill with Mode':
            with_mode.append(k)
        elif v == 'Fill with Mean':
            with_mean.append(k)
        elif v == 'Fill with Medain':
            with_median.append(k)
        else:
            to_drop.append(k)
    
    if len(with_mean) > 0:
        imp_mean = SimpleImputer(strategy = 'mean')
        df[with_mean] = imp_mean.fit_transform(df[with_mean])
    
    if len(with_median) > 0:
        imp_median = SimpleImputer(strategy = 'median')
        df[with_median] = imp_median.fit_transform(df[with_median])
    
    if len(with_mode) > 0:
        imp_mode = SimpleImputer(strategy = 'most_frequent')
        df[with_mode] = imp_mode.fit_transform(df[with_mode])
    
    if len(to_drop) > 0:
        df.drop(to_drop,axis = 1,inplace = True)
    
    file_name = file_name.split('.')[0]
    clean_file = f'static\data\{file_name}_fill_na.csv'
    debug(clean_file)
    df.to_csv(clean_file,index = False)
    return clean_file

    


if __name__ == '__main__':
    data = process()
    print(data['cols_miss'])