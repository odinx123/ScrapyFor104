import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas = None
def create_plot(parent, x, y1, labels):
    global canvas
    #if canvas is not None:
     #   canvas.get_tk_widget().pack_forget()  # 從 Tkinter 中移除 canvas widget
      #  canvas.get_tk_widget().destroy()  # 銷毀 canvas widget
       # plt.close("all")  # 關閉 matplotlib figure
    plt.rc("font", family="Microsoft Jhenghei")
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(x, y1, label=labels[0])  # 示例資料
    # plot.plot(x, y2, label=labels[1])  # 示例資料
    plot.legend()       # ===================須改

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill='x', expand=1)

def create_pie_chart(parent, data, labels, title):
    global canvas

    plt.rc("font", family="Microsoft Jhenghei")
    fig, ax = plt.subplots(facecolor='black')  # 设置图形背景颜色为黑色
    ax.set_facecolor('black')  # 设置轴的背景颜色为黑色
    ax.pie(data, labels=labels, labeldistance=1.05, autopct='%1.1f%%', startangle=90, textprops={'color':'aqua'})
    category = ' , '.join(title)
    ax.set_title(category, fontsize=20, color='aqua')  # 设置标题颜色
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill='x', expand=1)

'''def create_pie_chart(parent,data,labels):
    global canvas
  
    plt.rc("font", family="Microsoft Jhenghei")
        #fig = Figure(figsize=(5, 4), dpi=100)
       # ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    ax.set_facecolor('lightyellow')
    ax.pie(data, labels=labels,labeldistance=1.05, autopct='%1.1f%%', startangle=90)
    ax.set_title('學歷要求', fontsize=20)
    ax.axis('equal')  
    #ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, expand=1)
'''
def create_bar_chart_ForSalary(parent, y, x, title):
    global canvas

    plt.rc("font", family="Microsoft Jhenghei")
    fig, ax = plt.subplots(facecolor='black')  # 设置图形背景颜色为黑色
    ax.set_facecolor('black')  # 设置轴的背景颜色为黑色
    ax.bar(y, x, width=10, color='darkcyan')
    category = ' , '.join(title)
    ax.set_title(category, fontsize=20, color='aqua')  # 设置标题颜色
    ax.set_xlabel('月薪(k)', color='aqua')  # 设置x轴标签颜色
    ax.set_ylabel('職缺數(%)', color='aqua')  # 设置y轴标签颜色
    ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90])
    ax.set_xticklabels(['10', '20', '30', '40', '50', '60', '70', '80', '90'], color='white')  # 设置x轴刻度标签颜色
    ax.tick_params(axis='x', colors='aqua')  # 设置x轴刻度颜色
    ax.tick_params(axis='y', colors='aqua')  # 设置y轴刻度颜色
    ax.spines['bottom'].set_color('aqua')
    ax.spines['top'].set_color('aqua')
    ax.spines['right'].set_color('aqua')
    ax.spines['left'].set_color('aqua')

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill='x', expand=True)

def create_bar_chart_ForTool(parent, y, x, title):
    global canvas

    plt.rc("font", family="Microsoft Jhenghei")
    fig, ax = plt.subplots(facecolor='black')  # 设置图形背景颜色为黑色
    ax.set_facecolor('black')  # 设置轴的背景颜色为黑色
    ax.bar(y, x, color='darkcyan')
    category = ' , '.join(title)
    ax.set_title(category, fontsize=20, color='aqua')  # 设置标题颜色
    ax.set_xlabel('工具', color='aqua')  # 设置x轴标签颜色
    ax.set_ylabel('使用數', color='aqua')  # 设置y轴标签颜色
   # ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90])
   # ax.set_xticklabels(['10', '20', '30', '40', '50', '60', '70', '80', '90'], color='white')  # 设置x轴刻度标签颜色
    ax.tick_params(axis='x', colors='aqua')  # 设置x轴刻度颜色
    ax.tick_params(axis='y', colors='aqua')  # 设置y轴刻度颜色
    ax.spines['bottom'].set_color('aqua')
    ax.spines['top'].set_color('aqua')
    ax.spines['right'].set_color('aqua')
    ax.spines['left'].set_color('aqua')

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill='both', expand=1)
'''def create_bar_chart(parent, num, salary, title):
    global canvas
  
    plt.rc("font", family="Microsoft Jhenghei")
    fig, ax = plt.subplots()
    ax.bar(num,salary,width=10,color='skyblue')
    category=' , '.join(title)
    ax.set_title(category, fontsize=20)#職務類別
    ax.set_xlabel('月薪(k)')
    ax.set_ylabel('職缺數(%)')  #================
    ax.set_xticks([10,20,30,40,50,60,70,80,90],['10','20','30','40','50','60','70','80','90'])

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, expand=1)
'''
'''def create_bar_chart(parent, num, salary, title):
    global canvas

    plt.rc("font", family="Microsoft Jhenghei")
    fig, ax = plt.subplots(facecolor='purple')  # 設置圖形背景顏色為亮紫色
    ax.set_facecolor('#E6E6FA')  # 設置軸的背景顏色為亮紫色
    ax.bar(num, salary, width=10, color='skyblue')
    category = ' , '.join(title)
    ax.set_title(category, fontsize=20, color='aqua')  # 設置標題顏色
    ax.set_xlabel('月薪(k)', color='black')  # 設置x軸標籤顏色
    ax.set_ylabel('職缺數(%)', color='black')  # 設置y軸標籤顏色
    ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90], ['10', '20', '30', '40', '50', '60', '70', '80', '90'])
    ax.tick_params(axis='x', colors='black')  # 設置x軸刻度顏色
    ax.tick_params(axis='y', colors='black')  # 設置y軸刻度顏色
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, expand=1)
'''