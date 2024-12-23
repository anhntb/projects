import tkinter as tk
from tkinter import ttk

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng với Tab")

# Tạo Notebook (dùng để chứa các tab)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Tạo các Frame cho từng tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Thêm các tab vào Notebook
notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")

# Thêm widget vào tab1
label_tab1 = tk.Label(tab1, text="Đây là nội dung của Tab 1", font=("Arial", 14))
label_tab1.pack(padx=20, pady=20)

# Thêm widget vào tab2
label_tab2 = tk.Label(tab2, text="Đây là nội dung của Tab 2", font=("Arial", 14))
label_tab2.pack(padx=20, pady=20)

# Chạy ứng dụng
root.mainloop()
