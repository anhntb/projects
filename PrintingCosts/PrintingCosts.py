import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Tính chi phí in ấn")

# Tạo Notebook (dùng để chứa các tab)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Tạo các Frame cho từng tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Thêm các tab vào Notebook
notebook.add(tab1, text="Tính toán")
notebook.add(tab2, text="Chỉnh sửa")


################################################## TAB TÍNH CHI PHÍ IN ##################################################

# Đếm số trang trong file pdf
def count_pages(file_path):
    if file_path.endswith('.pdf'):
        try:
            reader = PdfReader(file_path)
            return len(reader.pages)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file PDF: {e}")
            return 0
    else:
        messagebox.showerror("Lỗi", "Định dạng file không được hỗ trợ. Vui lòng chọn file PDF")
        return 0

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")]) # Mở hộp thoại chỉ hiển thị file pdf cho người dùng chọn
    if file_path:
        num_pages = count_pages(file_path) # Đếm số trang 
        entry_pages.config(state='normal') # Cho phép chỉnh sửa 
        entry_pages.delete(0, tk.END) # Xóa nội dung hiện có trong ô
        entry_pages.insert(0, str(num_pages)) # Chèn nội dung mới
        entry_pages.config(state='readonly') # Khóa ô, không cho phép chỉnh sửa

# Tính chi phí
def calculate_cost():
    try:
        num_pages = int(entry_pages.get())
        num_pagesPerSide = int(combo_pagesPerSide.get())
        num_copies = int(spinbox_copies.get())
        is_twoSides = var_twoSides.get()

        # In 2 mặt
        twoSides_cost = 0.5 if is_twoSides else 1.0

        # Số tờ sẽ in
        num_sheets = num_pages / num_pagesPerSide * num_copies * twoSides_cost

        # Hệ số theo kích thước giấy 2^(4-X)
        scaleFactor_paperSize = 2 ** (4 - int(combo_paperSize.get()[1])) 

        # Giá theo loại giấy, loại mực, kích thước
        if var_paperType.get() == 0: # Giấy thường
            if var_inkType.get() == 0: # Mực đen
                if var_printingMethod.get() == 0: # UV
                    inkCost = int(entry_normal_black_UV.get()) # Thường - đen - UV
                else: 
                    inkCost = int(entry_normal_black_heatTransfer.get()) # Thường - đen - chuyển nhiệt
            else:
                if var_printingMethod.get() == 0: # UV
                    inkCost = int(entry_normal_color_UV.get()) # Thường - màu - UV
                else: 
                    inkCost = int(entry_normal_color_heatTransfer.get()) # Thường - màu - chuyển nhiệt  
        else:    
            if var_inkType.get() == 0: # Mực đen
                if var_printingMethod.get() == 0: # UV
                    inkCost = int(entry_couche_black_UV.get()) # Couche - đen - UV
                else: 
                    inkCost = int(entry_couche_black_heatTransfer.get()) # Couche - đen - chuyển nhiệt
            else:
                if var_printingMethod == 0: # UV
                    inkCost = int(entry_couche_color_UV.get()) # Couche - màu - UV
                else: 
                    inkCost = int(entry_couche_color_heatTransfer.get()) # Couche - màu - chuyển nhiệt

        # Giá khuyến mãi
        if var_paperType.get() == 0: # Giấy thường
            discounted_price = (1 - int(spinbox_normal_sale_value.get()) / 100) if num_sheets >= int(entry_normal_sale_quantity.get()) else 1.0
        else:
            discounted_price = (1 - int(spinbox_couche_sale_value.get()) / 100) if num_sheets >= int(entry_couche_sale_quantity.get()) else 1.0

        # Tính tổng chi phí
        total_cost = num_sheets * inkCost * scaleFactor_paperSize * discounted_price
        formatted_cost = "{:,}".format(int(total_cost))
        
        # Hiển thị kết quả
        result_label.config(text=f"Tổng chi phí: {formatted_cost} VND")
        return 0
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng upload file PDF.")
        return 1

# Nhãn và ô tổng số trang
label_pages = tk.Label(tab1, text="Tổng số lượng trang:")
label_pages.grid(row=0, column=0, sticky='e', padx=10, pady=30, columnspan=2)
entry_pages = tk.Entry(tab1, width=25, state='readonly')
entry_pages.grid(row=0, column=2, padx=10, pady=30, columnspan=2)

# Nút tải file
load_button = tk.Button(tab1, text="Tải file", command=load_file)
load_button.grid(row=0, column=4, sticky='w', padx=10, pady=30, columnspan=2)

# Số lượng trang trên 1 mặt in
label_pagesPerSide = tk.Label(tab1, text="Số trang trên 1 mặt in:")
label_pagesPerSide.grid(row=1, column=0, padx=10, pady=15)
combo_pagesPerSide = ttk.Combobox(tab1, width=10, values=[1, 2, 4, 8], state='readonly')
combo_pagesPerSide.grid(row=1, column=1, padx=10, pady=15)
combo_pagesPerSide.current(0)  # Đặt giá trị mặc định là 1

# Số bản copy
label_copies = tk.Label(tab1, text="Số bản sao:")
label_copies.grid(row=1, column=2, padx=10, pady=15)
spinbox_copies = tk.Spinbox(tab1, width=10, from_=1, to_=1000, increment=1)
spinbox_copies.grid(row=1, column=3, padx=10, pady=15)

# Size giấy
label_paperSize = tk.Label(tab1, text="Kích thước giấy:")
label_paperSize.grid(row=1, column=4, padx=10, pady=15)
combo_paperSize = ttk.Combobox(tab1, width=10, values=["A4", "A3", "A2", "A1", "A0"], state='readonly')
combo_paperSize.grid(row=1, column=5, padx=10, pady=15)
combo_paperSize.current(0)  # Đặt giá trị mặc định là A4

# Loại giấy
var_paperType=tk.IntVar(tab1, 0)
label_paperType = tk.Label(tab1, text="Loại giấy:")
label_paperType.grid(row=2, column=0, sticky='e', padx=10, pady=5)
radio_paperType_normal = tk.Radiobutton(tab1, text="Thường", value=0, variable=var_paperType)
radio_paperType_couche = tk.Radiobutton(tab1, text="Couche", value=1, variable=var_paperType)
radio_paperType_normal.grid(row=2, column=1, sticky='w', padx=10, pady=5)
radio_paperType_couche.grid(row=3, column=1, sticky='w', padx=10, pady=0)

# Loại mực: In màu, in thường
var_inkType=tk.IntVar(tab1, 0)
label_inkType = tk.Label(tab1, text="Loại mực:")
label_inkType.grid(row=2, column=2, sticky='e', padx=10, pady=5)
radio_inkType_black = tk.Radiobutton(tab1, text="Đen", value=0, variable=var_inkType)
radio_inkType_color = tk.Radiobutton(tab1, text="Màu", value=1, variable=var_inkType)
radio_inkType_black.grid(row=2, column=3, sticky='w', padx=10, pady=5)
radio_inkType_color.grid(row=3, column=3, sticky='w', padx=10, pady=0)

# Kỹ thuật in: UV, chuyển nhiệt
var_printingMethod=tk.IntVar(tab1, 0)
label_printingMethod = tk.Label(tab1, text="Kỹ thuật in:")
label_printingMethod.grid(row=2, column=4, sticky='e', padx=10, pady=5)
radio_printingMethod_black = tk.Radiobutton(tab1, text="UV", value=0, variable=var_printingMethod)
radio_printingMethod_color = tk.Radiobutton(tab1, text="Chuyển nhiệt", value=1, variable=var_printingMethod)
radio_printingMethod_black.grid(row=2, column=5, sticky='w', padx=10, pady=5)
radio_printingMethod_color.grid(row=3, column=5, sticky='w', padx=10, pady=0)

# In 1 hoặc 2 mặt
var_twoSides = tk.BooleanVar()
checkbox_twoSides = tk.Checkbutton(tab1, text="In 2 mặt giấy", variable=var_twoSides)
checkbox_twoSides.grid(row=4, columnspan=6, pady=15)

# Nút tính toán
calc_button = tk.Button(tab1, width=10, height=2, text="Tính", font=("Arial", 10, "bold"), command=calculate_cost)
calc_button.grid(row=5, columnspan=6, pady=15)

# Nhãn hiển thị kết quả
result_label = tk.Label(tab1, text="Tổng chi phí: 0 VND", font=("Arial", 14, "bold"))
result_label.grid(row=6, columnspan=6, pady=20)


################################################## TAB CHỈNH SỬA GIÁ ##################################################

# Tính lại chi phí
def update_cost():
    try:
        if calculate_cost() == 0:
            # Hiển thị kết quả
            messagebox.showinfo("Thông báo", "Đã tính lại chi phí, vui lòng xem ở tab Tính toán.")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng upload file PDF.")

# Giá mặc định
default_normal_sale_quantity = tk.StringVar(value="50")
default_normal_sale_value = tk.StringVar(value="10")
default_normal_black_UV = tk.StringVar(value="200")
default_normal_black_heatTransfer = tk.StringVar(value="300")
default_normal_color_UV = tk.StringVar(value="500")
default_normal_color_heatTransfer = tk.StringVar(value="700")

default_couche_sale_quantity = tk.StringVar(value="30")
default_couche_sale_value = tk.StringVar(value="10")
default_couche_black_UV = tk.StringVar(value="600")
default_couche_black_heatTransfer = tk.StringVar(value="800")
default_couche_color_UV = tk.StringVar(value="1500")
default_couche_color_heatTransfer = tk.StringVar(value="1800")

# Giấy thường
label_normal = tk.Label(tab2, text="Giấy thường", font=("Arial", 14, "bold"))
label_normal.grid(row=0, column=0, padx=10, pady=20, columnspan=2)

label_normal_sale_quantity = tk.Label(tab2, text="Số tờ tối thiểu để nhận KM:")
label_normal_sale_quantity.grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_normal_sale_quantity = tk.Entry(tab2, width=10, state='normal', textvariable=default_normal_sale_quantity)
entry_normal_sale_quantity.grid(row=1, column=1, padx=10, pady=5, sticky='w')

label_normal_sale_value = tk.Label(tab2, text="Giá trị khuyến mãi (%):")
label_normal_sale_value.grid(row=2, column=0, padx=10, pady=5, sticky='w')
spinbox_normal_sale_value = tk.Spinbox(tab2, width=10, from_=0, to_=100, increment=1, textvariable=default_normal_sale_value)
spinbox_normal_sale_value.grid(row=2, column=1, padx=10, pady=5, sticky='w')

label_inkType_method = tk.Label(tab2, text="Giá theo loại mực - kỹ thuật in", font=("Arial", 10, "bold"))
label_inkType_method.grid(row=3, column=0, padx=10, pady=15, columnspan=2)

label_normal_black_UV = tk.Label(tab2, text="Đen - UV (vnd):")
label_normal_black_UV.grid(row=4, column=0, padx=10, pady=5)
entry_normal_black_UV = tk.Entry(tab2, width=15, state='normal', textvariable=default_normal_black_UV)
entry_normal_black_UV.grid(row=4, column=1, padx=10, pady=5)

label_normal_black_heatTransfer = tk.Label(tab2, text="Đen - Chuyển nhiệt (vnd):")
label_normal_black_heatTransfer.grid(row=5, column=0, padx=10, pady=5)
entry_normal_black_heatTransfer = tk.Entry(tab2, width=15, state='normal', textvariable=default_normal_black_heatTransfer)
entry_normal_black_heatTransfer.grid(row=5, column=1, padx=10, pady=5)

label_normal_color_UV = tk.Label(tab2, text="Màu - UV (vnd):")
label_normal_color_UV.grid(row=6, column=0, padx=10, pady=5)
entry_normal_color_UV = tk.Entry(tab2, width=15, state='normal', textvariable=default_normal_color_UV)
entry_normal_color_UV.grid(row=6, column=1, padx=10, pady=5)

label_normal_color_heatTransfer = tk.Label(tab2, text="Màu - Chuyển nhiệt (vnd):")
label_normal_color_heatTransfer.grid(row=7, column=0, padx=10, pady=5)
entry_normal_color_heatTransfer = tk.Entry(tab2, width=15, state='normal', textvariable=default_normal_color_heatTransfer)
entry_normal_color_heatTransfer.grid(row=7, column=1, padx=10, pady=5)

# Couche
label_couche = tk.Label(tab2, text="Giấy Couche", font=("Arial", 14, "bold"))
label_couche.grid(row=0, column=2, padx=10, pady=20, columnspan=2)

label_couche_sale_quantity = tk.Label(tab2, text="Số tờ tối thiểu để nhận KM:")
label_couche_sale_quantity.grid(row=1, column=2, padx=10, pady=5, sticky='w')
entry_couche_sale_quantity = tk.Entry(tab2, width=10, state='normal', textvariable=default_couche_sale_quantity)
entry_couche_sale_quantity.grid(row=1, column=3, padx=10, pady=5, sticky='w')

label_couche_sale_value = tk.Label(tab2, text="Giá trị khuyến mãi (%):")
label_couche_sale_value.grid(row=2, column=2, padx=10, pady=5, sticky='w')
spinbox_couche_sale_value = tk.Spinbox(tab2, width=10, from_=0, to_=100, increment=1, textvariable=default_couche_sale_value)
spinbox_couche_sale_value.grid(row=2, column=3, padx=10, pady=5, sticky='w')

label_inkType_method = tk.Label(tab2, text="Giá theo loại mực - kỹ thuật in", font=("Arial", 10, "bold"))
label_inkType_method.grid(row=3, column=2, padx=10, pady=15, columnspan=2)

label_couche_black_UV = tk.Label(tab2, text="Đen - UV (vnd):")
label_couche_black_UV.grid(row=4, column=2, padx=10, pady=5)
entry_couche_black_UV = tk.Entry(tab2, width=15, state='normal', textvariable=default_couche_black_UV)
entry_couche_black_UV.grid(row=4, column=3, padx=10, pady=5)

label_couche_black_heatTransfer = tk.Label(tab2, text="Đen - Chuyển nhiệt (vnd):")
label_couche_black_heatTransfer.grid(row=5, column=2, padx=10, pady=5)
entry_couche_black_heatTransfer = tk.Entry(tab2, width=15, state='normal', textvariable=default_couche_black_heatTransfer)
entry_couche_black_heatTransfer.grid(row=5, column=3, padx=10, pady=5)

label_couche_color_UV = tk.Label(tab2, text="Màu - UV (vnd):")
label_couche_color_UV.grid(row=6, column=2, padx=10, pady=5)
entry_couche_color_UV = tk.Entry(tab2, width=15, state='normal', textvariable=default_couche_color_UV)
entry_couche_color_UV.grid(row=6, column=3, padx=10, pady=5)

label_couche_color_heatTransfer = tk.Label(tab2, text="Màu - Chuyển nhiệt (vnd):")
label_couche_color_heatTransfer.grid(row=7, column=2, padx=10, pady=5)
entry_couche_color_heatTransfer = tk.Entry(tab2, width=15, state='normal', textvariable=default_couche_black_heatTransfer)
entry_couche_color_heatTransfer.grid(row=7, column=3, padx=10, pady=5)

# Nút cập nhật -> giá sẽ được tính lại ở tab "Tính toán"
calc_button = tk.Button(tab2, width=10, height=2, text="Cập nhật", font=("Arial", 10, "bold"), command=update_cost)
calc_button.grid(row=8, columnspan=6, pady=15)

# Chạy ứng dụng
root.mainloop()
