import heapq
stocks = [
    {'helo':'hel','value':451},
    {'hahcn':'cdav','value':15212},
    {'csa':'cac','value':12}

]
print(heapq.nsmallest(1,stocks,key=lambda x: x['value']))