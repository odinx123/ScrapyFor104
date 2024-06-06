import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Toplevel

class ScrollableFrame:
    def __init__(self, parent_frame, data_list, salary_dic, *args, **kwargs):
        self.parent_frame = parent_frame
        self.data_list = data_list  # Store data list for later use
        self.canvas = tk.Canvas(parent_frame)
        self.scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.salary_dic=salary_dic
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind the mouse wheel to the canvas for scrolling
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # Display the data list on the scrollable frame
        self.display_data(data_list)

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def display_data(self, data_list):
        for i in range(len(data_list)):
            frame = ttk.Frame(self.scrollable_frame, padding="5")
            frame.pack(fill="x", pady=5)
            if i != 0:
                ttk.Label(frame, text='----------------------------------------------------------------------------------------').pack()
            ttk.Label(frame, text=data_list[i]['company_title'], font=('Arial', 20, 'bold'), foreground='moccasin').pack()
            ttk.Label(frame, text=data_list[i]['category'], font=('Arial', 15, 'bold'), foreground='tomato').pack()
    #月薪
            if int(data_list[i]['min_salary']) == 0 and str(data_list[i]['salary_max']) == 'inf':
                ttk.Label(frame, text='待遇面議', font=('Arial', 15, 'bold'), foreground='lawngreen').pack()
            elif str(data_list[i]['salary_max']) == 'inf':
                ttk.Label(frame, text=str(data_list[i]['min_salary']) + '以上', font=('Arial', 15, 'bold'), foreground='lawngreen').pack()
            else:
                ttk.Label(frame, text=str(data_list[i]['min_salary']) + '~' + str(data_list[i]['salary_max']), font=('Arial', 15, 'bold'), foreground='lawngreen').pack()
    #學歷        
            if data_list[i]['education']==[]:
                ttk.Label(frame, text='學歷'+'不拘', font=('Arial', 15, 'bold')).pack()
            else:  
                edu='' 
                for data in data_list[i]['education']:
                    edu+=data
                    edu+=' '
                ttk.Label(frame, text='學歷 : '+ edu, font=('Arial', 15, 'bold')).pack()
    #工作經驗
            if data_list[i]['experience']==[]:
                ttk.Label(frame, text='工作經驗'+'不拘', font=('Arial', 15, 'bold')).pack()
            else:    
                ttk.Label(frame, text='工作經驗'+data_list[i]['experience'][0], font=('Arial', 15, 'bold')).pack()
            tool='' 
            for data in data_list[i]['tool']:
                tool+=data
                tool+=' '
            ttk.Label(frame, text='使用工具 : '+tool, font=('Arial', 15, 'bold')).pack()
            ttk.Button(frame, text='查看月薪落點', command=lambda i=i: self.show_bar_chart(i)).pack()

    def show_bar_chart(self, index):
        plt.rc("font", family="Microsoft Jhenghei")
        new_window = Toplevel(self.parent_frame)
        new_window.title('Bar Chart')

        # Extract data for the bar chart from the selected item
        item = self.data_list[index]
        x = list(self.salary_dic.keys())
        y = list(self.salary_dic.values())
        if str(item['salary_max']) == 'inf':
            max=200
        else:
            max=int(item['salary_max'])//1000
        colors = ['aqua']*len(x)
        if int(item['min_salary']) != 0 and str(item['salary_max']) != 'inf':  #待遇面議不顯示月薪落點
            for i in range(len(x)):
                if int(x[i])>=int(item['min_salary'])//1000 and int(x[i])<=max:
                    colors[i]='red'
        title = item['category']
        
        fig, ax = plt.subplots(facecolor='black')  # 設定圖形背景顏色為黑色
        ax.set_facecolor('black')  # 將軸的背景顏色設定為黑色
        ax.bar(x, y, width=10, color=colors)
        category = ' , '.join(title)
        ax.set_title(category, fontsize=20, color='aqua')  # 設定標題顏色
        ax.set_xlabel('月薪(k)', color='aqua')  # 設定x軸標籤顏色
        ax.set_ylabel('職缺數(%)', color='aqua')  # 設定y軸標籤顏色
        ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150])
        ax.set_xticklabels(['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '110', '120', '130', '140', '150'], color='white')  # 设置x轴刻度标签颜色
        ax.tick_params(axis='x', colors='aqua')  # 設定x軸刻度顏色
        ax.tick_params(axis='y', colors='aqua')  # 設定y軸刻度顏色
        ax.spines['bottom'].set_color('aqua')
        ax.spines['top'].set_color('aqua')
        ax.spines['right'].set_color('aqua')
        ax.spines['left'].set_color('aqua')

        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
