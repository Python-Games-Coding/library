import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, END
import os

# 检查并创建配置文件夹和借阅书籍文件
def check_and_create_config(base_folder):
    config_folder = os.path.join(base_folder, "config")
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    
    config_file = os.path.join(config_folder, "borrow_books.txt")
    if not os.path.exists(config_file):
        with open(config_file, "w", encoding="utf-8") as file:
            file.write("")
    return config_file

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
base_folder = "C:/Users/Windows12.2Pro/Desktop/github project/library"  # 替换为你希望的绝对路径
config_file = check_and_create_config(base_folder)
borrowed_books = load_borrowed_books(config_file)
current_language = "en"  # 默认语言为英语

# 文本字典
texts = {
    "en": {
        "library_system": "Library System",  # 添加这行
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
        "change_language": "Change Language"
    },
    "zh": {
        "library_system": "图书管理系统",  # 添加这行
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
        "change_language": '切换语言'
    }
}

def switch_language():
    global current_language
    current_language = "zh" if current_language == "en" else "en"
    update_ui()

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

# 借书功能
def borrow_book():
    def next_step():
        book_name = entry.get()
        if not book_name:
            messagebox.showerror(texts[current_language]["error"], texts[current_language]["enter_book_name"])
            return
        
        book_path = f"books/{book_name}"
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
        
        # Check if the books directory exists, create it if it doesn't
        if not os.path.exists("books"):
            os.makedirs("books")
        
        window.destroy()
        step2()
    
    def step2():
        nonlocal total_pages
        
        def next_step():
            nonlocal total_pages
            try:
                total_pages = int(entry.get())
                if total_pages <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(texts[current_language]["error"], texts[current_language]["error_invalid_pages"])
                return
            
            window.destroy()
            step3(1)
        
        window = tk.Toplevel(root)
        window.title(texts[current_language]["create_book"])
        
        tk.Label(window, text=texts[current_language]["step2"], font=("Arial", 20)).pack(pady=10)
        entry = tk.Entry(window, font=("Arial", 20))
        entry.pack(pady=5)
        
        frame = tk.Frame(window)
        frame.pack(pady=10)
        
        tk.Button(frame, text=texts[current_language]["cancel"], font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
        tk.Button(frame, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)
    
    def step3(page):
        if page > total_pages:
            # Ensure 'books/' directory exists before attempting to write
            if not os.path.exists("books"):
                os.makedirs("books")
            
            with open(f"books/{book_name}", "w", encoding="utf-8") as file:
                for content in pages_content:
                    file.write(content + "\n")
            
            messagebox.showinfo(texts[current_language]["success_create"], texts[current_language]["success_create"])
            return
        
        def next_step():
            pages_content.append(entry.get())
            window.destroy()
            step3(page + 1)
        
        window = tk.Toplevel(root)
        window.title(texts[current_language]["create_book"])
        
        tk.Label(window, text=f"{texts[current_language]['step3']}{page}/{total_pages}页：", font=("Arial", 20)).pack(pady=10)
        entry = tk.Entry(window, font=("Arial", 20))
        entry.pack(pady=5)
        
        frame = tk.Frame(window)
        frame.pack(pady=10)
        
        tk.Button(frame, text=texts[current_language]["cancel"], font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
        tk.Button(frame, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)
    
    window = tk.Toplevel(root)
    window.title(texts[current_language]["create_book"])
    
    tk.Label(window, text=texts[current_language]["step1"], font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(window, font=("Arial", 20))
    entry.pack(pady=5)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text=texts[current_language]["cancel"], font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
    tk.Button(frame, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=step1).pack(side="right", padx=5)

# 阅读书籍功能
def read_book():
    def step1():
        book_name = entry.get()
        if not book_name:
            messagebox.showerror(texts[current_language]["error"], texts[current_language]["enter_book_name"])
            return
        
        book_path = f"books/{book_name}"
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
        step2(book_name)
    
    def step2(book_name):
        with open(f"books/{book_name}", "r", encoding="utf-8") as file:
            pages = file.read().splitlines()
        
        current_page = 0
        
        def show_page():
            text.delete(1.0, END)
            text.insert(END, pages[current_page])
        
        def next_page():
            nonlocal current_page
            if current_page < len(pages) - 1:
                current_page += 1
                show_page()
        
        def previous_page():
            nonlocal current_page
            if current_page > 0:
                current_page -= 1
                show_page()
        
        window = tk.Toplevel(root)
        window.title(texts[current_language]["read_book"])
        
        text = tk.Text(window, font=("Arial", 20), wrap="word")
        text.pack(expand=True, fill="both", pady=10)
        show_page()
        
        frame = tk.Frame(window)
        frame.pack(pady=10)
        
        tk.Button(frame, text=texts[current_language]["previous"], font=("Arial", 20), height=2, width=10, command=previous_page).pack(side="left", padx=5)
        tk.Button(frame, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=next_page).pack(side="right", padx=5)
    
    window = tk.Toplevel(root)
    window.title(texts[current_language]["read_book"])
    
    tk.Label(window, text=texts[current_language]["enter_book_name"], font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(window, font=("Arial", 20))
    entry.pack(pady=5)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text=texts[current_language]["cancel"], font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
    tk.Button(frame, text=texts[current_language]["next"], font=("Arial", 20), height=2, width=10, command=step1).pack(side="right", padx=5)

# 退出系统功能
def exit_system():
    root.destroy()

# 初始化主界面
root = tk.Tk()
root.title(texts[current_language]["library_system"])

borrow_button = tk.Button(root, text=texts[current_language]["borrow_book"], font=("Arial", 20), height=2, width=15, command=borrow_book)
borrow_button.pack(pady=10)

return_button = tk.Button(root, text=texts[current_language]["return_book"], font=("Arial", 20), height=2, width=15, command=return_book)
return_button.pack(pady=10)

view_button = tk.Button(root, text=texts[current_language]["view_account"], font=("Arial", 20), height=2, width=15, command=view_account)
view_button.pack(pady=10)

read_button = tk.Button(root, text=texts[current_language]["read_book"], font=("Arial", 20), height=2, width=15, command=read_book)
read_button.pack(pady=10)

create_button = tk.Button(root, text=texts[current_language]["create_book"], font=("Arial", 20), height=2, width=15, command=create_book)
create_button.pack(pady=10)

lang_button = tk.Button(root, text=texts[current_language]["change_language"], font=("Arial", 20), height=2, width=15, command=switch_language)
lang_button.pack(pady=10)

exit_button = tk.Button(root, text=texts[current_language]["exit"], font=("Arial", 20), height=2, width=15, command=exit_system)
exit_button.pack(pady=10)
root.mainloop()
