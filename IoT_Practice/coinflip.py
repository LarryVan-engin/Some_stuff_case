MOD = 10**9 + 7

# Hàm tính tổ hợp C(n, r) theo cách cơ bản
def tohop(n, r):
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)  # tối ưu một chút
    res = 1
    for i in range(1, r + 1):
        res = res * (n - i + 1) // i
    return res % MOD

# Hàm main
def coinFlipPossibilities(s, h, t):
    k = len(s)
    h_s = s.count('H')
    t_s = s.count('T')

    # Kiểm tra hợp lệ
    if h_s > h or t_s > t or k > h + t:
        return 0

    # Số lượt tung còn lại
    rem = (h + t) - k
    h_rem = h - h_s
    t_rem = t - t_s

    # Nếu không khớp thì không có cách nào
    if rem != h_rem + t_rem:
        return 0

    # Kết quả là C(rem, h_rem)
    return tohop(rem, h_rem)

# --- Nhập / xuất dữ liệu ---
s = input().strip()
h = int(input().strip())
t = int(input().strip())

print(coinFlipPossibilities(s, h, t))
