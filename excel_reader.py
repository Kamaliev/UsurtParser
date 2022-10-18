import pandas as pd
from database.schedule import Values


def get_default(file: str):
    filename = file.split('/')[1]
    if 'аспирантура' in filename.split(' '):
        return
    else:
        faculty = filename.split('\\')[-1].split(' ')[:2][0]
    if 'нечетная' in filename:
        odd = 0
    else:
        odd = 1

    df = pd.read_excel(file)

    return [df], [faculty], odd


def get_targeted(file):
    filename = file.split('/')[1].lower()
    if 'нечетная' in filename:
        odd = 0
    else:
        odd = 1

    df = pd.read_excel(file, None)
    dataframes = []
    facultets = []
    for facultet in df:
        facultets.append(facultet.split('-')[0])
        dataframes.append(df[facultet])

    return dataframes, facultets, odd


def get_task(file: str):
    dataframes, facultets, odd = get_targeted(file) if 'целевое' in file else get_default(file)
    clear_data = []
    for df, faculty in zip(dataframes, facultets):
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
                clear_data.append(
                    Values(
                        time=time,
                        weekday=date,
                        desc=desc,
                        group=group,
                        odd=odd,
                        facultative=str(faculty),
                        course=int(group.split("-")[-1][0])
                    )
                )
    return clear_data


def formatted_data(df, column):
    tmp = ''
    for i, data in df[column].items():
        if isinstance(data, str):
            tmp = data
        else:
            df[column][i] = tmp


if __name__ == '__main__':
    import os

    file = 'tmp/Нечетная (целевое)(2).xlsx'
    print(get_task(file))
