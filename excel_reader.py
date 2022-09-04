import pandas as pd
from database import Facultative, Schedule


def get_task(file: str):
    filename = file.split('/')[1]
    print(file)
    print(filename)
    if 'аспирантура' in filename.split(' '):
        return
    else:
        faculty = filename.split('\\')[-1].split(' ')[:2]
    if 'нечетная' in filename:
        odd = 0
    else:
        odd = 1
    schedule = Schedule()
    fac_id = Facultative().get_id(*faculty)
    df = pd.read_excel(file)
    columns = list(df.columns)
    new_columns = list(df.iloc[1])
    df.rename(columns={key: value for key, value in zip(columns, new_columns)}, inplace=True)
    df = df[2:]
    formatted_data(df, 'Часы')
    formatted_data(df, 'День')
    for group in df.columns[2:]:
        for i, data in df['День'].items():
            time = df['Часы'][i]
            if '\n' in data:
                data = data.split('\n')[-1]

            desc = df[group][i] if df[group][i] != '\n' else None
            if desc is None or isinstance(desc, float):
                continue

            date = data.split('\n')[0].split(' ')[0]
            schedule.add(date, time, desc, fac_id, group, odd)


def formatted_data(df, column):
    tmp = ''
    for i, data in df[column].items():
        if isinstance(data, str):
            tmp = data
        else:
            df[column][i] = tmp
