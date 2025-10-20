# def sumofsame(a, b):
#     # Lấy các chữ số duy nhất trong mỗi chuỗi
#     set_a = set(a)
#     set_b = set(b)

#     # Tìm các chữ số chung
#     common = set_a & set_b

#     # Tính tổng các chữ số chung (chuyển từ ký tự sang số)
#     total = sum(int(x) for x in common)
#     return total

# a = input().strip()
# b = input().strip()


# print(sumofsame(a, b))

###Tong lon nhat cua day con lien tiep
#Su dung thuat toan Kadane
def kadane(arr):
    max_sum = float('-inf') #Tong lon nhat
    current_sum = 0

    for x in arr:
        current_sum +=x
        if current_sum > max_sum:
            max_sum = current_sum
        if current_sum <0:
            current_sum = 0
    return max_sum

if __name__=="__main__":
    arr= list(map(int,input().split()))
    print(kadane(arr))
