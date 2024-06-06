import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from PIL import Image
Image.CUBIC = Image.BICUBIC
from ttkbootstrap.constants import *
import ScrollableFrame as sf
import chbox 
import chart
from jobQuery.jobAPI import JobDatabase

class Gui:
    def __init__(self, root,db):
        self.root = root
        self.root.title("GUI")
        self.root.geometry('1000x800+300+100')
        self.root.minsize(900, 800)
        self.root.maxsize(1800, 900)
        
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
        data_list = []
        for i in range(1,10):
            data_list.append(db.get_jobInfo_by_id(i))

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

#===預設圖表=====
#tab2=========
        tool_dic={}         
        for i in data_list:
            for j in i['tool']:
                if j not in tool_dic:
                    tool_dic[j]=1
                else:
                    tool_dic[j]+=1

        tool_x=list(tool_dic.keys())    
        tool_y=list(tool_dic.values())    
        chart.create_bar_chart_ForTool(self.tab2, tool_x, tool_y, ['使用工具'])
#tab3=========
        edu_dic={'不拘':0, '博士':0, '碩士':0, '大學':0, '專科':0,  '高中':0, '高中以下':0}
        edu_labels = ['不拘', '博士', '碩士', '大學', '專科',  '高中', '高中以下']
        for i in data_list:
            if i['education']==[]:
                edu_dic['不拘']+=1
                continue
            for j in i['education']:
                edu_dic[j]+=1

        edu_data=list(edu_dic.values())    
        chart.create_pie_chart(self.tab3, edu_labels, edu_data, ['學歷要求'])
#tab4==========
        salary_dic={15:0, 25:0, 35:0, 45:0, 55:0, 65:0, 75:0, 85:0,95:0,105:0,115:0,125:0,135:0,145:0} 
        for i in data_list:
            for j in range(15,155,10):
                if i['salary_max'] == 'inf':
                    max=160
                else:
                    max=i['salary_max']//1000
                if i['min_salary']//1000<=j and max>=j:
                    salary_dic[j]+=1
        salary_num=list(salary_dic.values())
        salary=list(salary_dic.keys())
        chart.create_bar_chart_ForSalary(self.tab4, salary, salary_num, ['薪資待遇'])
#tab5=============
        exp_dic={}                      
        for i in data_list:
            for j in i['experience']:
                if j not in exp_dic:
                    exp_dic[j]=1
                else:
                    exp_dic[j]+=1
        exp_labels=list(exp_dic.keys())
        exp_data=list(exp_dic.values())
        chart.create_pie_chart(self.tab5, exp_labels, exp_data, ['工作經歷'])
#tab1=========
        sf.ScrollableFrame(self.tab1, data_list,salary_dic)

        # 在右側新增選項按鈕
        self.create_option_menu()
        # 新增主題選擇器
        #self.create_theme_selector()
    
    def create_option_menu(self):
        # 在右側新增一個框架來放置按鈕
        self.button_frame = tk.Frame(self.right_side_frame)
        self.button_frame.pack(side='right', fill='y')

        # image
      #  self.filter_icon = tk.PhotoImage(file="C:\\Users\\user\\Desktop\\Gui\\filter_icon2.png")
        self.option_button = tk.Button(self.button_frame, text="filter", command=self.toggle_options)
       # self.option_button.config(image=self.filter_icon)
        self.option_button.pack(pady=20)
        
        # 建立可展開且隱藏的選項框架
        self.option_frame = tk.Frame(self.right_side_frame, bg='gray')     
        
        self.exp_label = tk.Label(self.option_frame, text='工作經歷',font=('Arial',15,'bold')).pack(pady=5)
        self.exp_menu = ['10年以上', '1年以上', '2年以上', '3年以上', '4年以上', '5年以上', '6年以上', '7年以上', '8年以上', '不拘']
        self.exp_option1 = ttk.Combobox(self.option_frame, value=self.exp_menu, width=8)
        self.exp_option1.pack(pady=5)
        self.exp_option1.set('不拘')

        self.edu_label = tk.Label(self.option_frame, text='學歷',font=('Arial',15,'bold')).pack(pady=5)
        self.edu_menu = ['不拘', '博士', '碩士', '大學', '專科', '高中', '高中以下']

        self.edu_option = ttk.Combobox(self.option_frame, value=self.edu_menu, width=8)
        self.edu_option.pack(pady=5)
        self.edu_option.set('不拘')
        #==============
        self.salary_meter1=tb.Meter(self.option_frame,metersize=120,
            padding=5,
            amountused=0,
            metertype="semi",
            stripethickness=10,
            amounttotal=150,
            subtext="月薪最小值",
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
            subtext="月薪最大值",
            textright="k",
            interactive=True
        )
        self.salary_meter2.pack()
        #==============
        self.job_label = tk.Label(self.option_frame, text='職務類別', bg='gray',font=('Arial',15,'bold'))
        self.job_label.pack()
        
        self.job_frame=tk.Frame(self.option_frame,width=200,height=100,bg='red')
        self.job_frame.pack()
        self.job_menu =[]
        self.job_menu = db.get_all_categories()
        self.job_option=chbox.ScrollableCheckboxFrame(self.job_frame,200,100)
        for i in self.job_menu:
            self.job_option.add_checkbox(i)

        self.tool_label  = tk.Label(self.option_frame, text='擅長工具',font=('Arial',15,'bold')).pack(pady=5)
      
        self.tool_frame=tk.Frame(self.option_frame,width=200,height=100,bg='red')
        self.tool_frame.pack()
        self.tool_menu = []
        self.tool_menu = db.get_all_tools()
        self.tool_option=chbox.ScrollableCheckboxFrame(self.tool_frame,200,100)
        for i in self.tool_menu:
            self.tool_option.add_checkbox(i)

      #  self.search_icon = tk.PhotoImage(file="C:\\Users\\user\\Desktop\\Gui\\search_icon8.png")
        self.search_btn = ttk.Button(self.option_frame, text="確定", style="success.Outline.TButton", command=self.update_chart)
     #   self.search_btn.config(image=self.search_icon)

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

    def get_salary_range(self):  # 取得月薪範圍
        num1=int(self.salary_meter1.amountusedvar.get())
        num2=int(self.salary_meter2.amountusedvar.get())
        range = []
        if num1 >= num2:
            range.append(num2)
            range.append(num1)
        else:
            range.append(num1)
            range.append(num2)
        return range

    def get_requirements(self):
        requirements={}
        requirements['education']=self.edu_option.get()  #取得學歷條件
        if requirements['education']=='不拘':
            requirements['education']=None
        requirements['experience']=self.exp_option1.get() #取得經驗條件
        if requirements['experience']=='不拘':
            requirements['experience']=None
        requirements['salary']=self.get_salary_range() #取得月薪範圍 月薪最小值:requirements['salary'][0], 最大值:[1]
        if requirements['salary'][0]==requirements['salary'][1]:
            requirements['salary'][0]=None
            requirements['salary'][1]=None
        category=self.job_option.get_selected_checkboxes()#取得職務類別條件
        if category==[]:
            category=['全部']
        requirements['category']=category
        requirements['tool']=self.tool_option.get_selected_checkboxes()
        if requirements['tool']==[]:
            requirements['tool']=None
        return requirements
       # print(requirements)

    def toggle_options(self):
        if self.option_frame.winfo_viewable():
            self.option_frame.pack_forget()
        else:
            self.option_frame.pack(side='right', expand=True, fill="both")

    def update_chart(self):
        chart.plt.rc("font", family="Microsoft Jhenghei")
      #  self.option_frame.place_forget()
        canvas = chart.canvas  
        if canvas is not None:
            canvas.get_tk_widget().pack_forget()
            canvas.get_tk_widget().destroy()
            chart.plt.close("all") 

        requirements=self.get_requirements()
        
        category=requirements['category']
        if category == ['全部']:
            category_filter=None
        else:
            category_filter=category
        edu=requirements['education']
        exp=requirements['experience']
        if requirements['salary'][0]==None:
           min_salary=None
        else: 
            min_salary=int(requirements['salary'][0])*1000
        if requirements['salary'][1]==None:
            max_salary=None
        else:
            max_salary=int(requirements['salary'][1])*1000
        tool=requirements['tool']


        data_list = []
        jobs = db.get_jobInfo_by_filter(category=category_filter, skill=None, education=edu, experience=exp, tool=tool,
            days=None, min_salary=min_salary, max_salary=max_salary,limit=10)
        for i, j in enumerate(jobs):
            data_list.append(j)

        
        for widget in self.tab2.winfo_children(): #使用工具
            widget.destroy()


        tool_dic={}
        for i in data_list:
            for j in i['tool']:
                if j not in tool_dic:
                    tool_dic[j]=1
                else:
                    tool_dic[j]+=1

        tool_x=list(tool_dic.keys())    
        tool_y=list(tool_dic.values())    

        chart.create_bar_chart_ForTool(self.tab2, tool_x, tool_y, category)

        for widget in self.tab3.winfo_children():  #學歷
            widget.destroy()
 
        edu_dic={'不拘':0, '博士':0, '碩士':0, '大學':0, '專科':0,  '高中':0, '高中以下':0}
        edu_labels = ['不拘', '博士', '碩士', '大學', '專科',  '高中', '高中以下']
        for i in data_list:
            if i['education']==[]:
                edu_dic['不拘']+=1
                continue
            for j in i['education']:
                edu_dic[j]+=1

        edu_data=list(edu_dic.values())
       
        chart.create_pie_chart(self.tab3, edu_labels, edu_data, category)
  
        for widget in self.tab4.winfo_children():   #月薪
            widget.destroy()

        salary_dic={15:0, 25:0, 35:0, 45:0, 55:0, 65:0, 75:0, 85:0, 95:0, 105:0, 115:0, 125:0, 135:0, 145:0}
        
        for i in data_list:
            if i['salary_max']!='inf':
                for j in range(15,155,10):    
                    if i['min_salary']//1000<=j and i['salary_max']//1000>=j:
                        salary_dic[j]+=1
        salary_num=list(salary_dic.values())
        salary=list(salary_dic.keys())

        chart.create_bar_chart_ForSalary(self.tab4, salary, salary_num, category)

        for widget in self.tab5.winfo_children():   #工作經驗
            widget.destroy()

        exp_dic={}
        for i in data_list:
            for j in i['experience']:
                if j not in exp_dic:
                    exp_dic[j]=1
                else:
                    exp_dic[j]+=1
        exp_labels=list(exp_dic.keys())
        exp_data=list(exp_dic.values())
        chart.create_pie_chart(self.tab5, exp_labels, exp_data, category)

        for widget in self.tab1.winfo_children():
            widget.destroy()
    #    print(data_list)
        sf.ScrollableFrame(self.tab1, data_list,salary_dic)

if __name__ == "__main__":
    db = JobDatabase(
        host='save-job-data.mysql.database.azure.com',
        username='azureruser',
        password='@C110152318',
        database="jobdatabase"
    )
    root = tb.Window(themename="vapor")  # 初始化視窗時設定主題
    gui = Gui(root,db)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()