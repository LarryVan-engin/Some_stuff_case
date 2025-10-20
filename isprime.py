import math

def prime():

    a = int(input())
    b = int(input())
    if a<b:
        return None #Khong hop le
    elif a>=1:
            bieu_thuc = a**2 - b**2
            #metric kiem tra so nguyen to
            if bieu_thuc < 2:
                return False, bieu_thuc
            for i in range(2, int(math.sqrt(bieu_thuc)) + 1):
                if bieu_thuc%i == 0:
                    return False, bieu_thuc
            return True, bieu_thuc   


if __name__=="__main__":
    while True:
        #nhap code show ket qua tai day
        #goi ham con
        result = prime()
        if result is None:
            print(0)
        else:
            is_prime, value = result
            if is_prime:
                #print(f"{value} la so nguyen to")
                print(1)
            else: 
                #print(f"{value} khong la nguyen to ")
                print(0)
        break


