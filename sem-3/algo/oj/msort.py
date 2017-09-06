def mergesort(ar):
        if len(ar) != 1:
                m = int(len(ar)/2)
                leftar = ar[:m]
                rightar = ar[m:]
                mergesort(leftar)
                mergesort(rightar)

                l1 = len(leftar)
                l2 = len(rightar)
                i = 0
                j = 0
                k = 0
                while (j < l1) and (k < l2) and (i < l1+l2):
                        if leftar[j] < rightar[k]:
                                ar[i] = leftar[j]
                                j += 1
                                i += 1
                        else:
                                ar[i] = rightar[k]
                                k += 1
                                i += 1
                while(j < l1):
                        ar[i] = leftar[j]
                        j += 1
                        i += 1
                while(k < l2):
                        ar[i] = rightar[k]
                        k += 1
                        i += 1





def main():
        ar=input()
        ar=ar.split()
        n = len(ar)
        for i in range(0,n):
                ar[i] = int(ar[i])
        mergesort(ar)
        for i in range(n):
                print(ar[i], " ", end='')

main()


