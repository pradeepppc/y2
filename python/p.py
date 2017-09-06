from urllib import request

url = 'https://query1.finance.yahoo.com/v7/finance/download/GOOG?period1=1497843566&period2=1500435566&interval=1d&events=history&crumb=RrkQ5lQrV/u'

def fun(url):
    responce = request.urlopen(url)
    cs  = responce.read()
    css = str(cs)
    lines  = css.split('\\n')
    name = r'gog.csv'
    f = open(name,'w')
    for line in lines:
        f.write(line + '\n')

    f.close()
fun(url)