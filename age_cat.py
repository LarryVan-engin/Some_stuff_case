import math

def age_cat():
    #xac dinh tuoi cua meo tren input nhap tu ban phim
    n = int(input())
    if n < 5: 
        print("Your cat is young")
    else:
        print("Your cat is old")

if __name__== "__main__":
    try:
       age_cat()
       
    except Exception:
        age_cat()