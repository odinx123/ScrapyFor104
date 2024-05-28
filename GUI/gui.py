import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from PIL import Image
Image.CUBIC = Image.BICUBIC
from ttkbootstrap.constants import *
import ScrollableFrame as sf
import chart

class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI")
        self.root.geometry('900x800+300+100')
        self.root.minsize(900, 800)
        #self.root.maxsize(1000, 800)
        
        self.style = tb.Style("vapor")  # 初始化為 cyborg 主題

        self.right_side_frame = tk.Frame(self.root, bg="gray", width=20, height=400)
        self.right_side_frame.pack(side='right', fill='y')  #初始化位置在視窗外部（右側）
        self.left_side_frame =tk.Frame(self.root)
        self.left_side_frame.pack(side='left', fill='both',expand=True)
        # 創建 Notebook
        self.notebook = ttk.Notebook(self.left_side_frame)
        self.notebook.pack(side='left', fill='both', expand=True)
        
        # ======創建分頁=========
        # 創建 tab1
        self.tab1 = ttk.Frame(self.notebook)
        data_list = [f"Sample data item {i}" for i in range(50)]
        sf.ScrollableFrame(self.tab1, data_list)
        self.notebook.add(self.tab1, text="職缺資訊")
        
        # 創建 tab2
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="使用工具")
        
        # 創建 tab3
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="學歷要求")
        
        # 創建 tab4
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="薪资待遇")
        # 創建 tab5
        self.tab5 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab5, text="工作經歷")

        tool_data_x = ['python', 'C++', 'js', 'css']
        tool_data_y = [2, 6, 5, 7]
        chart.create_bar_chart_ForTool(self.tab2, tool_data_x, tool_data_y,  ['使用工具'])

        pie_chart_data = [10, 20, 30, 25, 15]
        pie_chart_labels = ['碩士以上', '大學以上', '專科以上', '高中以上', '學歷不拘']
        chart.create_pie_chart(self.tab3, pie_chart_data, pie_chart_labels,['學歷要求'])
        
        num = [15, 25, 35]
        salary = [20, 10, 5]
        category = ['職務類別']
        chart.create_bar_chart_ForSalary(self.tab4, num, salary, category)

        exp_data = [10, 20, 30, 25, 15,20]
        exp_labels = ['五年以上','四年以上', '三年以上', '兩年以上', '一年以上', '不拘']
        chart.create_pie_chart(self.tab5, exp_data, exp_labels,['工作經歷'])

        # 在右側新增選項按鈕
        self.create_option_menu()

        # 新增主題選擇器
        #self.create_theme_selector()
    
    def create_option_menu(self):
        # 在右側新增一個框架來放置按鈕
        self.button_frame = tk.Frame(self.right_side_frame)
        self.button_frame.pack(side='right', fill='y')

        # image
        self.filter_icon = tk.PhotoImage(file=r"D:\Programming\Crawler\scrapy\ScrapyFor104\GUI\filter.png")
        self.option_button = tk.Button(self.button_frame, text="filter", command=self.toggle_options)
        self.option_button.config(image=self.filter_icon)
        self.option_button.pack(pady=20)
        
        # 建立可展開且隱藏的選項框架
        self.option_frame = tk.Frame(self.right_side_frame, bg='gray')     

        self.job_label = tk.Label(self.option_frame, text='職務類別', bg='gray')
       # self.job_label.grid(row=0, column=0, columnspan=2, padx=25, pady=3)
        self.job_label.pack()
        
        self.search_icon = tk.PhotoImage(file=r"D:\Programming\Crawler\scrapy\ScrapyFor104\GUI\search.png")
        self.search_btn = ttk.Button(self.option_frame, text="確定", style="success.Outline.TButton", command=self.update_chart)
        self.search_btn.config(image=self.search_icon)
        
        self.job_option = tk.Listbox(self.option_frame, selectmode=tk.MULTIPLE,height=8)
        job_menu = ['全部', 'AI工程师', 'Android工程师', 'BIOS工程师', 'FAE工程师', 'Internet程序设计师', 'iOS工程师', 'ISO／品保人员', 'MES工程师', 'MIS／网管主管', 'MIS程序设计师', 'MIS高阶主管', 'RF通讯工程师', 'UI设计师', 'UX设计师']
        for i in job_menu:
            self.job_option.insert(tk.END, i)
        #self.job_option.grid(row=1, column=0, columnspan=2, padx=25, pady=2)
        self.job_option.pack()

       # self.salary_label = tk.Label(self.option_frame, text='月薪範圍(k)', bg='gray')
        #self.salary_label.grid(row=2, column=0, columnspan=2, padx=25, pady=3)
        #self.salary_label.pack()
        self.exp_label = tk.Label(self.option_frame, text='工作經歷').pack(pady=5)
        self.exp_menu = ['五年以上','四年以上', '三年以上', '兩年以上', '一年以上', '不拘']
        self.exp_option1 = ttk.Combobox(self.option_frame, value=self.exp_menu, width=6)
        self.exp_option1.pack(pady=5)
        self.exp_option1.set('不拘')

        self.edu_label = tk.Label(self.option_frame, text='學歷').pack(pady=5)
        self.edu_menu = ['碩士以上', '大學以上', '專科以上', '高中以上', '學歷不拘']
        self.edu_option = ttk.Combobox(self.option_frame, value=self.edu_menu, width=8)
        self.edu_option.pack(pady=5)
        self.edu_option.set('學歷不拘')

        #self.salary_option2 = ttk.Combobox(self.option_frame, value=self.salary_menu, width=5)
       # self.salary_option2.grid(row=3, column=1, padx=5, pady=5)
       # self.salary_option2.set('None')
        #==============
        self.salary_meter1=tb.Meter(self.option_frame,metersize=120,
            padding=5,
            amountused=0,
            metertype="semi",
            stripethickness=10,
            amounttotal=150,
            subtext="月薪範圍",
            textright="k",
            interactive=True
        )
        self.salary_meter1.pack()
        self.salary_meter2=tb.Meter(self.option_frame,metersize=120,
            padding=5,
            amountused=0,
            metertype="semi",
            stripethickness=10,
            amounttotal=150,
            subtext="月薪範圍",
            textright="k",
            interactive=True
        )
        self.salary_meter2.pack()
        #==============
        self.testbtn = ttk.Button(self.option_frame, text="test", command=self.get_salary_range)
        self.testbtn.pack()

        self.tool_label  = tk.Label(self.option_frame, text='擅長工具').pack(pady=5)
        self.tool_option = tk.Listbox(self.option_frame, selectmode=tk.MULTIPLE,height=6)
        tool_menu = ['不拘','python', 'C++', 'js', 'css']
        for i in tool_menu:
            self.tool_option.insert(tk.END, i)
        self.tool_option.pack()

        self.search_btn.pack()

    def create_theme_selector(self):
        themes = self.style.theme_names()  # 取得所有可用主題
        self.theme_selector = ttk.Combobox(self.button_frame, values=themes)
        self.theme_selector.set(self.style.theme_use())  # 設定當前主題
        self.theme_selector.pack(pady=10)
        self.theme_selector.bind("<<ComboboxSelected>>", self.change_theme)

    def change_theme(self):
        selected_theme = self.theme_selector.get()
        self.style.theme_use(selected_theme)

    def get_salary_range(self):
        num1=int(self.salary_meter1.amountusedvar.get())
        num2=int(self.salary_meter2.amountusedvar.get())
        range = []
        if num1 >= num2:
            range.append(num2)
            range.append(num1)
        else:
            range.append(num1)
            range.append(num2)
        print(range)
        '''
        if self.salary_option1.get() != 'None':
            num1 = int(self.salary_option1.get())
        else:
            num1 = 0
        if self.salary_option2.get() != 'None':
            num2 = int(self.salary_option2.get())
        else:
            num2 = 0
        range = []
        if num1 >= num2:
            range.append(num2)
            range.append(num1)
        else:
            range.append(num1)
            range.append(num2)
        print(range)
        return range'''

    def toggle_options(self):
        if self.option_frame.winfo_viewable():
            self.option_frame.pack_forget()
        else:
            self.option_frame.pack(side='right', expand=True, fill="both")

    def update_chart(self):
        canvas = chart.canvas  
        if canvas is not None:
            canvas.get_tk_widget().pack_forget()
            canvas.get_tk_widget().destroy()
            chart.plt.close("all")

        chart.plt.rc("font", family="Microsoft Jhenghei")
        if not self.job_option.curselection():
            self.job_option.select_set(0)
        selected_indices = self.job_option.curselection()
        value = [self.job_option.get(idx) for idx in selected_indices]
        category = value

        self.option_frame.place_forget()

        for widget in self.tab2.winfo_children():
            widget.destroy()
        plot_data_x = [1, 2, 3, 4, 5]
        plot_data_y = [2, 6, 5, 7, 11]
        chart.create_bar_chart_ForTool(self.tab2, plot_data_x, plot_data_y, category)

        for widget in self.tab3.winfo_children():
            widget.destroy()
        pie_chart_data = [5, 10, 50, 30, 5]
        pie_chart_labels = ['碩士以上', '大學以上', '專科以上', '高中以上', '學歷不拘']
        chart.create_pie_chart(self.tab3, pie_chart_data, pie_chart_labels, category)
  
        for widget in self.tab4.winfo_children():
            widget.destroy()

        num = [15, 25, 35]
        salary = [20, 10, 5]
        chart.create_bar_chart_ForSalary(self.tab4, num, salary, category)

        for widget in self.tab5.winfo_children():
            widget.destroy()
        exp_data = [30, 10, 20, 15, 10,30]
        exp_labels = ['五年以上','四年以上', '三年以上', '兩年以上', '一年以上', '不拘']
        chart.create_pie_chart(self.tab5, exp_data, exp_labels, category)

if __name__ == "__main__":
    root = tb.Window(themename="vapor")  # 初始化視窗時設定主題
    gui = Gui(root)
   # root.bind("<space>",gui.update_chart)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()