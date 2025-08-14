import cmath

def tinh_toan_so_phuc(bieu_thuc):
    """Hàm tính toán các thông số của số phức

    Args:
        bieu_thuc (str): Biểu thức số phức dạng chuỗi

    Returns:
        tuple: Một tuple chứa phần thực, phần ảo, biên độ, góc pha (radian) và góc pha (độ)
    """

    try:
        # Đổi biểu thức thành số phức
        so_phuc = complex(bieu_thuc)

        # Tính toán các thông số
        phan_thuc = so_phuc.real
        phan_ao = so_phuc.imag
        bien_do = abs(so_phuc)
        goc_pha_rad = cmath.phase(so_phuc)
        goc_pha_do = goc_pha_rad * 180 / cmath.pi

        return phan_thuc, phan_ao, bien_do, goc_pha_rad, goc_pha_do

    except ValueError:
        print("Biểu thức nhập vào không hợp lệ. Vui lòng nhập lại!")
        return None

if __name__ == "__main__":
    while True:
        bieu_thuc = input("Nhập biểu thức số phức (hoặc 'quit' để thoát): ")
        if bieu_thuc.lower() == 'quit':
            break

        ket_qua = tinh_toan_so_phuc(bieu_thuc)
        if ket_qua:
            phan_thuc, phan_ao, bien_do, goc_pha_rad, goc_pha_do = ket_qua
            print("Phần thực:", phan_thuc)
            print("Phần ảo:", phan_ao)
            print("Biên độ:", bien_do)
            print("Góc pha (radian):", goc_pha_rad)
            print("Góc pha (độ):", goc_pha_do)
