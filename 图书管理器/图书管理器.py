import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, END
import os

# 全局变量，存储已借书籍的列表
my_books = []

# 检查文件夹是否存在，如果不存在则创建
def check_and_create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# 借书功能
def borrow_book():
    def next_step():
        book_name = entry.get()
        if not book_name:
            messagebox.showerror("错误", "请输入书名")
            return
        
        book_path = f"books/{book_name}"
        if not os.path.exists(book_path):
            response = messagebox.askyesno("提示", "该书籍不存在，是否新建书籍？")
            if response:
                create_book()
            return
        
        my_books.append(book_name)
        messagebox.showinfo("成功", f"成功借阅《{book_name}》")
        window.destroy()
    
    window = tk.Toplevel(root)
    window.title("借书")
    
    tk.Label(window, text="请输入书名", font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(window, font=("Arial", 20))
    entry.pack(pady=5)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text="取消", font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
    tk.Button(frame, text="下一步", font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)

# 还书功能
def return_book():
    def next_step():
        book_name = entry.get()
        if book_name not in my_books:
            messagebox.showerror("错误", "未借阅该书籍")
            return
        
        my_books.remove(book_name)
        messagebox.showinfo("成功", f"成功归还《{book_name}》")
        window.destroy()
    
    window = tk.Toplevel(root)
    window.title("还书")
    
    tk.Label(window, text="请输入书名", font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(window, font=("Arial", 20))
    entry.pack(pady=5)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text="取消", font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
    tk.Button(frame, text="下一步", font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)

# 查看账户功能
def view_account():
    window = tk.Toplevel(root)
    window.title("查看账户")
    
    listbox = Listbox(window, font=("Arial", 20))
    listbox.pack(pady=10)
    
    for book in my_books:
        listbox.insert(END, book)
    
    tk.Button(window, text="退出", font=("Arial", 20), height=2, width=10, command=window.destroy).pack(pady=10)

# 新建书籍功能
def create_book():
    book_name = None
    total_pages = 0
    pages_content = []
    
    def step1():
        nonlocal book_name
        book_name = entry.get()
        if not book_name:
            messagebox.showerror("错误", "请输入书名")
            return
        
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
                messagebox.showerror("错误", "请输入有效的页数")
                return
            
            window.destroy()
            step3(1)
        
        window = tk.Toplevel(root)
        window.title("新建书籍")
        
        tk.Label(window, text="请输入该书籍一共有多少页", font=("Arial", 20)).pack(pady=10)
        entry = tk.Entry(window, font=("Arial", 20))
        entry.pack(pady=5)
        
        frame = tk.Frame(window)
        frame.pack(pady=10)
        
        tk.Button(frame, text="上一步", font=("Arial", 20), height=2, width=10, command=lambda: [window.destroy(), create_book()]).pack(side="left", padx=5)
        tk.Button(frame, text="下一步", font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)
    
    def step3(page_num):
        nonlocal pages_content
        
        def next_step():
            content = text.get("1.0", END).strip()
            if not content:
                messagebox.showerror("错误", "请输入内容")
                return
            
            pages_content.append(content)
            if page_num == total_pages:
                save_book()
                window.destroy()
            else:
                window.destroy()
                step3(page_num + 1)
        
        window = tk.Toplevel(root)
        window.title(f"新建书籍 - 第{page_num}页")
        
        tk.Label(window, text=f"请输入第{page_num}页内容", font=("Arial", 20)).pack(pady=10)
        text = tk.Text(window, width=40, height=10, font=("Arial", 20))
        text.pack(pady=5)
        
        frame = tk.Frame(window)
        frame.pack(pady=10)
        
        if page_num == 1:
            tk.Button(frame, text="上一步", font=("Arial", 20), height=2, width=10, command=lambda: [window.destroy(), step2()]).pack(side="left", padx=5)
        else:
            tk.Button(frame, text="上一步", font=("Arial", 20), height=2, width=10, command=lambda: [window.destroy(), step3(page_num - 1)]).pack(side="left", padx=5)
        
        if page_num == total_pages:
            tk.Button(frame, text="完成", font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)
        else:
            tk.Button(frame, text="下一步", font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)
    
    def save_book():
        check_and_create_folder("books")
        book_path = f"books/{book_name}"
        check_and_create_folder(book_path)
        
        for i, content in enumerate(pages_content, start=1):
            with open(f"{book_path}/{i}.txt", "w", encoding="utf-8") as file:
                file.write(content)
        
        messagebox.showinfo("成功", f"成功新建书籍《{book_name}》")
    
    window = tk.Toplevel(root)
    window.title("新建书籍")
    
    tk.Label(window, text="请输入书名", font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(window, font=("Arial", 20))
    entry.pack(pady=5)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text="取消", font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
    tk.Button(frame, text="下一步", font=("Arial", 20), height=2, width=10, command=step1).pack(side="right", padx=5)

# 阅读书籍功能
def read_book():
    def next_step():
        book_name = entry.get()
        if book_name not in my_books:
            response = messagebox.askyesno("提示", "该书籍未借阅，是否借阅？")
            if response:
                window.destroy()
                borrow_book()
            return
        
        window.destroy()
        read_pages(book_name)
    
    window = tk.Toplevel(root)
    window.title("阅读书籍")
    
    tk.Label(window, text="请输入书名", font=("Arial", 20)).pack(pady=10)
    entry = tk.Entry(window, font=("Arial", 20))
    entry.pack(pady=5)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    tk.Button(frame, text="取消", font=("Arial", 20), height=2, width=10, command=window.destroy).pack(side="left", padx=5)
    tk.Button(frame, text="下一步", font=("Arial", 20), height=2, width=10, command=next_step).pack(side="right", padx=5)

def read_pages(book_name):
    book_path = f"books/{book_name}"
    pages = sorted([f for f in os.listdir(book_path) if f.endswith('.txt') and f[:-4].isdigit()], key=lambda x: int(x[:-4]))
    current_page = 0
    
    save_path = os.path.join(book_path, "save.txt")
    if os.path.exists(save_path):
        with open(save_path, "r", encoding="utf-8") as f:
            current_page = int(f.read().strip())
    
    def update_text():
        with open(os.path.join(book_path, pages[current_page]), "r", encoding="utf-8") as f:
            text.delete("1.0", END)
            text.insert(END, f.read())
    
    def save_progress():
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(str(current_page))
        messagebox.showinfo("保存", "阅读进度已保存")
    
    def next_page():
        nonlocal current_page
        if current_page < len(pages) - 1:
            current_page += 1
            update_text()
            back_button.config(state=tk.NORMAL)
            if current_page == len(pages) - 1:
                next_button.config(text="结束阅读", command=window.destroy)
    
    def previous_page():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            update_text()
            next_button.config(text="下一页", state=tk.NORMAL)
            if current_page == 0:
                back_button.config(state=tk.DISABLED)
    
    window = tk.Toplevel(root)
    window.title(f"阅读书籍 - {book_name}")
    
    text = tk.Text(window, width=40, height=20, font=("Arial", 20))
    text.pack(pady=10)
    
    frame = tk.Frame(window)
    frame.pack(pady=10)
    
    back_button = tk.Button(frame, text="上一页", font=("Arial", 20), height=2, width=10, command=previous_page, state=tk.DISABLED)
    back_button.pack(side="left", padx=5)
    
    next_button = tk.Button(frame, text="下一页", font=("Arial", 20), height=2, width=10, command=next_page)
    next_button.pack(side="right", padx=5)
    
    tk.Button(window, text="保存阅读进度", font=("Arial", 20), height=2, width=20, command=save_progress).pack(pady=10)
    
    update_text()


# 主窗口
root = tk.Tk()
root.title("图书管理器")

tk.Button(root, text="借书", font=("Arial", 20), height=2, width=20, command=borrow_book).pack(pady=10)
tk.Button(root, text="还书", font=("Arial", 20), height=2, width=20, command=return_book).pack(pady=10)
tk.Button(root, text="阅读书籍", font=("Arial", 20), height=2, width=20, command=read_book).pack(pady=10)
tk.Button(root, text="查看账户", font=("Arial", 20), height=2, width=20, command=view_account).pack(pady=10)
tk.Button(root, text="新建书籍", font=("Arial", 20), height=2, width=20, command=create_book).pack(pady=10)

root.mainloop()
