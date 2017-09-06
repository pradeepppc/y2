from collections import Counter
text = 'majkcnka a cjknac ajcna ckjdc acjdc d cjdc d cdjc dj cakjd cadcadc hello hello hello'
ans = text.split()
counter  = Counter(ans)
print(counter.most_common(4))