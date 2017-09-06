import random
import

def fun(url):
    name  = random.randrange(1,1000)
    fullname = str(name) + ".jpg"
    urllib.request.urlretrieve(url , fullname)

fun("https://www.google.co.in/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwiQ2eKJnpPVAhVBYo8KHY_GC2UQjRwIBw&url=https%3A%2F%2Fpixabay.com%2Fen%2Fphotos%2Fwinter%2F&psig=AFQjCNEBHpxLri2JkAojmz1JgkEEcVHRMw&ust=1500481168949705")