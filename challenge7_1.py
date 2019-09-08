import pandas as pd

pd.set_option('max_columns', None)


def data_clean():
    df_data = pd.read_excel('ClimateChange.xlsx', 'Data', index_col='Country code')
    df_data = df_data[df_data['Series code'] == 'EN.ATM.CO2E.KT']
    df_data.drop(['Country name', 'Series code', 'Series name', 'SCALE', 'Decimals'], axis=1, inplace=True)
    df_data.replace('..', pd.np.nan, inplace=True)
    df_data = df_data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df_data.dropna(how='all', inplace=True)
    df_data['Sum emissions'] = df_data.sum(axis=1)
    df_data = df_data['Sum emissions']

    df_country = pd.read_excel('ClimateChange.xlsx', 'Country', index_col='Country code', usecols=[0, 1, 4])
    df = pd.concat([df_country, df_data], axis=1)
    return df


def co3():
    df = data_clean()
    Sum_emissions = pd.DataFrame(df.groupby('Income group').sum())

    # groupby后跟的max() min()是以groupby那列数据作为索引，求出各列的最大值，最小值，但是求出的最大值并不能和国家名对应，因为max求出的国家名的最大值是根据ascii码表的顺序求出的
    df_highest = pd.DataFrame(df.groupby(['Income group']).max())
    df_highest.rename(columns={'Sum emissions': 'Highest emissions', 'Country name': 'Highest emission country'},
                      inplace=True)

    df_lowest = pd.DataFrame(df.groupby(['Income group']).min())
    df_lowest.rename(columns={'Sum emissions': 'Lowest emissions', 'Country name': 'Lowest emission country'},
                     inplace=True)

    Highest_emissions_country = df_highest['Highest emission country']
    Highest_emissions = df_highest['Highest emissions']

    Lowest_emissions = df_lowest['Lowest emissions']
    Lowest_emissions_country = df_lowest['Lowest emission country']

    results = pd.concat(
        [Sum_emissions, Highest_emissions_country, Highest_emissions, Lowest_emissions_country, Lowest_emissions],
        axis=1)

    return results


def co2():
    df = data_clean()
    df_sum = df.groupby('Income group').sum()

    df_max = df.sort_values(by='Sum emissions', ascending=False).groupby('Income group').head(1).set_index(
        'Income group')
    df_max.columns = ['Highest emission country', 'Highest emissions']

    # df_max.reindex(columns=[5:])  reindex可以用来选择列
    # df_max = df_max.reindex(columns=['Highest emission country', 'Highest emissions'])

    df_min = df.sort_values(by='Sum emissions').groupby('Income group').head(1).set_index(
        'Income group')
    df_min.columns = ['Lowest emission country', 'Lowest emissions']

    results = pd.concat([df_sum, df_max, df_min], axis=1)

    return results


print(co2())

