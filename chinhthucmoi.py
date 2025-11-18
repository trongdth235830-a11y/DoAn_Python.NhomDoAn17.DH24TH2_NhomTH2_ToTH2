import tkinter as tk 
from tkinter import ttk, messagebox 
from tkcalendar import DateEntry 
import mysql.connector 

def connect_db(): 
    return mysql.connector.connect( 
        host="localhost", 
        user="root",        # thay bằng user MySQL của bạn 
        password="0965704430Tt",        # thay bằng password MySQL của bạn 
        database="qlcactuyendulich" 
    )

# ====== Hàm canh giữa cửa sổ ====== 
def center_window(win, w=700, h=500): 
    ws = win.winfo_screenwidth() 
    hs = win.winfo_screenheight() 
    x = (ws // 2) - (w // 2) 
    y = (hs // 2) - (h // 2) 
    win.geometry(f'{w}x{h}+{x}+{y}') 


# ====== các cửa sổ  ======
def qlcactuyendulich(parent):
    root = tk.Toplevel(parent) if parent is not None else tk.Tk()
    # ẩn menu cha khi mở cửa sổ con
    if parent is not None:
        try:
            parent.withdraw()
        except Exception:
            pass
    root.title("Quản lý các tuyến du lịch")
    center_window(root, 1000, 500)
    root.resizable(False, False)

    tree = None

    # ====== Tiêu đề ======
    lbl_title = tk.Label(root, text="QUẢN LÝ CÁC TUYẾN DU LỊCH", font=("Arial", 18, "bold"),bg = "#f2fa00") 
    lbl_title.pack(pady=10) 
    
    # ====== Frame nhập thông tin ====== 
    frame_info = tk.Frame(root) 
    frame_info.pack(pady=5, padx=10, fill="x") 
    
    tk.Label(frame_info, text="Mã tuyến").grid(row=0, column=0, padx=5, pady=5, 
    sticky="w") 
    entry_matuyen = tk.Entry(frame_info, width=15) 
    entry_matuyen.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Tên tuyến").grid(row=0, column=2, padx=5, pady=5, 
    sticky="w") 
    entry_tentuyen = tk.Entry(frame_info, width=15) 
    entry_tentuyen.grid(row=0, column=3, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Điểm xuất phát").grid(row=1, column=0, padx=5, pady=5, 
    sticky="w") 
    entry_diemxuatphat = tk.Entry(frame_info, width=15) 
    entry_diemxuatphat.grid(row=1, column=1, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Điểm đến").grid(row=1, column=2, padx=5, pady=5, 
    sticky="w") 
    entry_diemden = tk.Entry(frame_info, width=15) 
    entry_diemden.grid(row=1, column=3, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Loại hình").grid(row=1, column=4, padx=5, pady=5, 
    sticky="w") 
    cbb_loaihinh = ttk.Combobox(frame_info, values=[ 
        "Tour tự túc", "Tour trọn gói"
        ], width=12, state="readonly") 
    cbb_loaihinh.grid(row=1, column=5, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Thời gian").grid(row=0, column=4, padx=5, pady=5, 
    sticky="w") 
    entry_thoigian = tk.Entry(frame_info, width=15) 
    entry_thoigian.grid(row=0, column=5, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Giá tour").grid(row=1, column=6, padx=5, pady=5, 
    sticky="w") 
    entry_giatour = tk.Entry(frame_info, width=10) 
    entry_giatour .grid(row=1, column=7, padx=5, pady=5, sticky="w")

    def load_data(): 
        for row in tree.get_children(): 
            tree.delete(row) 
        conn = connect_db() 
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM tuyendulich") 
        for row in cursor.fetchall(): 
            tree.insert("", tk.END, values=row) 
        cursor.close() 
        conn.close()

    # ====== Bảng danh sách tuyến du lịch ====== 
    lbl_ds = tk.Label(root, text="Danh sách các tuyến du lịch", font=("Arial", 10, "bold")) 
    lbl_ds.pack(pady=5, anchor="w", padx=10) 
    
    columns = ("Mã tuyến", "Tên tuyến", "Điểm xuất phát", "Điểm đến", "Thời gian", "Loại hình", "Giá tour") 
    tree = ttk.Treeview(root, columns=columns, show="headings", height=10) 
    
    for col in columns: 
        tree.heading(col, text=col.capitalize()) 
    
    tree.column("Mã tuyến", width=60, anchor="center") 
    tree.column("Tên tuyến", width=100, anchor="center")
    tree.column("Điểm xuất phát", width=100, anchor="center") 
    tree.column("Điểm đến", width=100, anchor="center") 
    tree.column("Thời gian", width=100, anchor="center") 
    tree.column("Loại hình", width=80, anchor="center") 
    tree.column("Giá tour", width=100, anchor="center") 
    
    tree.pack(padx=10, pady=5, fill="both")
    load_data() 
    #====== Chức năng CRUD ====== 
    def clear_input(): 
        entry_matuyen.delete(0, tk.END) 
        entry_tentuyen.delete(0, tk.END) 
        entry_diemxuatphat.delete(0, tk.END) 
        entry_diemden.delete(0, tk.END) 
        entry_thoigian.delete(0, tk.END) 
        cbb_loaihinh.set('') 
        entry_giatour.delete(0, tk.END)
  
    def them_tdl(): 
        matuyen = entry_matuyen.get() 
        tentuyen = entry_tentuyen.get() 
        diemxuatphat = entry_diemxuatphat.get() 
        diemden = entry_diemden.get() 
        thoigian = entry_thoigian.get() 
        loaihinh = cbb_loaihinh.get() 
        giatour = entry_giatour.get() 
        
        if not (matuyen and tentuyen and diemxuatphat and diemden and thoigian and loaihinh and giatour): 
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin") 
            return 
        
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute( 
                "INSERT INTO tuyendulich (matuyen, tentuyen, diemxuatphat, diemden, thoigian, loaihinh, giatour) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                (matuyen, tentuyen, diemxuatphat, diemden, thoigian, loaihinh, giatour) 
            ) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Thêm tuyến du lịch thành công") 
            load_data() 
            clear_input() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Lỗi khi thêm tuyến du lịch: {err}") 
        finally: 
            cursor.close() 
            conn.close()
    def xoa_tdl(): 
        selected_item = tree.selection() 
        if not selected_item: 
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tuyến du lịch để xóa") 
            return 
        
        matuyen = tree.item(selected_item)["values"][0] 
        
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute("DELETE FROM tuyendulich WHERE matuyen = %s", (matuyen,)) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Xóa tuyến du lịch thành công") 
            load_data() 
            clear_input() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Lỗi khi xóa tuyến du lịch: {err}") 
        finally: 
            cursor.close() 
            conn.close()
    def sua_tdl():
        selected_item = tree.selection() 
        if not selected_item: 
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tuyến du lịch để sửa") 
            return 
        
        matuyen = entry_matuyen.get() 
        tentuyen = entry_tentuyen.get() 
        diemxuatphat = entry_diemxuatphat.get() 
        diemden = entry_diemden.get() 
        thoigian = entry_thoigian.get() 
        loaihinh = cbb_loaihinh.get() 
        giatour = entry_giatour.get() 
        
        if not (matuyen and tentuyen and diemxuatphat and diemden and thoigian and loaihinh and giatour): 
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin") 
            return 
        
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute( 
                "UPDATE tuyendulich SET tentuyen=%s, diemxuatphat=%s, diemden=%s, thoigian=%s, loaihinh=%s, giatour=%s WHERE matuyen=%s", 
                (tentuyen, diemxuatphat, diemden, thoigian, loaihinh, giatour, matuyen) 
            ) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Sửa tuyến du lịch thành công") 
            load_data() 
            clear_input() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Lỗi khi sửa tuyến du lịch: {err}") 
        finally: 
            cursor.close() 
            conn.close()
    def luu_tdl(): 
        matuyen = entry_matuyen.get()
        tentuyen = entry_tentuyen.get()
        diemxuatphat = entry_diemxuatphat.get()
        diemden = entry_diemden.get()
        thoigian = entry_thoigian.get()
        loaihinh = cbb_loaihinh.get()
        giatour = entry_giatour.get()
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("update tuyendulich set tentuyen=%s, diemxuatphat=%s, diemden=%s, thoigian=%s, loaihinh=%s, giatour=%s where matuyen=%s",
                    (tentuyen, diemxuatphat, diemden, thoigian, loaihinh, giatour, matuyen))
        conn.commit()
        conn.close()
        load_data()
        clear_input()

        # ====== Frame nút ====== 
    frame_btn = tk.Frame(root) 
    frame_btn.pack(pady=5) 
    
    tk.Button(frame_btn, text="Thêm", width=8, command=them_tdl).grid(row=0, column=0, 
    padx=5) 
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_tdl).grid(row=0, column=1, 
    padx=5) 
    tk.Button(frame_btn, text="Sửa", width=8, command=sua_tdl).grid(row=0, column=2, 
    padx=5) 
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, 
    column=3, padx=5) 
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_tdl).grid(row=0, column=4, 
    padx=5) 
    tk.Button(frame_btn, text="Thoát", width=8, command=root.destroy,bg = "#f80606").grid(row=0, 
    column=5, padx=5) 

    root.grab_set()
    root.wait_window()
    # hiện lại menu cha khi đóng cửa sổ con
    if parent is not None:
        try:
            parent.deiconify()
        except Exception:
            pass
    return root

def qlkhachhang(parent):
    root = tk.Toplevel(parent) if parent is not None else tk.Tk()
    if parent is not None:
        try:
            parent.withdraw()
        except Exception:
            pass
    root.title("Quản lý khách hàng")
    center_window(root, 800, 500)
    root.resizable(False, False)

        # ====== Tiêu đề ======
    lbl_title = tk.Label(root, text="QUẢN LÝ KHÁCH HÀNG", font=("Arial", 18, "bold"),bg = "#f87f06") 
    lbl_title.pack(pady=10) 

    frame_info = tk.Frame(root) 
    frame_info.pack(pady=5, padx=10, fill="x") 

    tk.Label(frame_info, text="Mã khách hàng").grid(row=0, column=0, padx=5, pady=5, 
    sticky="w") 
    entry_makhachhang = tk.Entry(frame_info, width=15) 
    entry_makhachhang.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Họ tên").grid(row=0, column=2, padx=5, pady=5, 
    sticky="w") 
    entry_hoten = tk.Entry(frame_info, width=15) 
    entry_hoten.grid(row=0, column=3, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Số điện thoại").grid(row=1, column=0, padx=5, pady=5, 
    sticky="w") 
    entry_sodienthoai = tk.Entry(frame_info, width=15) 
    entry_sodienthoai.grid(row=1, column=1, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Email").grid(row=1, column=2, padx=5, pady=5, 
    sticky="w") 
    entry_email = tk.Entry(frame_info, width=20) 
    entry_email.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Địa chỉ").grid(row=1, column=4, padx=5, pady=5, 
    sticky="w") 
    entry_diachi = tk.Entry(frame_info, width=15) 
    entry_diachi.grid(row=1, column=5, padx=5, pady=5, sticky="w")

    def load_data(): 
        for row in tree.get_children(): 
            tree.delete(row) 
        conn = connect_db() 
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM khachhang") 
        rows = cursor.fetchall() 
        for row in rows: 
            tree.insert("", tk.END, values=row) 
        cursor.close() 
        conn.close()

    # ====== Bảng danh sách phương tiện ======
    lbl_ds = tk.Label(root, text="Danh sách khách hàng", font=("Arial", 10, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10) 

    columns = ("Mã khách hàng", "Họ tên", "Số điện thoại", "Email", "Địa chỉ")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns: 
        tree.heading(col, text=col.capitalize()) 

    tree.column("Mã khách hàng", width=100, anchor="center") 
    tree.column("Họ tên", width=100, anchor="center") 
    tree.column("Số điện thoại", width=150, anchor="w")
    tree.column("Email", width=150, anchor="w") 
    tree.column("Địa chỉ", width=80, anchor="center")

    tree.pack(padx=10, pady=5, fill="both")

    #====== Chức năng CRUD ====== 
    def clear_input(): 
        entry_makhachhang.delete(0, tk.END) 
        entry_hoten.delete(0, tk.END) 
        entry_sodienthoai.delete(0, tk.END) 
        entry_email.delete(0, tk.END) 
        entry_diachi.delete(0, tk.END)

    def them_khachhang(): 
        makhachhang = entry_makhachhang.get() 
        hoten = entry_hoten.get() 
        sodienthoai = entry_sodienthoai.get() 
        email = entry_email.get() 
        diachi = entry_diachi.get() 
        
        if not (makhachhang and hoten and sodienthoai and email and diachi):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin khách hàng.")
            return 
        
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute( 
                "INSERT INTO khachhang (makhachhang, hoten, sodienthoai, email, diachi) VALUES (%s, %s, %s, %s, %s)", 
                (makhachhang, hoten, sodienthoai, email, diachi) 
            ) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Thêm khách hàng thành công.") 
            clear_input() 
            load_data() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Không thể thêm khách hàng. Lỗi: {err}") 
        finally: 
            cursor.close() 
            conn.close()

    def xoa_khachhang(): 
        selected_item = tree.selection() 
        if not selected_item: 
            messagebox.showwarning("Chú ý", "Vui lòng chọn khách hàng để xóa.") 
            return 
        makhachhang = tree.item(selected_item)["values"][0] 
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khách hàng mã {makhachhang}?") 
        if not confirm: 
            return 
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute("DELETE FROM khachhang WHERE makhachhang = %s", (makhachhang,)) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Xóa khách hàng thành công.") 
            load_data() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Không thể xóa khách hàng. Lỗi: {err}") 
        finally: 
            cursor.close() 
            conn.close()

    def sua_khachhang(): 
        selected_item = tree.selection() 
        if not selected_item: 
            messagebox.showwarning("Chú ý", "Vui lòng chọn khách hàng để sửa.") 
            return 
        makhachhang = entry_makhachhang.get() 
        hoten = entry_hoten.get() 
        sodienthoai = entry_sodienthoai.get() 
        email = entry_email.get() 
        diachi = entry_diachi.get() 
        
        if not (makhachhang and hoten and sodienthoai and email and diachi): 
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin khách hàng.") 
            return 
        
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute( 
                "UPDATE khachhang SET hoten=%s, sodienthoai=%s, email=%s, diachi=%s WHERE makhachhang=%s", 
                (hoten, sodienthoai, email, diachi, makhachhang) 
            ) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Cập nhật khách hàng thành công.") 
            clear_input() 
            load_data() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Không thể cập nhật khách hàng. Lỗi: {err}") 
        finally: 
            cursor.close() 
            conn.close()

    def luu_khachhang():
        makhachhang = entry_makhachhang.get() 
        hoten = entry_hoten.get() 
        sodienthoai = entry_sodienthoai.get() 
        email = entry_email.get() 
        diachi = entry_diachi.get() 
        
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("update khachhang set hoten=%s, sodienthoai=%s, email=%s, diachi=%s where makhachhang=%s",
                    (hoten, sodienthoai, email, diachi, makhachhang))
        conn.commit()
        conn.close()
        load_data()
        clear_input()

    # ====== Frame nút ======
    frame_btn = tk.Frame(root) 
    frame_btn.pack(pady=5) 

    tk.Button(frame_btn, text="Thêm", width=8, command=them_khachhang).grid(row=0, column=0, 
    padx=5) 
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_khachhang).grid(row=0, column=1, 
    padx=5) 
    tk.Button(frame_btn, text="Sửa", width=8, command=sua_khachhang).grid(row=0, column=2, 
    padx=5) 
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, 
    column=3, padx=5) 
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_khachhang).grid(row=0, column=4, 
    padx=5) 
    tk.Button(frame_btn, text="Thoát", width=8, command=root.destroy,bg = "#f80606").grid(row=0, 
    column=5, padx=5) 

    load_data()
    root.grab_set()
    root.wait_window()
    if parent is not None:
        try:
            parent.deiconify()
        except Exception:
            pass
    return root

def tuyenthamquan(parent):
    root = tk.Toplevel(parent) if parent is not None else tk.Tk()
    if parent is not None:
        try:
            parent.withdraw()
        except Exception:
            pass
    root.title("Quản lý các tuyến tham quan")
    center_window(root, 1000, 500)
    root.resizable(False, False)

    tree = None

    # ====== Tiêu đề ======
    lbl_title = tk.Label(root, text="QUẢN LÝ CÁC TUYẾN THAM QUAN", font=("Arial", 18, "bold"),bg = "#f806e4") 
    lbl_title.pack(pady=10) 

    frame_info = tk.Frame(root) 
    frame_info.pack(pady=5, padx=10, fill="x") 
    
    tk.Label(frame_info, text="Mã điểm").grid(row=0, column=0, padx=5, pady=5, 
    sticky="w") 
    entry_madiem = tk.Entry(frame_info, width=15) 
    entry_madiem.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Mã tuyến").grid(row=0, column=2, padx=5, pady=5, 
    sticky="w") 

    cbb_matuyen = ttk.Combobox(frame_info, width=15, state="readonly")
    cbb_matuyen.grid(row=0, column=3, padx=5, pady=5, sticky="w")
                     
    tk.Label(frame_info, text="Tên điểm").grid(row=1, column=0, padx=5, pady=5, 
    sticky="w") 
    entry_tendiem = tk.Entry(frame_info, width=15) 
    entry_tendiem.grid(row=1, column=1, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Địa chỉ").grid(row=1, column=2, padx=5, pady=5, 
    sticky="w") 
    entry_diachi = tk.Entry(frame_info, width=20) 
    entry_diachi.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Phí tham quan").grid(row=1, column=4, padx=5, pady=5, 
    sticky="w") 
    entry_phithamquan = tk.Entry(frame_info, width=15) 
    entry_phithamquan.grid(row=1, column=5, padx=5, pady=5, sticky="w") 

    def fetch_available_matuyen():
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT matuyen FROM tuyendulich")
            matuyens = [row[0] for row in cursor.fetchall()]
            conn.close()
            return matuyens
        return []

    def populate_combobox():
        # điền giá trị cho combobox mã tuyến
        available_matuyen = fetch_available_matuyen()
        cbb_matuyen['values'] = available_matuyen
        if available_matuyen:
           cbb_matuyen.current(0)
        else:
            cbb_matuyen.set('')

    # ====== Bảng danh sách tuyến tham quan ====== 
    lbl_ds = tk.Label(root, text="Danh sách các tuyến tham quan", font=("Arial", 10, "bold")) 
    lbl_ds.pack(pady=5, anchor="w", padx=10) 
    
    columns = ("Mã điểm", "Mã tuyến", "Tên điểm", "Địa chỉ", "Phí tham quan") 
    tree = ttk.Treeview(root, columns=columns, show="headings", height=10) 
    
    for col in columns: 
        tree.heading(col, text=col.capitalize()) 
    
    tree.column("Mã điểm", width=60, anchor="center") 
    tree.column("Mã tuyến", width=100, anchor="center")
    tree.column("Tên điểm", width=100, anchor="center") 
    tree.column("Địa chỉ", width=100, anchor="center") 
    tree.column("Phí tham quan", width=100, anchor="center") 
    
    tree.pack(padx=10, pady=5, fill="both")

    #====== Chức năng CRUD ====== 
    def clear_input(): 
        entry_madiem.delete(0, tk.END) 
        cbb_matuyen.set('')
        entry_tendiem.delete(0, tk.END)
        entry_diachi.delete(0, tk.END)
        entry_phithamquan.delete(0, tk.END)
    
    def load_data(): 
        nonlocal tree
        if tree is None: return
        for row in tree.get_children():
            tree.delete(row)
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                sql= """
                SELECT tq.madiem, tq.matuyen, tq.tendiem, tq.diachi, tq.phithamquan
                FROM diemthamquan tq
                JOIN tuyendulich td ON tq.matuyen = td.matuyen
                ORDER BY tq.madiem"""
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    tree.insert("", tk.END, values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Không thể tải dữ liệu.\nLỗi: {err}")
            finally:
                cursor.close()
                conn.close()

    def them_thamquan(): 
        madiem = entry_madiem.get() 
        matuyen = cbb_matuyen.get()
        tendiem = entry_tendiem.get() 
        diachi = entry_diachi.get()
        phithamquan = entry_phithamquan.get()

        if not (madiem and matuyen and tendiem and diachi and phithamquan): 
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.") 
            return
        conn = connect_db() 
        cursor = conn.cursor()
        try: 
            cursor.execute( 
                "INSERT INTO diemthamquan (madiem, matuyen, tendiem, diachi, phithamquan) VALUES (%s, %s, %s, %s, %s)", 
                (madiem, matuyen, tendiem, diachi, phithamquan) 
            ) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Thêm điểm tham quan thành công.") 
            clear_input() 
            load_data() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Không thể thêm điểm tham quan.\nLỗi: {err}") 
        finally: 
            cursor.close() 
            conn.close()
    def xoa_thamquan(): 
        selected_item = tree.selection() 
        if not selected_item: 
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn điểm tham quan để xóa.") 
            return 
        madiem = tree.item(selected_item)["values"][0] 
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute("DELETE FROM diemthamquan WHERE madiem = %s", (madiem,)) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Xóa điểm tham quan thành công.") 
            load_data() 
            clear_input() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Không thể xóa điểm tham quan.\nLỗi: {err}") 
        finally: 
            cursor.close() 
            conn.close()

    def sua_thamquan():
        selected_item = tree.selection() 
        if not selected_item: 
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn điểm tham quan để sửa.") 
            return
        
        madiem = entry_madiem.get()
        matuyen = cbb_matuyen.get()
        tendiem = entry_tendiem.get()
        diachi = entry_diachi.get()
        phithamquan = entry_phithamquan.get()
        if not (madiem and matuyen and tendiem and diachi and phithamquan): 
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.") 
            return
        conn = connect_db() 
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE diemthamquan SET matuyen=%s, tendiem=%s, diachi=%s, phithamquan=%s WHERE madiem=%s",
                (matuyen, tendiem, diachi, phithamquan, madiem)
            )
            conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật điểm tham quan thành công.")
            load_data()
            clear_input()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể cập nhật điểm tham quan.\nLỗi: {err}")
        finally:
            cursor.close()
            conn.close()
    def luu_thamquan(): 
        madiem = entry_madiem.get()
        matuyen = cbb_matuyen.get()
        tendiem = entry_tendiem.get()
        diachi = entry_diachi.get()
        phithamquan = entry_phithamquan.get()
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("update diemthamquan set matuyen=%s, tendiem=%s, diachi=%s, phithamquan=%s where madiem=%s", 
                    (matuyen, tendiem, diachi, phithamquan, madiem))
        conn.commit()
        conn.close()
        load_data()
        clear_input()
    # populate combobox mã tuyến khi mở cửa sổ
    
    # ====== Frame nút ====== 
    frame_btn = tk.Frame(root) 
    frame_btn.pack(pady=5) 
    
    tk.Button(frame_btn, text="Thêm", width=8, command=them_thamquan).grid(row=0, column=0, 
    padx=5) 
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_thamquan).grid(row=0, column=1, 
    padx=5) 
    tk.Button(frame_btn, text="Sửa", width=8, command=sua_thamquan).grid(row=0, column=2, 
    padx=5) 
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, 
    column=3, padx=5) 
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_thamquan).grid(row=0, column=4, 
    padx=5) 
    tk.Button(frame_btn, text="Thoát", width=8, command=root.destroy,bg = "#f80606").grid(row=0, 
    column=5, padx=5) 

    populate_combobox()
    load_data()
    root.grab_set()
    root.wait_window()
    if parent is not None:
        try:
            parent.deiconify()
        except Exception:
            pass
    return root

def qlphuongtien(parent):
    root = tk.Toplevel(parent) if parent is not None else tk.Tk()
    if parent is not None:
        try:
            parent.withdraw()
        except Exception:
            pass
    root.title("Quản lý các phương tiện")
    center_window(root, 1000, 500)
    root.resizable(False, False)

    tree = None

    # ====== Tiêu đề ======
    lbl_title = tk.Label(root, text="QUẢN LÝ CÁC PHƯƠNG TIỆN", font=("Arial", 18, "bold"),bg = "#6ff806") 
    lbl_title.pack(pady=10) 

    frame_info = tk.Frame(root) 
    frame_info.pack(pady=5, padx=10, fill="x") 

    tk.Label(frame_info, text="Mã phương tiện").grid(row=0, column=0, padx=5, pady=5, 
    sticky="w") 
    entry_maphuongtien = tk.Entry(frame_info, width=15) 
    entry_maphuongtien.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Mã tuyến").grid(row=0, column=2, padx=5, pady=5, 
    sticky="w") 
    cbb_matuyen = ttk.Combobox(frame_info, width=15, state="readonly")
    cbb_matuyen.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Tên phương tiện").grid(row=1, column=0, padx=5, pady=5, 
    sticky="w") 
    entry_tenphuongtien = tk.Entry(frame_info, width=15) 
    entry_tenphuongtien.grid(row=1, column=1, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Loại phương tiện").grid(row=1, column=2, padx=5, pady=5, 
    sticky="w") 
    entry_loaiphuongtien = tk.Entry(frame_info, width=20) 
    entry_loaiphuongtien.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Sức chứa").grid(row=1, column=4, padx=5, pady=5, 
    sticky="w") 
    entry_succhua = tk.Entry(frame_info, width=15) 
    entry_succhua.grid(row=1, column=5, padx=5, pady=5, sticky="w")

    def load_data(): 
        for row in tree.get_children(): 
            tree.delete(row) 
        conn = connect_db() 
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM phuongtien") 
        for row in cursor.fetchall(): 
            tree.insert("", tk.END, values=row) 
        cursor.close() 
        conn.close()

    # ====== Bảng danh sách phương tiện ======
    lbl_ds = tk.Label(root, text="Danh sách các phương tiện", font=("Arial", 10, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10) 

    columns = ("Mã phương tiện", "Mã tuyến", "Tên phương tiện", "Loại phương tiện", "Sức chứa")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns: 
        tree.heading(col, text=col.capitalize()) 

    tree.column("Mã phương tiện", width=60, anchor="center") 
    tree.column("Mã tuyến", width=100, anchor="center") 
    tree.column("Tên phương tiện", width=150, anchor="w")
    tree.column("Loại phương tiện", width=150, anchor="w") 
    tree.column("Sức chứa", width=80, anchor="center")

    tree.pack(padx=10, pady=4, fill="both")
    load_data()
    #====== Chức năng CRUD ====== 
    def clear_input(): 
        entry_maphuongtien.delete(0, tk.END) 
        cbb_matuyen.set('') 
        entry_tenphuongtien.delete(0, tk.END) 
        entry_loaiphuongtien.delete(0, tk.END) 
        entry_succhua.delete(0, tk.END)

    def them_phuongtien(): 
        maphuongtien = entry_maphuongtien.get() 
        matuyen = cbb_matuyen.get() 
        tenphuongtien = entry_tenphuongtien.get() 
        loaiphuongtien = entry_loaiphuongtien.get() 
        succhua = entry_succhua.get() 
        
        if not (maphuongtien and matuyen and tenphuongtien and loaiphuongtien and succhua):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return
        
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute( 
                "INSERT INTO phuongtien (maphuongtien, matuyen, tenphuongtien, loaiphuongtien, succhua) VALUES (%s, %s, %s, %s, %s)", 
                (maphuongtien, matuyen, tenphuongtien, loaiphuongtien, succhua) 
            ) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Thêm phương tiện thành công.") 
            clear_input() 
            load_data() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Không thể thêm phương tiện.\nLỗi: {err}") 
        finally: 
            cursor.close() 
            conn.close()

    def xoa_phuongtien(): 
        selected_item = tree.selection() 
        if not selected_item: 
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn phương tiện để xóa.") 
            return 
        maphuongtien = tree.item(selected_item)["values"][0] 
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute("DELETE FROM phuongtien WHERE maphuongtien = %s", (maphuongtien,)) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Xóa phương tiện thành công.") 
            load_data() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Không thể xóa phương tiện.\nLỗi: {err}") 
        finally: 
            cursor.close() 
            conn.close()

    def sua_phuongtien():
        selected_item = tree.selection() 
        if not selected_item: 
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn phương tiện để sửa.") 
            return 
        
        maphuongtien = entry_maphuongtien.get() 
        matuyen = cbb_matuyen.get() 
        tenphuongtien = entry_tenphuongtien.get() 
        loaiphuongtien = entry_loaiphuongtien.get() 
        succhua = entry_succhua.get() 
        
        if not (maphuongtien and matuyen and tenphuongtien and loaiphuongtien and succhua): 
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.") 
            return 
        
        conn = connect_db() 
        cursor = conn.cursor() 
        try: 
            cursor.execute( 
                "UPDATE phuongtien SET matuyen=%s, tenphuongtien=%s, loaiphuongtien=%s, succhua=%s WHERE maphuongtien=%s", 
                (matuyen, tenphuongtien, loaiphuongtien, succhua, maphuongtien) 
            ) 
            conn.commit() 
            messagebox.showinfo("Thành công", "Cập nhật phương tiện thành công.") 
            clear_input() 
            load_data() 
        except mysql.connector.Error as err: 
            messagebox.showerror("Lỗi", f"Không thể cập nhật phương tiện.\nLỗi: {err}") 
        finally: 
            cursor.close() 
            conn.close()

    def luu_phuongtien():
        maphuongtien = entry_maphuongtien.get()
        matuyen = cbb_matuyen.get()
        tenphuongtien = entry_tenphuongtien.get()
        loaiphuongtien = entry_loaiphuongtien.get()
        succhua = entry_succhua.get()
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("update phuongtien set matuyen=%s, tenphuongtien=%s, loaiphuongtien=%s, succhua=%s where maphuongtien=%s", 
                    (matuyen, tenphuongtien, loaiphuongtien, succhua, maphuongtien))
        conn.commit()
        conn.close()
        load_data()
        clear_input()

    def fetch_available_matuyen():
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT matuyen FROM tuyendulich")
            matuyens = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            return matuyens
        return []

    def populate_combobox():
        values = fetch_available_matuyen()
        cbb_matuyen['values'] = values
        if values:
            cbb_matuyen.current(0)
        else:
           cbb_matuyen.set('')

    populate_combobox()
    # ====== Frame nút ======
    frame_btn = tk.Frame(root) 
    frame_btn.pack(pady=5) 

    tk.Button(frame_btn, text="Thêm", width=8, command=them_phuongtien).grid(row=0, column=0, 
    padx=5) 
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_phuongtien).grid(row=0, column=1, 
    padx=5) 
    tk.Button(frame_btn, text="Sửa", width=8, command=sua_phuongtien).grid(row=0, column=2, 
    padx=5) 
    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, 
    column=3, padx=5) 
    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_phuongtien).grid(row=0, column=4, 
    padx=5) 
    tk.Button(frame_btn, text="Thoát", width=8, command=root.destroy,bg = "#f80606").grid(row=0, 
    column=5, padx=5)

    load_data()
    root.grab_set()
    root.wait_window()
    if parent is not None:
        try:
            parent.deiconify()
        except Exception:
            pass
    return root

def dattour(parent):
    root = tk.Toplevel(parent)
    if parent is not None:
        try:
            parent.withdraw()
        except Exception:
            pass
    root.title("Quản lý đặt tour")
    center_window(root, 1000, 500)
    root.resizable(False, False)

    tree = None

    #===== Hàm hỗ trợ ======
    def fetch_available_matuyen():
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT matuyen FROM tuyendulich")
            matuyens = [row[0] for row in cursor.fetchall()]
            conn.close()
            return matuyens
        return []

    def fetch_available_makhachhang():
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT makhachhang, hoten FROM khachhang")
            makhachhangs = cursor.fetchall()
            conn.close()
            return makhachhangs
        return []

    def populate_combobox():
        available_makhachhang = fetch_available_makhachhang()  # [(id, hoten), ...]
        available_matuyen = fetch_available_matuyen()

      # Hiển thị "makhachhang - họ tên" trong combobox
        kh_values = [f"{mk} - {ht}" for mk, ht in available_makhachhang]
        cbb_makhachhang['values'] = kh_values
        cbb_matuyen['values'] = available_matuyen

        if kh_values:
            cbb_makhachhang.current(0)
        else:
            cbb_makhachhang.set('Không có khách hàng đặt tour')
        if available_matuyen:
           cbb_matuyen.current(0)
        else:
            cbb_matuyen.set('Chưa có tuyến tham quan')

    # ====== Tiêu đề ======
    lbl_title = tk.Label(root, text="QUẢN LÝ ĐẶT TOUR", font=("Arial", 18, "bold"),bg = "#04c5f5")
    lbl_title.pack(pady=10)
    
    # ====== Tải dữ liệu ======
    def load_data():
        nonlocal tree
        if tree is None: return
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                sql= """
                SELECT dt.madattour, dt.makhachhang, dt.matuyen, dt.ngaydat, dt.songuoi
                FROM dattour dt
                JOIN khachhang kh ON dt.makhachhang = kh.makhachhang
                JOIN tuyendulich tl ON dt.matuyen = tl.matuyen
                ORDER by dt.madattour DESC
                """
                cursor.execute(sql)
                for row in cursor.fetchall():
                    row_list = list(row)
                    khachhang_name = f"{row_list[1]}{row_list[1]}"
                    tuyendulich_name = f"{row_list[2]}{row_list[2]}"
                    tree.insert("", tk.END, values=(row_list[0],
                     khachhang_name, 
                     tuyendulich_name, 
                     row_list[3], 
                     row_list[4])
                     )
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Không thể tải dữ liệu đặt tour.\nLỗi: {err}")
            finally:
                conn.close()


    # ====== Tạo đặt tour ======
    def dat_tour():
        makhachhang_raw = cbb_makhachhang.get()
        makhachhang = makhachhang_raw.split(' - ')[0] if ' - ' in makhachhang_raw else makhachhang_raw
        matuyen_raw = cbb_matuyen.get()
        matuyen = matuyen_raw.split(' - ')[0] if ' - ' in matuyen_raw else matuyen_raw
        ngaydat = date_entry.get_date()
        songuoi = entry_songuoi.get()
        ngaydat = date_entry.get_date()
        songuoi = entry_songuoi.get()
        madattour = entry_madattour.get()

        if not (makhachhang and matuyen and ngaydat and songuoi):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO dattour (madattour,makhachhang, matuyen, ngaydat, songuoi) VALUES (%s, %s, %s, %s, %s)",
                    (madattour,makhachhang, matuyen, ngaydat, songuoi)
                )
                conn.commit()
                messagebox.showinfo("Thành công", "Đặt tour thành công.")
                load_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Không thể đặt tour.\nLỗi: {err}")
            finally:
                conn.close()

    def xoa_tour():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn đặt tour để xóa.")
            return
        madattour = tree.item(selected_item)["values"][0]
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM dattour WHERE madattour = %s", (madattour,))
                conn.commit()
                messagebox.showinfo("Thành công", "Xóa đặt tour thành công.")
                load_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Không thể xóa đặt tour.\nLỗi: {err}")
            finally:
                conn.close()
    def sua_tour():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn đặt tour để sửa.")
            return
        madattour = tree.item(selected_item)["values"][0]
        makhachhang_raw = cbb_makhachhang.get()
        makhachhang = makhachhang_raw.split(' - ')[0] if ' - ' in makhachhang_raw else makhachhang_raw
        matuyen_raw = cbb_matuyen.get()
        matuyen = matuyen_raw.split(' - ')[0] if ' - ' in matuyen_raw else matuyen_raw
        ngaydat = date_entry.get_date()
        songuoi = entry_songuoi.get()

        if not (makhachhang and matuyen and ngaydat and songuoi):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE dattour SET makhachhang=%s, matuyen=%s, ngaydat=%s, songuoi=%s WHERE madattour=%s",
                    (makhachhang, matuyen, ngaydat, songuoi, madattour)
                )
                conn.commit()
                messagebox.showinfo("Thành công", "Cập nhật đặt tour thành công.")
                load_data()
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Không thể cập nhật đặt tour.\nLỗi: {err}")
            finally:
                conn.close()
  

    # ====== Frame thông tin ======
    frame_info = tk.Frame(root)
    frame_info.pack(pady=5, padx=10, fill="x")

    cbb_makhachhang = ttk.Combobox(frame_info, width=13, state= "readonly")
    cbb_matuyen= ttk.Combobox(frame_info, width=13, state= "readonly")
    date_entry = DateEntry(frame_info, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    
    tk.Label(frame_info, text="Mã đặt tour").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_madattour = tk.Entry(frame_info, width=15)
    entry_madattour.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="Khách đã đặt").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    cbb_makhachhang.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="Tuyến tham quan đã đặt").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    cbb_matuyen.grid(row=0, column=5, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="Ngày đặt").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="Số người").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_songuoi = tk.Entry(frame_info, width=15)
    entry_songuoi.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    
    # ====== Bảng danh sách đặt tour ======
    lbl_ds = tk.Label(root, text="Danh sách đặt tour", font=("Arial", 10, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10)
    columns = ("Mã đặt tour", "Khách hàng", "Tuyến tham quan", "Ngày đặt", "Số người")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column("Mã đặt tour", width=80, anchor="center")
        tree.column("Khách hàng", width=200, anchor="w")
        tree.column("Tuyến tham quan", width=200, anchor="w")
        tree.column("Ngày đặt", width=100, anchor="center")
        tree.column("Số người", width=80, anchor="center")
    tree.pack(padx=10, pady=5, fill="both")
    load_data()
    
    # ====== Frame nút ======
    frame_btn = tk.Frame(root)
    frame_btn.pack(pady=10)


    tk.Button(frame_btn, text="Đặt Tour", width=10, command=dat_tour,bg = "#0ac3f2").grid(row=0, column=0, padx=5)
    tk.Button(frame_btn, text="Sửa Tour", width=10, command=sua_tour,bg = "#07f73f").grid(row=0, column=1, padx=5)
    tk.Button(frame_btn, text="Hủy Tour", width=10, command=xoa_tour,bg = "#c6fb07").grid(row=0, column=2, padx=5)

    tk.Button(frame_btn, text="Thoát",bg = "#f61904", width=10, command=root.destroy).grid(row=0, column=4, padx=5)

    # ====== Tải dữ liệu ban đầu ======
    populate_combobox()
    load_data()
    root.grab_set()
    root.wait_window()
    if parent is not None:
        try:
            parent.deiconify()
        except Exception:
            pass
    return root
#==== Main Application Window ======
def main():
    root = tk.Tk()
    root.title("MENU QUẢN LÝ DU LỊCH")
    center_window(root, 800, 600)
    root.resizable(False, False)

    if not connect_db():
        messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến cơ sở dữ liệu MySQL.")
        root.destroy()
        return

    lbl_menu = tk.Label(root, text="MENU QUẢN LÝ DU LỊCH", font=("Arial", 20, "bold"),bg = "#b9ced3" , fg = "#320AE3")
    lbl_menu.pack(pady=30)

    frame_menu = tk.Frame(root)
    frame_menu.pack(pady=5)

    tk.Button(frame_menu, text="Quản lý các tuyến du lịch", width=30, height=2, command=lambda: qlcactuyendulich(root), bg = "#edf909" , ).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(frame_menu, text="Quản lý khách hàng", width=30, height=2, command=lambda: qlkhachhang(root),bg = "#f98603" ).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(frame_menu, text="Quản lý phương tiện", width=30, height=2, command=lambda: qlphuongtien(root),bg = "#69f903" ).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(frame_menu, text="Quản lý tuyến tham quan", width=30, height=2, command=lambda: tuyenthamquan(root),bg = "#f903dc").grid(row=3, column=0, padx=10, pady=10)
    tk.Button(frame_menu, text="Quản lý đặt tour", width=30, height=2, command=lambda: dattour(root),bg = "#03ccf9" ).grid(row=4, column=0, padx=10, pady=10) 
    tk.Button(frame_menu, text="Thoát", width=30, height=2, command=root.quit, bg= "#f50707" , fg = "#f8fc07").grid(row=5, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()


    


