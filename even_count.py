# def even_digit_number(arr):
#     """
#     Hàm tìm các số chẵn trong mảng
#     :param arr: danh sách các số nguyên
#     """
#     if not isinstance(arr, list):
#         raise ValueError
#     if len(arr) > 10**5:
#         raise ValueError
#     if any(x < 0 or x > 10**6 for x in arr):
#         raise ValueError

#     # Đếm số chẵn bằng list comprehension
#     even_count = sum(1 for x in arr if x % 2 == 0)
#     return even_count

# if __name__ == "__main__":
#     try:
#         arr = list(map(int, input().split()))

#         result = even_digit_number(arr)
#         print(result)
#     except ValueError:
#         print(0)
#     except Exception:
#         print(0)


###Gộp các khoảng chồng lấn [start, end]

# def merged_interval():
#     interval = []
#     while True:
#         line = input()
#         if not line.strip():
#             break
        
#         start, end = map(int, line.split())
#         interval.append([start, end])
    
#     interval.sort(key=lambda x: x[0])

#     if not interval:
#         return
    
#     merged = [interval[0]]

#     for current_start, current_end  in interval[1:]:
#         last_merged_end = merged[-1][1]

#         if current_start <= last_merged_end:
#             merged[-1][1] = max(last_merged_end, current_end)

#         else:
#             merged.append([current_start, current_end])
#     for start, end in merged:
#         print(f"{start} {end}")

# #Run function
# merged_interval()

###Ma trận xoắn ốc
import math
import os

def spiral_matrix(n):

    mat = [[0]*n for _ in range(n)] #Cho matrix la cac so 0 het
    num = 1
    top, bottom = 0, n-1
    left, right = 0, n-1

    while left <= right and top <= bottom:
        #Di tu trai qua phai tren hang top
        for j in range(left, right+1):
            mat[top][j] = num
            num +=1
        top +=1
    
        #Di tu tren xuong o cot right
        for i in range(top, bottom+1):
            mat[i][right]= num
            num += 1
        right -=1

        #Neu con hang bottom, di tu phai sang trai
        if top <= bottom:
            for j in range(right, left-1, -1):
                mat[bottom][j]= num
                num +=1
            bottom -=1

        #Neu con cot left, di tu duoi len
        if left <= right:
            for i in range(bottom, top-1, -1):
                mat[i][left]=num
                num +=1
            left +=1
    return mat
    
#call functions
if __name__=="__main__":
    n = int(input().strip())
    result = spiral_matrix(n)

    for row in result:
        print(" ".join(map(str,row)))

    

