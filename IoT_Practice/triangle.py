import math

def triangle(arr):
    if not isinstance(arr, list):
        raise ValueError
    if len(arr) != 3:
        raise ValueError
    if any(x <= 0 for x in arr):
        raise ValueError
    a, b, c = arr[0], arr[1], arr[2]
    # Kiểm tra điều kiện bất đẳng thức tam giác
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError
    if a == b and b == c:
        print("Equilateral triangle")
    elif a==b or a==c or b==c:
        print("Isosceles triangle")
    else:
        print("Scalene triangle")

if __name__ == "__main__":
    try:
        arr = list(map(int, input().split()))
        triangle(arr)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)
