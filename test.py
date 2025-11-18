def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ngocha1020",
            database="qlcactuyendulich",
            port=3306,
            # auth_plugin='mysql_native_password'  # bật nếu bị lỗi xác thực
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối MySQL:\n{err}")
        return None