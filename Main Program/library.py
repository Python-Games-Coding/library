import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, END, Canvas
import os

# 检查并创建配置文件夹和借阅书籍文件
def check_and_create_config():
    config_folder = "config"
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    
    config_file = os.path.join(config_folder, "borrow_books.txt")
    if not os.path.exists(config_file):
        with open(config_file, "w", encoding="utf-8") as file:
            file.write("")
    return config_file

# 检查并创建书籍文件夹
def check_and_create_books_folder():
    books_folder = "books"
    if not os.path.exists(books_folder):
        os.makedirs(books_folder)
    return books_folder

# 读取借阅书籍列表
def load_borrowed_books(config_file):
    with open(config_file, "r", encoding="utf-8") as file:
        books = file.read().splitlines()
    return books

# 保存借阅书籍列表
def save_borrowed_books(config_file, books):
    with open(config_file, "w", encoding="utf-8") as file:
        file.write("\n".join(books))

# 初始化配置和全局变量
config_file = check_and_create_config()
books_folder = check_and_create_books_folder()
borrowed_books = load_borrowed_books(config_file)
current_language = "en"  # 默认语言为英语
page_text = "page"  # 默认语言为英语的页文本

# 文本字典
texts = {
    "en": {
        "library_system": "Library System",
        "borrow_book": "Borrow Book",
        "return_book": "Return Book",
        "view_account": "View Account",
        "create_book": "Create Book",
        "read_book": "Read Book",
        "exit": "Exit",
        "enter_book_name": "Please enter the book name",
        "error": "Error",
        "book_not_borrowed": "The book is not borrowed",
        "success_borrow": "Successfully borrowed the book",
        "success_return": "Successfully returned the book",
        "step1": "Please enter the book name",
        "step2": "Please enter the total number of pages",
        "step3": "Please enter the content of page ",
        "next": "Next",
        "previous": "Previous",
        "cancel": "Cancel",
        "complete": "Complete",
        "borrow_prompt": "The book is not borrowed. Would you like to borrow it?",
        "book_not_exist": "The book does not exist",
        "create_book_prompt": "The book does not exist, would you like to create it?",
        "borrow": "Borrow",
        "return": "Return",
        "view": "View",
        "create": "Create",
        "read": "Read",
        "error_invalid_pages": "Please enter a valid number of pages",
        "success_create": "Successfully created the book",
        "success_return": "Successfully returned the book", 
        "change_language": "Change Language", 
        "page": "page", 
        "version": "version", 
        "more_info": "More info please go to https://github.com/Python-Games-Coding/library", 
        "version_title": "Version: 1.0 Build1926"
    },
    "zh": {
        "library_system": "图书管理系统",
        "borrow_book": "借书",
        "return_book": "还书",
        "view_account": "查看账户",
        "create_book": "新建书籍",
        "read_book": "阅读书籍",
        "exit": "退出",
        "enter_book_name": "请输入书名",
        "error": "错误",
        "book_not_borrowed": "未借阅该书籍",
        "success_borrow": "成功借阅书籍",
        "success_return": "成功归还书籍",
        "step1": "请输入书名",
        "step2": "请输入该书籍一共有多少页",
        "step3": "请输入第",
        "next": "下一步",
        "previous": "上一步",
        "cancel": "取消",
        "complete": "完成",
        "borrow_prompt": "未借阅该书籍，是否借阅后再阅读？",
        "book_not_exist": "该书籍不存在",
        "create_book_prompt": "该书籍不存在，是否新建书籍？",
        "borrow": "借书",
        "return": "还书",
        "view": "查看",
        "create": "新建",
        "read": "阅读",
        "error_invalid_pages": "请输入有效的页数",
        "success_create": "成功新建书籍",
        "success_return": "成功归还书籍", 
        "change_language": '切换语言', 
        "page": "页", 
        "version": "版本", 
        'more_info': "更多信息请前往https://github.com/Python-Games-Coding/library查看", 
        "version_title": "版本号: 1.0 Build1926"
    }
}


def switch_language():
    global current_language, page_text
    current_language = "zh" if current_language == "en" else "en"
    update_ui()
    update_ui2()

def update_ui():
    global current_language
    root.title(texts[current_language]["library_system"])
    borrow_button.config(text=texts[current_language]["borrow_book"])
    return_button.config(text=texts[current_language]["return_book"])
    view_button.config(text=texts[current_language]["view_account"])
    create_button.config(text=texts[current_language]["create_book"])
    read_button.config(text=texts[current_language]["read_book"])
    exit_button.config(text=texts[current_language]["exit"])
    lang_button.config(text=texts[current_language]["change_language"])
    version_button.config(text=texts[current_language]["version"])

def update_ui2():
    global page_text
    page_text = texts[current_language]["page"]

# 借书功能
def borrow_book():
    def next_step():
        book_name = entry.get()
        if not book_name:
            messagebox.showerror(texts[current_language]["error"], texts[current_language]["enter_book_name"])
            return
        
        book_path = os.path.join(books_folder, book_name)
        if not os.path.exists(book_path):
            response = messagebox.askyesno(texts[current_language]["error"], texts[current_language]["create_book_prompt"])
            if response:
                create_book()
            return
        
        borrowed_books.append(book_name)
        save_borrowed_books(config_file, borrowed_books)
        messagebox.showinfo(texts[current_language]["success_borrow"], f"{texts[current_language]['success_borrow']}《{book_name}》")
        window.destroy()
    
    window = tk.Toplevel(root)
    window.title(texts[current_language]["borrow_book"])
    
    tk.Label(window, text=texts[current_language]["enter_book_name"], font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(window, font=("Arial", 20))
    entry.pack(pady=5)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text=texts[current_language]["cancel"], font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
    tk.Button(frame, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)

# 还书功能
def return_book():
    def next_step():
        book_name = entry.get()
        if book_name not in borrowed_books:
            messagebox.showerror(texts[current_language]["error"], texts[current_language]["book_not_borrowed"])
            return
        
        borrowed_books.remove(book_name)
        save_borrowed_books(config_file, borrowed_books)
        messagebox.showinfo(texts[current_language]["success_return"], f"{texts[current_language]['success_return']}《{book_name}》")
        window.destroy()
    
    window = tk.Toplevel(root)
    window.title(texts[current_language]["return_book"])
    
    tk.Label(window, text=texts[current_language]["enter_book_name"], font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(window, font=("Arial", 20))
    entry.pack(pady=5)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text=texts[current_language]["cancel"], font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
    tk.Button(frame, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)

# 查看账户功能
def view_account():
    window = tk.Toplevel(root)
    window.title(texts[current_language]["view_account"])
    
    listbox = Listbox(window, font=("Arial", 20))
    listbox.pack(pady=10)
    
    for book in borrowed_books:
        listbox.insert(END, book)
    
    tk.Button(window, text=texts[current_language]["exit"], font=("Arial", 20), height=2, width=10, command=window.destroy).pack(pady=10)

# 新建书籍功能
def create_book():
    book_name = None
    total_pages = 0
    pages_content = []
    
    def step1():
        nonlocal book_name
        book_name = entry.get()
        if not book_name:
            messagebox.showerror(texts[current_language]["error"], texts[current_language]["enter_book_name"])
            return
        frame1.pack_forget()
        step2()
    
    def step2():
        frame2.pack(pady=10)
    
    def step3():
        nonlocal total_pages
        try:
            total_pages = int(entry2.get())
            if total_pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(texts[current_language]["error"], texts[current_language]["error_invalid_pages"])
            return
        
        frame2.pack_forget()
        update_page_content(1)
    
    def update_page_content(current_page):
        if current_page > total_pages:
            save_book()
            return
        
        frame3.pack_forget()
        frame3.pack(pady=10)
        
        label_page.config(text=f"{page_text} {current_page}/{total_pages}")
        entry3.delete(1.0, END)
        
        if current_page <= len(pages_content):
            entry3.insert(END, pages_content[current_page - 1])
        
        def save_page_content():
            content = entry3.get(1.0, END).strip()
            if len(pages_content) >= current_page:
                pages_content[current_page - 1] = content
            else:
                pages_content.append(content)
            update_page_content(current_page + 1)
        
        button_frame3_next.config(command=save_page_content)
    
    def save_book():
        book_path = os.path.join(books_folder, book_name)
        with open(book_path, "w", encoding="utf-8") as file:
            for page in pages_content:
                file.write(page + "\n---\n")
        
        messagebox.showinfo(texts[current_language]["success_create"], f"{texts[current_language]['success_create']}《{book_name}》")
        window.destroy()
    
    window = tk.Toplevel(root)
    window.title(texts[current_language]["create_book"])
    
    # Step 1
    frame1 = tk.Frame(window)
    frame1.pack(pady=10)
    tk.Label(frame1, text=texts[current_language]["step1"], font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(frame1, font=("Arial", 20))
    entry.pack(pady=5)
    tk.Button(frame1, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=step1).pack(pady=10)
    
    # Step 2
    frame2 = tk.Frame(window)
    tk.Label(frame2, text=texts[current_language]["step2"], font=("Arial", 20)).pack(pady=10)
    entry2 = tk.Entry(frame2, font=("Arial", 20))
    entry2.pack(pady=5)
    tk.Button(frame2, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=step3).pack(pady=10)
    
    # Step 3
    frame3 = tk.Frame(window)
    label_page = tk.Label(frame3, text="", font=("Arial", 20))
    label_page.pack(pady=10)
    entry3 = tk.Text(frame3, font=("Arial", 20), height=10, width=40)
    entry3.pack(pady=5)
    button_frame3_next = tk.Button(frame3, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10)
    button_frame3_next.pack(pady=10)
    
    update_ui2()
    frame1.pack()

# 阅读书籍功能
def read_book():
    def next_step():
        book_name = entry.get()
        if not book_name:
            messagebox.showerror(texts[current_language]["error"], texts[current_language]["enter_book_name"])
            return
        
        book_path = os.path.join(books_folder, book_name)
        if not os.path.exists(book_path):
            response = messagebox.askyesno(texts[current_language]["error"], texts[current_language]["borrow_prompt"])
            if response:
                borrow_book()
            return
        
        if book_name not in borrowed_books:
            response = messagebox.askyesno(texts[current_language]["error"], texts[current_language]["borrow_prompt"])
            if response:
                borrow_book()
            return
        
        window.destroy()
        read_book_content(book_name, book_path)
    
    window = tk.Toplevel(root)
    window.title(texts[current_language]["read_book"])
    
    tk.Label(window, text=texts[current_language]["enter_book_name"], font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(window, font=("Arial", 20))
    entry.pack(pady=5)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text=texts[current_language]["cancel"], font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
    tk.Button(frame, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)

def read_book_content(book_name, book_path):
    with open(book_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    pages = content.split("\n---\n")
    total_pages = len(pages)
    
    def update_page(current_page):
        if current_page < 1 or current_page > total_pages:
            return
        
        label_page.config(text=f"{page_text} {current_page}/{total_pages}")
        text.delete(1.0, END)
        text.insert(END, pages[current_page - 1])
    
    def next_page():
        nonlocal current_page
        if current_page < total_pages:
            current_page += 1
            update_page(current_page)
    
    def previous_page():
        nonlocal current_page
        if current_page > 1:
            current_page -= 1
            update_page(current_page)
    
    current_page = 1
    
    window = tk.Toplevel(root)
    window.title(book_name)
    
    label_page = tk.Label(window, text="", font=("Arial", 20))
    label_page.pack(pady=10)
    
    text = tk.Text(window, font=("Arial", 20), height=15, width=60)
    text.pack(pady=10)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text=texts[current_language]["previous"], font=("Arial", 20), height=2, width=10, command=previous_page).pack(side="left", padx=5)
    tk.Button(frame, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=next_page).pack(side="right", padx=5)
    
    update_page(current_page)

def version():
    window = tk.Tk()
    window.title(texts[current_language]["version_title"])
    c = Canvas(window, width=710, height=600, bg='white')
    display = '                                             Version 1.0-Build1926\n'
    def Hi():
        window.destroy()
    info = c.create_text(0, 50, anchor='w', fill='black', font='Pristina 19 bold', text=display + texts[current_language]["more_info"])
    btn = tk.Button(window, text=texts[current_language]["exit"], command=Hi)
    btn.pack()
    c.pack()

# 初始化主窗口
root = tk.Tk()
root.title(texts[current_language]["library_system"])

# 主菜单按钮
borrow_button = tk.Button(root, text=texts[current_language]["borrow_book"], font=("Arial", 20), height=2, width=20, command=borrow_book)
borrow_button.pack(pady=10)
return_button = tk.Button(root, text=texts[current_language]["return_book"], font=("Arial", 20), height=2, width=20, command=return_book)
return_button.pack(pady=10)
view_button = tk.Button(root, text=texts[current_language]["view_account"], font=("Arial", 20), height=2, width=20, command=view_account)
view_button.pack(pady=10)
create_button = tk.Button(root, text=texts[current_language]["create_book"], font=("Arial", 20), height=2, width=20, command=create_book)
create_button.pack(pady=10)
read_button = tk.Button(root, text=texts[current_language]["read_book"], font=("Arial", 20), height=2, width=20, command=read_book)
read_button.pack(pady=10)

# 语言切换按钮
lang_button = tk.Button(root, text=texts[current_language]["change_language"], font=("Arial", 20), height=2, width=20, command=switch_language)
lang_button.pack(pady=10)

version_button = tk.Button(root, text=texts[current_language]["version"], font=("Arial", 20), height=2, width=20, command=version)
version_button.pack(pady=10)


exit_button = tk.Button(root, text=texts[current_language]["exit"], font=("Arial", 20), height=2, width=20, command=root.quit)
exit_button.pack(pady=10)



# 初始化UI
update_ui()

# 启动主循环
root.mainloop()
