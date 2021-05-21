from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv
from datetime import datetime


GUI = Tk()
GUI.title("โปรแกรมบันทึกค่าใช้จ่าย by Noo")
GUI.geometry("500x700+500+50")

###############MENU####################

menubar = Menu(GUI)
GUI.config(menu = menubar)

# File menu
filemenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = filemenu)
filemenu.add_command(label = "Import CSV")
filemenu.add_command(label = "Export to Googlesheet")

#Help
def About():
    messagebox.showinfo("About", "สวัสดีค่ะ โปรแกรมนี้คือโปรแกรมที่เกิดจากการเรียนกับลุง\nสนใจเรียนกับลงไหม?\nติดต่อลุงได้เลยค่ะ")

helpmenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Help", menu = helpmenu)
helpmenu.add_command(label = "About", command = About)

#Donate
donatemenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Donate", menu = donatemenu)

########################################

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand = 1)

icon_t1 = PhotoImage(file="wallet.png")
icon_t2 = PhotoImage(file="expenselist.png")


Tab.add(T1, text = f'{"เพิ่มค่าใช้จ่าย":^{30}}', image=icon_t1,compound="top")
Tab.add(T2, text= f'{"ค่าใช้จ่ายทั้งหมด":^{30}}', image = icon_t2, compound = "top")

F1 = Frame(T1)
# F1.place(x=100,y=50)
F1.pack()

days = {"Mon":"จันทร์",
        "Tue":"อังคาร",
        "Wed":"พุธ",
        "Thu":"พฤหัส",
        "Fri":"ศุกร์",
        "Sat":"เสาร์",
        "Sun":"อาทิตย์"}

def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    amount = v_amount.get()

    if expense == "":
        print("No Data")
        messagebox.showwarning("Error", "กรุณากรอกข้อมูลให้ครบ")
        return
    elif price == "":
        messagebox.showwarning("Error", "กรุณากรอกราคา")
        return
    elif amount == "":
        messagebox.showwarning("Error", "กรุณากรอกจำนวน")
        return

    try:
        total = int(price) * int(amount)
        print("รายการ : {} ราคา : {}".format(expense,price))
        print("จำนวน : {} รวมทั้งหมด : {} บาท".format(amount,total))

        text = "รายการ : {} ราคา : {}\n".format(expense,price)
        text = text + "จำนวน : {} รวมทั้งหมด : {} บาท".format(amount,total)
        v_result.set(text)


        v_expense.set("")
        v_price.set("")
        v_amount.set("")

        today = datetime.now().strftime("%a")
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt = days[today] + "-" + dt
        with open("savedata.csv","a",encoding="utf-8",newline="") as f:

            fw = csv.writer(f)
            data = [dt,expense,price,amount,total]
            fw.writerow(data)
        E1.focus()
        update_table()
    except Exception as e:
        print("ERROR",e)
        messagebox.showwarning("Error", "กรุณากรอกข้อมูลใหม่")
        v_expense.set("")
        v_price.set("")
        v_amount.set("")
        
GUI.bind("<Return>",Save)    
FONT1 = (None,20)

main_icon = PhotoImage(file="background.png")

Mainicon = Label(F1,image = main_icon)
Mainicon.pack()


#---------------------text1-------------------
L = ttk.Label(F1, text="รายการค่าใช้จ่าย",font=FONT1).pack()
v_expense=StringVar()
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()

#---------------------text2-------------------
L = ttk.Label(F1, text="ราคา (บาท)",font=FONT1).pack()
v_price=StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()

#---------------------text3-------------------
L = ttk.Label(F1, text="จำนวน",font=FONT1).pack()
v_amount=StringVar()
E3 = ttk.Entry(F1,textvariable=v_amount,font=FONT1)
E3.pack()

icon_b1 = PhotoImage(file = "save.png")

B2 = ttk.Button(F1,text =f'{"Save": >{10}}',image = icon_b1,compound ="left", command=Save)
B2.pack(ipadx=50,ipady=20, pady=20)

v_result = StringVar()
v_result.set("---------------------ผลลัพธ์------------------------")
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground = "green")
result.pack(pady=20)

#############################TAB2############################

def read_csv():
    with open("savedata.csv", newline="", encoding = "utf-8") as f:
        fr = csv.reader(f)
        data = list(fr)
    return data
        # print(data)
        # print("----------")
        # print(data[0][0])
        # for a,b,c,d,e in data:
        #     print(e)

# table
L = ttk.Label(T2, text = "ตารางแสดงผลลัพธ์ทั้งหมด", font = FONT1).pack(pady = 20)

header = ["วัน-เวลา","รายการ","ค่าใช้จ่าย","จำนวน","รวม"]
resulttable = ttk.Treeview(T2, columns = header, show = "headings", height = 20)
resulttable.pack()

# for i in range(len(header)):
#     resulttable.heading(header[i], text = header[i])

for h in header:
    resulttable.heading(h, text = h)

headerwidth = [150, 170, 80, 80, 80]
for h, w in zip(header, headerwidth):
    resulttable.column(h, width = w)

# resulttable.insert("", 1, value = ["จันทร์", "น้ำดื่ม", 30, 5, 150])
# resulttable.insert("", "end", value = ["อังคาร", "น้ำดื่ม", 30, 5, 150])


def update_table():
    resulttable.delete(*resulttable.get_children())
    # for c in resulttable.get_children():
    #     resulttable.delete(c)
    data = read_csv()
    for d in data:
        resulttable.insert("",0,value = d)

update_table()


GUI.bind("<Tab>" ,lambda x: E2.focus())
GUI.mainloop()
