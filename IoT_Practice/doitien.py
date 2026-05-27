import math

def doitien(n, k, arr):
   
    if k < 0 or k > 100:
        return 0
    if len(arr) != len(set(arr)):
        return 0
    if not arr:
        return 0
    if any(x < 1 or x > 10000 for x in arr):
        return 0
    
#dung thuat toan dynamic process
    dp = [math.inf] * (n + 1)
    dp[0] = 0  

    for i in range(1, n + 1):
        for coin in arr:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[n] if dp[n] != math.inf else 0


if __name__ == "__main__":
   
    n = int(input().strip())
    k = int(input().strip())
    arr = list(map(int, input().split()))

   
    if any(x < 1 or x > 10000 for x in arr):
        print(0)
    else:
        print(doitien(n, k, arr))
