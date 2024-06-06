import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas = None
def create_plot(parent, x, y1, labels):
    global canvas

    plt.rc("font", family="Microsoft Jhenghei")
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(x, y1, label=labels[0])  # 示例資料
    # plot.plot(x, y2, label=labels[1])  # 示例資料
    plot.legend()       # ===================須改

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def create_pie_chart(parent, labels, data, title):
    global canvas

    plt.rc("font", family="Microsoft Jhenghei")
    fig, ax = plt.subplots(facecolor='black')  # 設定圖形背景顏色為黑色
    ax.set_facecolor('black')  # 將軸的背景顏色設定為黑色
    ax.pie(data, labels=labels, labeldistance=1.05, autopct='%1.1f%%', startangle=90, textprops={'color':'aqua'})
    category = ' , '.join(title)
    ax.set_title(category, fontsize=20, color='aqua')  # 設定標題顏色
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def create_bar_chart_ForSalary(parent, x, y, title):
    global canvas

    plt.rc("font", family="Microsoft Jhenghei")
    fig, ax = plt.subplots(facecolor='black')  # 設定圖形背景顏色為黑色
    ax.set_facecolor('black')  # 將軸的背景顏色設定為黑色
    ax.bar(x, y, width=10, color='darkcyan')
    category = ' , '.join(title)
    ax.set_title(category, fontsize=20, color='aqua')  # 設定標題顏色
    ax.set_xlabel('月薪(k)', color='aqua')  # 設定x軸標籤顏色
    ax.set_ylabel('數量', color='aqua')  # 設定y軸標籤顏色
    ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90,100,110,120,130,140,150])
    ax.set_xticklabels(['10', '20', '30', '40', '50', '60', '70','80','90','100','110','120','130','140','150'], color='white')  # 设置x轴刻度标签颜色
    ax.tick_params(axis='x', colors='aqua')  # 設定x軸刻度顏色
    ax.tick_params(axis='y', colors='aqua')  # 設定y軸刻度顏色
    ax.spines['bottom'].set_color('aqua')
    ax.spines['top'].set_color('aqua')
    ax.spines['right'].set_color('aqua')
    ax.spines['left'].set_color('aqua')

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def create_bar_chart_ForTool(parent, x, y, title):
    global canvas

    plt.rc("font", family="Microsoft Jhenghei")
    fig, ax = plt.subplots(facecolor='black')  # 設定圖形背景顏色為黑色
    ax.set_facecolor('black')  # 將軸的背景顏色設定為黑色
    ax.bar(x, y, color='darkcyan')
    category = ' , '.join(title)
    ax.set_title(category, fontsize=20, color='aqua')  # 設定標題顏色
    ax.set_xlabel('工具', color='aqua')  # 設定x軸標籤顏色
    ax.set_ylabel('使用數', color='aqua')  # 設定y軸標籤顏色
    ax.tick_params(axis='x', colors='aqua')  # 設定x軸刻度顏色
    ax.tick_params(axis='y', colors='aqua')  # 設定x軸刻度顏色
    ax.spines['bottom'].set_color('aqua')
    ax.spines['top'].set_color('aqua')
    ax.spines['right'].set_color('aqua')
    ax.spines['left'].set_color('aqua')

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill='both', expand=True)