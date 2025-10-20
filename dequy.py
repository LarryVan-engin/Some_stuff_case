import math
import os

def matrix(board, word):
    rows = len(board)
    cols = len(board[0])

    def search(i, j, k):
        
        # Nếu đã tìm hết ký tự trong word
        if k == len(word):
            return True
        
        # Nếu vượt biên hoặc ký tự không khớp
        if i < 0 or i >= rows or j < 0 or j >= cols or board[i][j] != word[k]:
            return False

        # Đánh dấu ô đã dùng
        temp = board[i][j]
        board[i][j] = " "

        # Tìm theo 4 hướng
        found = (
            search(i+1, j, k+1) or
            search(i-1, j, k+1) or
            search(i, j+1, k+1) or
            search(i, j-1, k+1)
        )

        # Khôi phục ô
        board[i][j] = temp
        return found

    # Thử bắt đầu từ mọi ô
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == word[0]:
                if search(i, j, 0):
                    return True
    return False


# --- Nhập dữ liệu ---
word = input().strip()
n = int(input().strip())
board = [input().split() for _ in range(n)]

# --- Xuất kết quả ---
print(matrix(board, word))
