def inssort(ar,n):
        for l in range(1, n):
                key = ar[l]
                j = l - 1
                while (j >= 0) and (ar[j] > key):
                        ar[j + 1] = ar[j]
                        j -= 1
                ar[j + 1] = key
        return ar
def main():
        ar=input()
        ar=ar.split()
        n = len(ar)
        for i in range(0,n):
                ar[i] = int(ar[i])
        ar = inssort(ar,n)
        for i in range(n):
                print(ar[i], " ", end='')

main()


