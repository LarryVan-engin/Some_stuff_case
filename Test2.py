import cmath
import re  # Thư viện xử lý chuỗi với regex

def tinh_toan_so_phuc(bieu_thuc):
    """Hàm tính toán các thông số của số phức, hỗ trợ nhập e^(jθ) và cos(θ) + j*sin(θ)"""

    try:
        # Xử lý trường hợp nhập e^(jθ) hoặc exp(jθ)
        match_exp = re.match(r"(?:e\^|exp)\(?(j?[-+]?\d*\.?\d*)\)?", bieu_thuc, re.IGNORECASE)
        if match_exp:
            theta_str = match_exp.group(1)  # Lấy góc theta
            theta = float(theta_str[1:]) if theta_str and theta_str[0] == 'j' else float(theta_str or 1)
            so_phuc = cmath.exp(1j * theta)  # e^(jθ) = cos(θ) + j*sin(θ)

        # Xử lý dạng cos(θ) + j*sin(θ)
        elif re.match(r"cos\(.+\)\s*\+\s*j\s*\*\s*sin\(.+\)", bieu_thuc):
            match_cos_sin = re.findall(r"[-+]?\d*\.?\d+", bieu_thuc)
            if len(match_cos_sin) == 2:
                theta1, theta2 = map(float, match_cos_sin)
                if theta1 == theta2:  # Đảm bảo góc cos và sin khớp
                    so_phuc = cmath.cos(theta1) + 1j * cmath.sin(theta1)
                else:
                    raise ValueError("Góc của cos() và sin() không khớp!")

        # Nếu không phải 2 dạng trên, thử chuyển thẳng thành số phức
        else:
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
        bieu_thuc = input("Nhập số phức (VD: a+bj, e^(jθ), cos(θ) + j*sin(θ), hoặc 'quit' để thoát): ")
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