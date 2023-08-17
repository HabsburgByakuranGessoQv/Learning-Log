a = [0] * 105
sumNmb = [[0] * 105] * 105
dp = [[0] * 105] * 105
if __name__ == "__main__":
    n = int(input())
    print('123')
    for i in range(n):
        a[i] = int(input())
        dp[i][i] = a[i]
        sumNmb[i][i] = a[i]
    for i in range(n):
        for j in range(i + 1, n):
            sumNmb[i][j] = sumNmb[i][j - 1] + a[j]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            print(i, j)
            dp[i][j] = sumNmb[i][j] - min(dp[i + 1][j], dp[i][j - 1])
    print(dp)
    print(str(dp[0][n - 1]) + " " + str(sumNmb[0][n - 1] - dp[0][n - 1]))
