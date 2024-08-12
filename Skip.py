import pandas as pd


def process_session_data(df):
    df = df.drop(columns=['Количество_баллов', 'ID_дисциплины'])
    df['Пересдача'] = df['Пересдача'].replace({'Да': 1, 'Нет': 0})
    df['Комиссия'] = df['Комиссия'].replace({'Да': 1, 'Нет': 0})
    df['Средний_балл'] = df.groupby(['ID_студента', 'Номер_сессии'])['Оценка_по_предмету'].transform('mean')
    df['Общее_число_пересдач'] = df.groupby(['ID_студента', 'Номер_сессии'])['Количество_пересдач'].transform('sum')
    df = df.drop(columns=['Пересдача', 'Комиссия', 'Оценка_по_предмету', 'Количество_пересдач']).drop_duplicates(subset=['ID_студента', 'Номер_сессии'])
    df.reset_index(drop=True, inplace=True)
    return df

# Чтение данных
dfs = [pd.read_csv(f'/Users/jimsgood/Downloads/import/session{year}.csv', delimiter=';') for year in range(2015, 2024)]

# Обработка данных для каждого года
dfs_processed = [process_session_data(df) for df in dfs]

# Объединение всех данных по колонке ID_студента
merged_df = pd.concat(dfs_processed).pivot_table(index='ID_студента', columns='Номер_сессии', values=['Средний_балл', 'Общее_число_пересдач']).reset_index()
merged_df.columns = ['ID_студента'] + [f'{col1}_Сессия_{int(col2)}' if col1 != 'ID_студента' else col1 for col1, col2 in merged_df.columns[1:]]
merged_df.columns.name = None

# Подсчет общего количества пересдач за весь период времени для каждого студента
merged_df['Общее_число_пересдач_за_все_время'] = merged_df[[col for col in merged_df.columns if 'Общее_число_пересдач' in col]].sum(axis=1)

# Заполнение пропусков нулями
merged_df = merged_df.fillna(0)

# Сохранение итогового DataFrame в Excel
merged_df.to_excel('Результаты_сессий_2015_2023.xlsx', index=False)

# Загрузка данных из трех файлов
df_2022 = pd.read_csv('/Users/jimsgood/Downloads/import/absence2022.csv', delimiter=';')
df_2023 = pd.read_csv('/Users/jimsgood/Downloads/import/absence2023.csv', delimiter=';')
df_2024 = pd.read_csv('/Users/jimsgood/Downloads/import/absence2024.csv', delimiter=';')

# Удаляем ненужные столбцы
df_2022.drop(columns=['Тип_пропуска', 'ID_дисциплины'], inplace=True)
df_2023.drop(columns=['Тип_пропуска', 'ID_дисциплины'], inplace=True)
df_2024.drop(columns=['Тип_пропуска', 'ID_дисциплины'], inplace=True)

# Подсчитываем количество прогулов в каждом году
counts_2022 = df_2022['ID_студента'].value_counts().reset_index()
counts_2022.columns = ['ID_студента', 'Количество_прогулов_2022']

counts_2023 = df_2023['ID_студента'].value_counts().reset_index()
counts_2023.columns = ['ID_студента', 'Количество_прогулов_2023']

counts_2024 = df_2024['ID_студента'].value_counts().reset_index()
counts_2024.columns = ['ID_студента', 'Количество_прогулов_2024']

# Объединяем все данные в один DataFrame
combined = pd.merge(counts_2022, counts_2023, on='ID_студента', how='outer')
combined = pd.merge(combined, counts_2024, on='ID_студента', how='outer')

# Заполняем NaN значения нулями
combined.fillna(0, inplace=True)

# Преобразуем все количество прогулов в int
combined['Количество_прогулов_2022'] = combined['Количество_прогулов_2022'].astype(int)
combined['Количество_прогулов_2023'] = combined['Количество_прогулов_2023'].astype(int)
combined['Количество_прогулов_2024'] = combined['Количество_прогулов_2024'].astype(int)

# Суммируем количество прогулов для каждого студента
combined['Общее_количество_прогулов'] = combined['Количество_прогулов_2022'] + combined['Количество_прогулов_2023'] + combined['Количество_прогулов_2024']

# Оставляем только необходимые столбцы
combined = combined[['ID_студента', 'Общее_количество_прогулов']]

# Сохраняем результат в Excel файл
combined.to_excel('student_absences.xlsx', index=False)

results_df = pd.read_excel('Результаты_сессий_2015_2023.xlsx')
absences_df = pd.read_excel('student_absences.xlsx')

# Объединение данных по столбцу ID_студента
merged_df = pd.merge(results_df, absences_df, on="ID_студента", how="outer")

# Сохранение объединенных данных в новый файл Excel
merged_df.to_excel('оценки_и_пропуски_маргу.xlsx', index=False)