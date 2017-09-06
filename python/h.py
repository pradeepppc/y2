import random
import urllib.request

def fun(url):
    name = random.randrange(1,500)
    fullname = str(name) + '.jpg'
    urllib.request.urlretrieve(url,fullname)
fun('https://www.google.co.in/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwi1qM-EpZPVAhWHOo8KHf4rDGYQjRwIBw&url=https%3A%2F%2Fwww.w3schools.com%2Fcss%2Fcss3_images.asp&psig=AFQjCNGSNeyBkFTo3kAEmVY5lELAJDeB5w&ust=1500483003874427')