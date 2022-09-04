import os


class Config:
    database = os.path.abspath(os.path.join("../", 'db.sqlite3'))
    sql_files = os.path.abspath(os.path.join("../", 'sql'))


def get_sql_commands() -> list:
    commands = []

    files = os.listdir(Config.sql_files)

    for file in files:
        path = os.path.join(Config.sql_files, file)
        with open(path, 'r') as f:
            commands += [i.strip() for i in f.read().split(';') if i.strip() != '']
    return commands


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


if __name__ == '__main__':
    print(get_sql_commands())
