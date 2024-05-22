import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self, root):
        plt.rc("font", family="Microsoft Jhenghei")  #設定字型為 Windows 內建的微軟正黑體,支援中文顯示
        self.root = root
        self.root.title("GUI")
        self.root.geometry('700x700+300+100')
#
        self.option_frame = tk.Frame(self.root, bg="lightgray", width=200, height=400)
        self.option_frame.place(x=400, y=0)  # 初始化位置在視窗外部（右側）
#
        # 創建Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side='left', fill='both', expand=True)
        
        # ======創建分頁=========
        # 創建tab1
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="a")
        # 創建tab2
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="b")
        # 創建tab3
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="c")
        # 創建tab4
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="d")
        # 創建tab5
        self.tab5 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab5, text="e")

        # 在tab1中創建折線圖
        plot_data_x=[1, 2, 3, 4, 5]
        plot_data_y1=[2, 6, 5, 7, 11]   #==========================
        plot_data_labels=['a']#,'b']
        self.create_plot(self.tab1, plot_data_x, plot_data_y1, plot_data_labels)

        # 在tab2中創建圓餅圖
        pie_chart_data=[10,20,30,40]
        pie_chart_labels = ['A', 'B', 'C', 'D'] 
        self.create_pie_chart(self.tab2, pie_chart_data, pie_chart_labels)
        # 在tab3中創建薪水長條圖
        num=[15,25,35]
        salary=[20,10,5]
        category=['職務類別']
        self.create_bar_chart(self.tab3, num, salary, category)



        # 在右側添加選項按鈕
        self.create_option_menu()
    
    def create_option_menu(self):
        # 在右側添加一個框架來放置按鈕
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side='right', fill='y')
        #image C:\\Users\\user\\Desktop\\py_gui\\icon.png
        self.icon=tk.PhotoImage(file=r"GUI\t\icon.png")
        self.option_button = tk.Button(self.button_frame, text="menu", command=self.toggle_options)
        self.option_button.config(image=self.icon)
        self.option_button.pack(pady=20)  
        # 創建可展開和隱藏的選項框架
        self.option_frame = tk.Frame(self.root)
        self.job_label=tk.Label(self.option_frame,text='職務類別')
        self.job_label.pack(pady=5)
        optionList = ['a','b','c','d','e']  #職務類別===============
        self.value = tk.StringVar()
        self.value.set('職務類別')
        self.option1 = tk.OptionMenu(self.option_frame, self.value,*optionList)
        self.search_btn = tk.Button(self.option_frame, text="確定",command=self.update_chart)
        
        self.option1.pack(pady=5)
        self.search_btn.pack(pady=5)
    
    def toggle_options(self):
        if self.option_frame.winfo_viewable():
            self.option_frame.place_forget()
        else:
            #self.option_frame.pack(side='right', fill='y')
            self.option_frame.place(x=root.winfo_width()-130,y=0)

    def create_plot(self, parent, x, y1, labels):
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        plot.plot(x, y1, label=labels[0])  # 示例資料
       # plot.plot(x, y2, label=labels[1])  # 示例資料
        plot.legend()       # ===================須改

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_pie_chart(self,parent,data,labels):
        #fig = Figure(figsize=(5, 4), dpi=100)
       # ax = fig.add_subplot(111)
        fig, ax = plt.subplots()
        ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def create_bar_chart(self, parent, num, salary, category):
       # plt.rc("font", family="Microsoft Jhenghei")
        fig, ax = plt.subplots()
        ax.bar(num,salary,width=10,color='skyblue')
        ax.set_title(category[0])#職務類別
        ax.set_xlabel('月薪(k)')
        ax.set_ylabel('職缺數(%)')  #================
        ax.set_xticks([10,20,30,40,50,60,70,80,90],['10','20','30','40','50','60','70','80','90'])

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def update_chart(self):#/////////////////////////////////////
       # plt.rc("font", family="Microsoft Jhenghei")
        self.option_frame.place_forget()
        for widget in self.tab1.winfo_children():
            widget.destroy()
        plot_data_x=[1, 2, 3, 4, 5]
        plot_data_y1=[2, 6, 5, 7, 11]   #new data
        plot_data_labels=['a']
        self.create_plot(self.tab1, plot_data_x, plot_data_y1, plot_data_labels)

        for widget in self.tab2.winfo_children():
            widget.destroy()
        pie_chart_data=[5,10,50,35]            #mew data
        pie_chart_labels = ['A', 'B', 'C', 'D'] 
        self.create_pie_chart(self.tab2, pie_chart_data, pie_chart_labels)

        for widget in self.tab3.winfo_children():
            widget.destroy()
        category=self.value.get()
        num=[15,25,35]    #     neew data
        salary=[20,10,5]   #
        self.create_bar_chart(self.tab3, num, salary, category)

if __name__ == "__main__":
    root = tk.Tk()
    gui = Gui(root)
    root.mainloop()
