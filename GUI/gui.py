import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from PIL import Image
Image.CUBIC = Image.BICUBIC
from ttkbootstrap.constants import *
import ScrollableFrame as sf
import chbox 
import chart
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

import sys
import os
# 獲取當前腳本所在目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
# 獲取上層目錄
parent_dir = os.path.dirname(current_dir)
# 將上層目錄添加到sys.path
sys.path.append(parent_dir)
# 現在可以導入上層目錄中的模組或包
from queryData.jobQuery import JobDatabase

# 獲取當前腳本所在的目錄
script_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(script_dir, 'images\\')

class Gui:
    def __init__(self, root,db):
        self.root = root
        self.root.title("GUI")
        self.root.geometry('1000x900+300+50')
        self.root.minsize(900, 800)
        self.root.maxsize(1800, 900)
        
        self.style = tb.Style("morph")  # 初始化為 cyborg 主題

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
        self.notebook.add(self.tab2, text="推薦工作")     
        # 創建 tab3
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="學歷要求")     
        # 創建 tab4
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="薪资待遇")
        # 創建 tab5
        self.tab5 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab5, text="工作經歷")
        # 創建 tab6
        self.tab6 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab6, text="使用工具")

#===預設圖表=====

#tab3=========
        edu_dic={'不拘':0, '博士':0, '碩士':0, '大學':0, '專科':0,  '高中':0, '高中以下':0}
        for i in data_list:
            if not i['education']:
                edu_dic['不拘']+=1
                continue
            for j in i['education']:
                edu_dic[j]+=1
        edu_labels = [k for k ,v in edu_dic.items() if v!=0]
        edu_data = [v for k,v in edu_dic.items() if v!=0] 
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
        exp_dic={'不拘':0, '1年以上':0, '2年以上':0, '3年以上':0, '4年以上':0, '5年以上':0, '6年以上':0, '7年以上':0, '8年以上':0, '10年以上':0}
        for i in data_list:
            if i['experience']==[]:
                exp_dic['不拘']+=1
                continue
            for j in i['experience']:
                exp_dic[j]+=1

        exp_labels = [k for k ,v in exp_dic.items() if v!=0]
        exp_data = [v for k,v in exp_dic.items() if v!=0] 
        chart.create_bar_chart_ForExp(self.tab5, exp_labels, exp_data,['工作經驗'])
#tab1=========
        sf.ScrollableFrame(self.tab1, data_list,salary_dic)
#tab6=========
        tool_dic={}         
        for i in data_list:
            if len(tool_dic)>=10:
                break
            for j in i['tool']:
                if j not in tool_dic:
                    tool_dic[j]=1
                else:
                    tool_dic[j]+=1

        tool_x=list(tool_dic.keys())    
        tool_y=list(tool_dic.values())    
        chart.create_bar_chart_ForTool(self.tab6, tool_x, tool_y, ['使用工具'])

        # 在右側新增選項按鈕
        self.create_option_menu()
        # 新增主題選擇器
        #self.create_theme_selector()
#推薦
        self.jobs = db.get_jobInfo_by_filter(
            category=None,
            skill=None,
            education=None,
            tool=None,
            experience=None,
            days=None,
            min_salary=None,
            max_salary=None,
            limit=None,
        )
        self.jobs = [j for j in self.jobs]
        self.jobs = pd.DataFrame(self.jobs)

        # 將列表轉換為字符串
        self.jobs['category'] = self.jobs['category'].apply(lambda x: ' '.join(x))
        self.jobs['skill'] = self.jobs['skill'].apply(lambda x: ' '.join(x))
        self.jobs['tool'] = self.jobs['tool'].apply(lambda x: ' '.join(x))

        # 將類別、技能和工具合併為一個文本列
        self.jobs['combined'] = self.jobs['category'] + ' ' + self.jobs['skill'] + ' ' + self.jobs['tool']

        # 計算TF-IDF特徵
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(self.jobs['combined'])

        # 計算餘弦相似度
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
#tab2=========
        job_id=data_list[0]['job_id']
        job_id_list=self.recommend(job_id,self.cosine_sim)
        recom_data_list=[]#推薦職缺資訊
        self.recom_job_id_list=[0,0,0,0,0]
        self.next=0
        for i in job_id_list:
            recom_data_list.append(db.get_jobInfo_by_id(i))
        sf.ScrollableFrame(self.tab2, recom_data_list,salary_dic)
        
    
    def recommend(self, job_id, cosine_sim, num_of_jobs=2):
        idx = self.jobs[self.jobs['job_id'] == job_id].index[0]  # 獲取工作的索引(dataframe的index)
        sim_scores = list(enumerate(cosine_sim[idx]))  # 獲取該工作的所有相似度
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_of_jobs*2]  # 取前5個相似的工作，0是自己
        job_indices = random.sample([i[0] for i in sim_scores], num_of_jobs)
        return [i for i in self.jobs['job_id'].iloc[job_indices]]
    
    def create_option_menu(self):
        # 在右側新增一個框架來放置按鈕
        self.button_frame = tk.Frame(self.right_side_frame)
        self.button_frame.pack(side='right', fill='y')

        # image
        self.button_icon1 = tk.PhotoImage(file=image_dir+"button_icon.png")
        self.button_icon2 = tk.PhotoImage(file=image_dir+"button_icon2.png")
        self.option_button = tk.Button(self.button_frame, text="filter", command=self.toggle_options)
        self.option_button.config(image=self.button_icon1)
        self.option_button.pack(fill='y',expand=True)
        
        # 建立可展開且隱藏的選項框架
        self.option_frame = tk.Frame(self.right_side_frame, bg='gray')     
        
        self.exp_label = tk.Label(self.option_frame, text='工作經歷',font=('Arial',15,'bold')).pack(pady=5)
        self.exp_menu = ['全部', '10年以上', '1年以上', '2年以上', '3年以上', '4年以上', '5年以上', '6年以上', '7年以上', '8年以上', '不拘']
        self.exp_option1 = ttk.Combobox(self.option_frame, value=self.exp_menu, width=8)
        self.exp_option1.pack(pady=5)
        self.exp_option1.set('全部')

        self.edu_label = tk.Label(self.option_frame, text='學歷',font=('Arial',15,'bold')).pack(pady=5)
        self.edu_menu = ['全部', '不拘', '博士', '碩士', '大學', '專科', '高中', '高中以下']

        self.edu_option = ttk.Combobox(self.option_frame, value=self.edu_menu, width=8)
        self.edu_option.pack(pady=5)
        self.edu_option.set('全部')
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
        self.start_updating_meter2_min()
        
   
        #==============
        self.job_label = tk.Label(self.option_frame, text='職務類別', bg='gray',font=('Arial',15,'bold'))
        self.job_label.pack()
        
        self.job_frame=tk.Frame(self.option_frame,width=200,height=100,bg='red',bd=1,relief='groove')
        self.job_frame.pack()
        self.job_menu =[]
        self.job_menu = db.get_all_categories()
        self.job_option=chbox.ScrollableCheckboxFrame(self.job_frame,200,100)
        for i in self.job_menu:
            self.job_option.add_checkbox(i)

        self.tool_label  = tk.Label(self.option_frame, text='擅長工具',font=('Arial',15,'bold')).pack(pady=5)
      
        self.tool_frame=tk.Frame(self.option_frame,width=200,height=100,bd=1,relief='groove')
        self.tool_frame.pack()
        self.tool_menu = []
        self.tool_menu = db.get_all_tools()
        self.tool_option=chbox.ScrollableCheckboxFrame(self.tool_frame,200,100)
        for i in self.tool_menu:
            self.tool_option.add_checkbox(i)

        self.search_icon = tk.PhotoImage(file=image_dir+"search_icon9.png")
        self.search_btn = ttk.Button(self.option_frame, text="確定", style="success.Outline.TButton", command=self.update_chart)
        self.search_btn.config(image=self.search_icon)
        self.search_btn.pack()

        
    def start_updating_meter2_min(self):
        self.update_meter2_min()
        self.root.after(100, self.start_updating_meter2_min)
        
    def update_meter2_min(self):
        min_salary1 = self.salary_meter1.amountusedvar.get()
        if self.salary_meter2.amountusedvar.get() < min_salary1:
            self.salary_meter2.amountusedvar.set(min_salary1)
            
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
        if requirements['education']=='全部':
            requirements['education']=None
        requirements['experience']=self.exp_option1.get() #取得經驗條件
        if requirements['experience']=='全部':
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
            self.option_button.config(image=self.button_icon1)
        else:
            self.option_frame.pack(side='right', expand=True, fill="both")
            self.option_button.config(image=self.button_icon2)

    def update_chart(self):
        chart.plt.rc("font", family="Microsoft Jhenghei")
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
#取得職缺資訊
        data_list = []
        jobs = db.get_jobInfo_by_filter(category=category_filter, skill=None, education=edu, experience=exp, tool=tool,
            days=None, min_salary=min_salary, max_salary=max_salary)#,limit=10)
        for i, j in enumerate(jobs):
            data_list.append(j)
#學歷 
        for widget in self.tab3.winfo_children(): 
            widget.destroy()
 
        edu_dic={'不拘':0, '博士':0, '碩士':0, '高中':0, '大學':0, '專科':0, '高中以下':0}
        for i in data_list:
            if i['education']==[]:
                edu_dic['不拘']+=1
                continue
            for j in i['education']:
                edu_dic[j]+=1

        edu_labels = [k for k ,v in edu_dic.items() if v!=0]
        edu_data = [v for k,v in edu_dic.items() if v!=0] 
        chart.create_pie_chart(self.tab3, edu_labels, edu_data, category)
#月薪  
        for widget in self.tab4.winfo_children():   
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
#工作經驗
        for widget in self.tab5.winfo_children():   
            widget.destroy()
        exp_dic={'不拘':0, '1年以上':0, '2年以上':0, '3年以上':0, '4年以上':0, '5年以上':0, '6年以上':0, '7年以上':0, '8年以上':0, '10年以上':0}
        for i in data_list:
            if i['experience']==[]:
                exp_dic['不拘']+=1
                continue
            for j in i['experience']:
                exp_dic[j]+=1

        exp_labels = [k for k ,v in exp_dic.items() if v!=0]
        exp_data = [v for k,v in exp_dic.items() if v!=0] 
        chart.create_bar_chart_ForExp(self.tab5, exp_labels, exp_data, category)
#使用工具        
        for widget in self.tab6.winfo_children(): 
            widget.destroy()

        tool_dic={}

        for i in data_list:
            for j in i['tool']:
                if j in tool_dic:
                    tool_dic[j]+=1
                elif len(tool_dic)<=15:
                    tool_dic[j]=1
                else:
                    continue
        tool_x=list(tool_dic.keys())    
        tool_y=list(tool_dic.values())    
        chart.create_bar_chart_ForTool(self.tab6, tool_x, tool_y, category)
#更新職缺資訊        
        for widget in self.tab1.winfo_children():
            widget.destroy()
      #  print(data_list)
        sf.ScrollableFrame(self.tab1, data_list,salary_dic)
#推薦工作
        for widget in self.tab2.winfo_children():
            widget.destroy()

        

        job_id_index=random.randint(0,len(data_list))
        job_id=data_list[job_id_index]['job_id']
        self.recom_job_id_list[self.next]=job_id
        if self.next==4:
            self.next=0
        else:
            self.next+=1
        #print("recom_job_id_list")
        #print(self.recom_job_id_list)
        job_id_list=[] #要丟進recommend的id
        for i in self.recom_job_id_list:
            if i!=0:
                job_id_list+=self.recommend(i,self.cosine_sim)
       # print('job_id_list')
       # print(job_id_list)
        recom_data_list=[]#推薦職缺資訊 
        for i in job_id_list:
            recom_data_list.append(db.get_jobInfo_by_id(i))
        sf.ScrollableFrame(self.tab2, recom_data_list,salary_dic)

if __name__ == "__main__":
    db = JobDatabase(
        host='localhost',
        username='root',
        password='9879',
        database="jobdatabase"
    )
    root = tb.Window(themename="vapor")  # 初始化視窗時設定主題
    gui = Gui(root, db)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()