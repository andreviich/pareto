#Загрузка библиотек
import pandas as pd
import numpy as np
import csv


hhh = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
df = pd.read_csv('flat.csv', delimiter=";")

# #Формирование массивов данных и поиск максимальных значений по критериям
max_number1,\
max_number2,\
max_number3,\
max_number4,\
max_number5,\
max_number6,\
max_number7,\
max_number8 = max(df.iloc[0].to_list()),\
              max(df.iloc[1].to_list()),\
              max(df.iloc[2].to_list()),\
              max(df.iloc[3].to_list()),\
              max(df.iloc[4].to_list()),\
              max(df.iloc[5].to_list()),\
              max(df.iloc[6].to_list()),\
              max(df.iloc[7].to_list())
points = df.iloc[8].to_list()
df.drop(df.tail(1).index,inplace=True)

df = df.transpose()
df.columns = ["Стоимость→min","Площадь→max","Время до метро→min","Год постройки→max","Этаж→max","Потолок→max","Залог→min","Предудущих собственников→min","Стоимость коммунальных платежей (фикс)→min" ]
print(df)



#Формирование таблицы с максимальными значениями по критериям
def pretty_table(data, cell_sep=' | ', header_separator=True) -> str:
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [str(data[row][col]) for row in range(rows)]
        col_width.append(len(max(columns, key=len)))

    separator = "-+-".join('-' * n for n in col_width)

    lines = []

    for i, row in enumerate(range(rows)):
        result = []
        for col in range(cols):
            item = str(data[row][col]).rjust(col_width[col])
            result.append(item)

        lines.append(cell_sep.join(result))

        if i == 0 and header_separator:
            lines.append(separator)

    return '\n'.join(lines)

data = [
    ["Максимум", "Значение"],
    {"по стоимости": max_number1, "по площади": max_number2, "по времени до метро": max_number3, "по году постройки": max_number4, "по оценке постояльцев": max_number5, "по этажу": max_number6, "по высоте потолков": max_number7, "по залогу":max_number8}
]
rows = [
    data[0]
]
rows += [(k, v) for k, v in data[1].items()]
print(pretty_table(rows))


#Коэффициенты значимости
kk = np.array(points)
kk1 = np.sum([kk])
koef = [-kk[0]/kk1, kk[1]/kk1, -kk[2]/kk1, kk[3]/kk1, kk[4]/kk1, kk[5]/kk1, kk[6]/kk1, -kk[7]/kk1]
kkkk = [kk, koef]
ind = ['Значимость', 'a (%) = ']
cpl = ['', '', '', '', '', '', '', '', '', '']
df1 = pd.DataFrame(data=kkkk, index = ind, columns = cpl)
print(df1)

df_tr = df.transpose()

b1 = df_tr.iloc[0]/max(df_tr.iloc[0].to_list())
c1 = df_tr.iloc[1]/max(df_tr.iloc[1].to_list())
d1 = df_tr.iloc[2]/max(df_tr.iloc[2].to_list())
e1 = df_tr.iloc[3]/max(df_tr.iloc[3].to_list())
f1 = df_tr.iloc[4]/max(df_tr.iloc[4].to_list())
g1 = df_tr.iloc[5]/max(df_tr.iloc[5].to_list())
h1 = df_tr.iloc[6]/max(df_tr.iloc[6].to_list())
i1 = df_tr.iloc[7]/max(df_tr.iloc[7].to_list())
j1 = df_tr.iloc[8]/max(df_tr.iloc[8].to_list())

p = np.array([b1, c1, d1, e1, f1, g1, h1, i1, j1])
p = p.transpose()

columns = ["Стоимость→min","Площадь→max","Время до метро→min","Год постройки→max","Этаж→max","Потолок→max","Залог→min","Предудущих собственников→min","Стоимость коммунальных платежей (фикс)→min" ]

df2 = pd.DataFrame(data=p, index = hhh, columns = columns)
print(df2)


koef = [-kk[0]/kk1, kk[1]/kk1, -kk[2]/kk1, kk[3]/kk1, kk[4]/kk1, kk[5]/kk1, kk[6]/kk1, -kk[7]/kk1,-kk[8]/kk1]

ww = p*koef
www = np.array([np.sum([ww[0]]), np.sum([ww[1]]), np.sum([ww[2]]), np.sum([ww[3]]), np.sum([ww[4]]), np.sum([ww[5]]), np.sum([ww[6]]), np.sum([ww[7]]), np.sum([ww[8]]), np.sum([ww[9]])])
www = www.transpose()
print(www)
print ('Оптимальное значение', max(www), f'- квартира № {np.where(www == max(www))[0][0] + 1}')

hhh = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
hhh2 = ['Показатель по линейной свертке']

df3 = pd.DataFrame(data=www, index = hhh, columns = hhh2)
print(df3)


