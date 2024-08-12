import pandas as pd

results_df = pd.read_excel('Студент_Маргу_1.xlsx')
absences_df = pd.read_excel('оценки_и_пропуски_маргу.xlsx')

# Объединение данных по столбцу ID_студента
merged_df = pd.merge(results_df, absences_df, on="ID_студента", how="outer")

merged_df = merged_df.dropna(subset=['Формат_обучения'])

# Удаление строк, где в колонке "Общее_число_пересдач_Сессия_2" ничего не указано
merged_df = merged_df.dropna(subset=['Общее_число_пересдач_Сессия_2'])
merged_df['Общее_количество_прогулов'] = merged_df['Общее_количество_прогулов'].fillna(0, inplace=True)
# Сохранение объединенных данных в новый файл Excel
merged_df.to_excel('марГу.xlsx', index=False)

