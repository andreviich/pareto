# Импорт библиотеки, которая ищет парето оптимальные точки
from paretoset import paretoset
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from numpy import exp,sqrt
import time
import csv
import pandas as pd

def data_entry():
    global vibor, matrr, df, criteria, direction, number_object, number_char, name_object, name_char, weight, criteria_num, code
    vibor = input('Введите "+", чтобы самостоятельно заполнить массив характеристик объектов. Введите "-" для рандомного заполнения: ')
    #рандомный ввод
    if vibor == "-":
        number_object = int(input('Введите количество объектов: '))
        number_char = int(input('Введите количество характеристик: '))
        dd = float(input('Введите нижнюю границу максимального числа для рандомного заполнения: '))
        cc = float(input('Введите верхнюю границу максимального числа для рандомного заполнения: '))
        matrr = {}
        for i in range(number_char):
            matrr[i+1] = np.random.uniform(dd, cc, number_object)
        df = pd.DataFrame(matrr)
        code = list(range(1, number_object+1))
        df.index = code
        #df.index.name = 'Объекты'
        entered_list_a = input("Введите список критериев через запятую, по которым осуществляется оптимизация: ").split(',')
        name_object = list(map(int, entered_list_a))
        criteria = list(name_object)
        direction = {}
        print('Укажите направление оптимизации для критериев. Введите "max" для направления к максимуму, введите "min" - к минимуму:')
        for i in range(len(name_object)):
            direction[name_object[i]] = input(str(name_object[i])+' - ')
        weight = {}
        print("Введите весовые коэффициенты характеристик:")
        for i in range(len(name_object)):
            weight[name_object[i]] = float(input(str(name_object[i])+' - '))
        print(df)
        print("Список критериев:", criteria)
        print("Направление оптимизации для каждого из указанных критериев:", direction)
        print("Весовые коэффициенты характеристик:", weight)
        
    #ручной ввод
    elif vibor == "+":
        number_object = int(input('Введите количество объектов: '))
        print("Введите название объектов:")
        name_object = []
        for i in range(number_object):
            name = input(str(i+1)+" - ")
            name_object.append(name.replace(" ", ""))
        number_char = int(input('Введите количество характеристик: '))
        print("Введите название характеристик:")
        name_char = []
        for i in range(number_char):
            name1 = input(str(i+1)+" - ")
            name_char.append(name1.replace(" ", ""))
        print(name_object)
        print(name_char)
        matrr_1 = {}
        print("Заполните через запятую значения характеристик объектов:")
        for i in range(number_object):
            obj_list = input(str(i+1)+": ").split(',')
            matrr_1[name_object[i]] = list(map(float, obj_list))
        #print(matrr_1)
        lll = list(matrr_1.items())
        matrr = {}
        for i in range(number_char):
            line = []
            for ii in range(number_object):
                line.append(lll[ii][1][i])
            matrr[name_char[i]] = line  
        #print(matrr)
        df = pd.DataFrame(matrr)
        df.index = name_object
        #df.index.name = 'Объекты'
        entered_list = input("Введите список критериев через запятую, по которым осуществляется оптимизация: ")
        ent_list = entered_list.replace(" ", "")
        e_list = ent_list.split(',')
        criteria = list(e_list)
        entered_list_a = input("Введите порядковые номера критериев через запятую, по которым осуществляется оптимизация: ").split(',')
        criteria_num = list(map(int, entered_list_a))
        direction = {}
        print('Укажите направление оптимизации для критериев. Введите "max" для направления к максимуму, введите "min" - к минимуму:')
        for i in range(len(criteria)):
            direction[criteria[i]] = input(criteria[i]+' - ')
        weight = {}
        print("Введите весовые коэффициенты характеристик:")
        for i in range(len(criteria)):
            weight[criteria[i]] = float(input(str(criteria[i])+' - '))
        print(df)
        print("Список критериев:", criteria)
        print("Направление оптимизации для каждого из указанных критериев:", direction)
        print("Весовые коэффициенты характеристик:", weight)
        
data_entry()


def pareto_solution():
    # сумма произв критериев для каждого объекта
    # Если минимизируем и максимизируем одновременно, то надо делать по две диаграммы для каждого критерия. Надо снаяала отнормировать каждый критерий (разделить на максимум каждого критерия все остальные значения), т.е мы присовим им вес.
    # надо среди оптимальных найти сам
    # Делаем маску - для каждого key
    # (критерия, по которыу осуществляется оптимизация) указываем values
    # т.е куда мы его устремляем

    mask = paretoset(df[direction.keys()],
                     sense=direction.values())

    # накладываем маску
    pareto_points = df[mask]

    print("Набор точек поверхности Парето: \n")
    print(pareto_points, "\n")
    print("Направление оптимизации для каждого из указанных критериев:", direction,  "\n")
    print("Оптимальные по Парето точки: ", pareto_points.index.tolist(), "\n")


    # Если количество оптимизируемых критериев = 2, то рисуем диаграмму значений
    if len(direction.keys()) == 2:

        ax = df.plot.scatter(x= list(direction.keys())[0], y = list(direction.keys())[1], color="Green", label="Массив точек")
        pareto_points.plot.scatter(x= list(direction.keys())[0], y = list(direction.keys())[1], color="white", label="Направления оптимизации: "+str(direction), ax=ax);
        pareto_points.plot.scatter(x= list(direction.keys())[0], y = list(direction.keys())[1], color="Red", linestyle = "--", label="Оптимальные по Парето", ax=ax)
        #pareto_points.plot(x= list(direction.keys())[1], y = list(direction.keys())[0], color="orange", linestyle = "--", label="Поверхность Парето", ax=ax)
        plt.title("Плоскость Парето")
        plt.legend(loc='best')

    # Если количество оптимизируемых критериев >2, то рисуем лепестковую диаграмму
    else:

    # надо как то взять все значения датафрейма без индексов и заголовков колонок
        categories = [str(elem) for elem in df.columns.tolist()]
        #print(categories)
        matr_PM = []
        for i in range(len(df.index.tolist())):
            list_PM = df.iloc[i]
            matr_PM.append(list_PM.tolist())
        #print(matr_PM, sep = "\n")


        # r ->  числовые значения характеристик
        # theta -> оси / названия характеристик
        # name -> легенда / имена объектов

        fig = go.Figure()
        for pm,d in zip(matr_PM, df.index.tolist()):
            fig.add_trace(go.Scatterpolar(r = pm, theta=categories, fill= 'toself',
                                          name=str(d)))


        fig.update_layout(title = "Лепестковая диаграмма", polar = dict(radialaxis = dict(visible = True),
        angularaxis = dict(rotation=360)),
        showlegend=True)

        fig.show()

start_time = time.time()
pareto_solution()
print("Время:", (time.time() - start_time))


import numpy as np
from numpy import exp,sqrt
import time
import csv
from scipy.optimize import linprog
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#import oapackage
plt.rcParams['figure.figsize'] = (10.0, 7.0)

def linear_convolution():
    #создаем список, внутри которого списки данных характеристик
    coords = []
    for i in range(len(criteria)):
        coords.append(list(df[criteria[i]]))
    #print(coords)

    #создаем список, внутри которого списки данных характеристик конкретного объекта
    coords_final = []
    for i in range(number_object):
        line_coords = []
        for ii in range(len(criteria)):
            line_coords.append(coords[ii][i])
        coords_final.append(line_coords)
    #print(*coords_final, sep='\n')

    #в зависимости от направления оптимизации меняем знак у значения словаря
    new_weight = {}
    for i in range(len(criteria)):
        if direction[criteria[i]] == 'max':
            new_weight[criteria[i]] = weight.get(criteria[i])
        elif direction[criteria[i]] == 'min':
            new_weight[criteria[i]] = weight.get(criteria[i])*(-1)
    #print(new_weight)
    weight_all = list(new_weight.values()) #список значений словаря

    #первый этап выполнения линейной свертки по критериям
    svertka = []
    for i in range(len(coords_final)):
        sver = []
        for ii in range(len(coords_final[i])):
            sv = coords_final[i][ii]*weight_all[ii]
            sver.append(sv)
        svertka.append(sver)
    #print(*svertka, sep='\n')

    #Линейная свертка по критериям
    svertka_final = []
    for i in range(len(svertka)):
        line_sv = sum(svertka[i])
        li = round(line_sv, 2)
        svertka_final.append(li)

    #объект, который подходит для оптимального значения
    if vibor == "+":
        opti = svertka_final.index(max(svertka_final))
        optimal_name = name_object[opti]
    elif vibor == "-":
        opti = svertka_final.index(max(svertka_final))
        optimal_name = opti + 1

    print("Свертка:", svertka_final)
    print("Оптимальное значение:", max(svertka_final), "-", optimal_name)
    print("Направление оптимизации для каждого из указанных критериев:", direction,  "\n")

    #диаграмма свертки
    DD = {}
    if vibor == "+":
        DD1 = name_object
    elif vibor == "-":
        DD1 = []
        for i in range(number_object):
            DD1.append(i+1)
    #print(DD1)
    for i in range(len(svertka_final)):
        DD[DD1[i]] = svertka_final[i]
    #print(DD)
    fig, ax = plt.subplots()
    ax.bar(DD1, svertka_final)
    ax.bar(optimal_name, max(svertka_final), color = 'red', label = "Оптимальное значение: "+str(max(svertka_final))+" - "+str(optimal_name))
    fig.set_figwidth(12)    #  ширина Figure
    fig.set_figheight(6)    #  высота Figure
    plt.legend()
    plt.title('Диаграмма линейной свертки критериев')
    plt.show()


    if len(criteria) == 2:
        #в зависимости от направления оптимизации меняем знак у значений соответствующего столбца характеристик
        new_coords = []
        for i in range(len(criteria)):
            if direction[criteria[i]] == 'max':
                aa = list(df[criteria[i]])
                n_coords = aa
                new_coords.append(n_coords)
            elif direction[criteria[i]] == 'min':
                bb = list(df[criteria[i]])
                n_coords = [v*(-1) for v in bb]
                new_coords.append(n_coords)
        #print(new_coords)

        #создаем список, внутри которого списки данных характеристик конкретного объекта
        new_coords_final = []
        for i in range(number_object):
            n_line_coords = []
            for ii in range(len(criteria)):
                n_line_coords.append(new_coords[ii][i])
            new_coords_final.append(n_line_coords)
        #print(*new_coords_final, sep='\n')

        #Изменяем параметры свертки (𝑎1; 𝑎2) от 0 до 1 с интервалом 0,1
        alpha1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        alpha2 = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]
        step1 = []
        #all_alp1 = []
        #all_alp2 = []
        for i in range(len(alpha1)):
            line_step = []
            for ii in range(len(new_coords_final)):
                alp = alpha1[i]*new_coords_final[ii][0]+alpha2[i]*new_coords_final[ii][1]
                #a1 = alpha1[i]*new_coords_final[ii][0]
                #a2 = alpha2[i]*new_coords_final[ii][1]
                line_step.append(round(alp, 3))
            step1.append(line_step)
        #print(step1)
        Final = np.array(step1).transpose() #это для того, чтобы выглядело как в методичке
        #print(Final)

        #находим максимальные значения по каждому критерию
        maxlist = []
        index = [] #список, который отслеживает индекс максимального значения для выявления соответствующего объекта
        for i in range(len(alpha1)):
            maxlist.append(max(step1[i]))
            ind = step1[i].index(maxlist[i])
            index.append(ind)
        #print(index)
        #unique_index = list(set(index))
        #print(unique_index)

        #с помощью списка index выводим значения характеристик объектов
        true_points = []
        for i in range(len(index)):
            point = index[i]
            pointt = coords_final[point]
            true_points.append(pointt)
        #print(true_points)

        #уникальные значения списка true_points
        from  more_itertools import unique_everseen
        pppooo = list(unique_everseen(true_points))
        #print(pppooo)

        #набор точек поверхности Паретто
        LLL = [] #индексы нужных объектов
        for i in range(len(pppooo)):
            point_par = coords_final.index(pppooo[i])
            LLL.append(point_par)
        #print(LLL)
        Names = [] #наименования нужных объектов
        if vibor == "+":
            for i in range(len(LLL)):
                itog_par = name_object[LLL[i]]
                Names.append(itog_par)
        elif vibor == "-":
            for i in range(len(LLL)):
                Names.append(LLL[i])
        print(Names)
        #if vibor == "-":
            #for i in range(len(Names)):

        VALUES = list(matrr.values())
        NEW_VALUES = [] #для пандаса
        for i in range(len(VALUES)):
            Linee = []
            for ii in range(len(Names)):
                Linee.append(VALUES[i][LLL[ii]])
            NEW_VALUES.append(Linee)
        #print(NEW_VALUES)

        itog_points_pareto = {} #набор точек поверхности Паретто
        for i in range(len(list(matrr.values()))):
            itog_points_pareto[list(matrr.keys())[i]] = NEW_VALUES[i]
        new_df = pd.DataFrame(itog_points_pareto)
        if vibor == '+':
            new_df.index = Names
        elif vibor == '-':
            for i in range(len(Names)):
                Names[i] = Names[i] + 1
            new_df.index = Names

        #точки для графика
        final_points = []
        for i in range(len(criteria)):
            line_points = []
            for ii in range(len(true_points)):
                line_points.append(true_points[ii][i])
            final_points.append(line_points)
        #print(*final_points, sep='\n')

        print("\n"+"Результат многокритериальной оптимизации по Парето:")
        print(*list(Final), sep = '\n')
        print("Максимальные значения:")
        print(maxlist, "\n")
        print("Набор точек поверхности Паретто:")
        print(new_df)

        plt.scatter(final_points[0], final_points[1], color = 'white', label = 'Направления оптимизации: '+str(direction))
        plt.scatter(coords[0], coords[1], color = 'blue', label = 'Массив точек')
        plt.scatter(final_points[0], final_points[1], color = 'red', label = 'Оптимальные значения')
        plt.plot(final_points[0], final_points[1], color = 'orange', linestyle = '--', label = 'Поверхность Парето')
        plt.title('Плоскость Парето через линейную свертку')
        plt.legend()
        plt.xlabel(criteria[0])
        plt.ylabel(criteria[1])
        plt.grid()
        plt.show()

        #график
        data = {} #делаем словарь, где клюс - стратегия, значение - строчка линейной свертки
        if vibor == "+":
            datata = name_object
        elif vibor == "-":
            datata = []
            for i in range(number_object):
                datata.append(i+1)
        #print(datata)
        for i in range(len(list(Final))):
            data[datata[i]] = Final[i]
        #print(data)

        dff = pd.DataFrame(data)
        dff.plot(kind='bar', figsize=(11,7))
        index = np.arange(11)
        plt.xticks(index,[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        plt.plot((index), (maxlist))
        plt.title('Гистограмма распределения')
        plt.grid()
        plt.show()

    #какие-то жалкие попытки сделать > 2 характеристик
    if len(criteria) > 2:
        new_coords = []
        for i in range(len(criteria)):
            if direction[criteria[i]] == 'max':
                aa = list(df[criteria[i]])
                n_coords = aa
                new_coords.append(n_coords)
            elif direction[criteria[i]] == 'min':
                bb = list(df[criteria[i]])
                n_coords = [v*(-1) for v in bb]
                new_coords.append(n_coords)
        #print(new_coords)
        new_coords_final = []
        for i in range(number_object):
            n_line_coords = []
            for ii in range(len(criteria)):
                n_line_coords.append(new_coords[ii][i])
            new_coords_final.append(n_line_coords)
        #print(*new_coords_final, sep='\n')



        categories = [str(elem) for elem in df.columns.tolist()]
        matr_PM = []
        for i in range(len(df.index.tolist())):
            list_PM = df.iloc[i]
            matr_PM.append(list_PM.tolist())
        #print(categories)
        #print(matr_PM)
        DD2 = []
        for i in range(len(DD1)):
            DD2.append(str(DD1[i]))
        #print(DD2)

        # r ->  числовые значения характеристик
        # theta -> оси / названия характеристик
        # name -> легенда / имена объектов

        fig = go.Figure()
        if vibor == "+":
            for pm,d in zip(matr_PM, name_object):
                fig.add_trace(go.Scatterpolar(r = pm, theta=categories, fill= 'toself', name=str(d)))
        elif vibor == "-":
            for pm,d in zip(matr_PM, DD2):
                fig.add_trace(go.Scatterpolar(r = pm, theta=categories, fill= 'toself', name=str(d)))

        fig.update_layout(title = "Лепестковая диаграмма", polar = dict(radialaxis = dict(visible = True),
        angularaxis = dict(rotation=90)), showlegend=True)

        fig.show()


start_time = time.time()
linear_convolution()
print("Время:", (time.time() - start_time))




def ideal_dot():
    if vibor == '-' :
        criteria_num = name_object
        direct = {}
        print('Укажите направление оптимизации для критериев. Введите "max" для направления к максимуму, введите "min" - к минимуму:')
        for i in range(len(name_object)):
            direct[name_object[i]] = input(str(name_object[i])+' - ')
    else:
        entered_list_a = input("Введите порядковые номера критериев через запятую, по которым осуществляется оптимизация: ").split(',')
        criteria_num = list(map(int, entered_list_a))
        direct = {}
        print('Укажите направление оптимизации для критериев. Введите "max" для направления к максимуму, введите "min" - к минимуму:')
        for i in range(len(criteria_num)):
            direct[criteria_num[i]] = input(str(criteria_num[i])+' - ')
    #print(criteria_num)
    #print(direction)
    #значения из датафрейма
    categories = df.columns.tolist()
    matr_PM = []
    for i in range(len(df.index.tolist())):
        list_PM = df.iloc[i]
        matr_PM.append(list_PM.tolist())
    #print(matr_PM, sep='\n')
    trash = np.array(matr_PM)
    trtr = trash.transpose()
    #print(trtr)

    #формирование идеальной точки
    ideal_dot = []
    for i in range(len(criteria_num)):
        k = criteria_num[i] - 1
        l = criteria_num[i]
        if direct[l] == 'max':
            ideal_dot.append(max(trtr[k]) + 1)
        elif direct[l] == 'min':
            ideal_dot.append(min(trtr[k]) - 1)

    print('значения идеальной точки по заданным критериям:')
    print(ideal_dot)

    #нахождение расстояний до идеальной точки по заданным критериям

    #оставляем в исходном массиве только значения по используемым критериям
    clear_trash = []
    for i in range(len(trash)):
        dot = trash[i]
      ##почистить dot оставив только нужные критерии
        clear_dot = []
        for k in range (len(criteria_num)):
            index = criteria_num[k] - 1
            clear_dot.append(dot[index])
        clear_trash.append(clear_dot)
    #print(clear_trash)

    #первые 2 шага формулы из методички
    distances = []
    for i in range(len(clear_trash)):
        dot = clear_trash[i]
        dist = []
        for j in range(len(ideal_dot)):
        #print(ideal_dot[j])
            step_one = ideal_dot[j] - dot[j]
            step_two = step_one ** 2
            dist.append(step_two)
        distances.append(dist)
    #print(distances, sep = '\n')

    #последние 2 шага формулы из методички
    final_distances = []
    for i in range(len(distances)):
        k = sum(distances[i])
        final_distances.append(math.sqrt(k))
    #print(final_distances)

    print('Оптимальное значение:', min(final_distances))

    minim = min(final_distances)
    for i in range(len(final_distances)):
        if minim == final_distances[i]:
            g = i
    print('Номер точки, наиболее приближенной к идеальной:', g+1)
    print('----------------------------------------------------------------------')

    #Паретто-оптимальное множество решений + идеальная точка и ближайшая к ней
    mask = paretoset(df[direction.keys()],
                    sense=direction.values())

    # накладываем маску
    pareto_points = df[mask]
    categories = [str(elem) for elem in df.columns.tolist()]
    pareto_list = []
    for i in range(len(pareto_points.index.tolist())):
        list_PM = pareto_points.iloc[i]
        pareto_list.append(list_PM.tolist())
    pareto_list.append(ideal_dot)

    #граффффффффффеееееееееееееееееееееееееееееееееееееекккккккккккккккккккккккккк с указанием идеальной точки
    fig = go.Figure()
    for pm,d in zip(pareto_list, df.index.tolist()):
        fig.add_trace(go.Scatterpolar(r = pm, theta=categories, fill= 'toself',
                                              name=str(d)))

    fig.update_layout(title = "Лепестковая диаграмма с указанием идеальной точки", polar = dict(radialaxis = dict(visible = True),
    angularaxis = dict(rotation=90)),
    showlegend=True)

    fig.show()

    #вывод парето-оптимальных точек + идеальная
    print('Набор точек поверхности Паретто:')
    for i in range(len(pareto_list)):
        print(i+1, *pareto_list[i])

start_time = time.time()
ideal_dot()
print('------------------------------------------------------------------------')
print("Время:", (time.time() - start_time))
