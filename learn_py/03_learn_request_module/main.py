import os
# import sys
import requests

print ("Welcome to IsItDown.py!")
print ("Please write a URL or URLs you want to check. (separated by comma)")

arr_urls=[]

def input_url():
  your_urls = input("Enter your URL: ")
  your_urls = your_urls.split(",")

  for url in your_urls:
    url = url.strip().lower()  
    arr_urls.append(url)

  return arr_urls


def chk_urls():
  inp_urls = input_url()

  for url in inp_urls:
    if "." in url:
      try:
        if (url[0:4] != "http"):
          url = f"http://{url}"
        res = requests.get(url).status_code
        
        if (res == 404):
          print(f"{url} is Not Found")
        elif (res == 200):
          print(f"{url} is up")
      except:
        print(f"{url} is down")
        
    else:
      print(f"{url} is not a valid url")
      break

    
def input_program_over():
  the_answer = input("Do you want to start over? y/n ")

  return the_answer
  
def chk_program_over():
  the_answer = input_program_over()
  
  if the_answer == "y":
    # os.execl(sys.executable, sys.executable, *sys.argv)
    os.system('clear')
  elif the_answer == "n":
    print("k.bye")
  else:
    print("This is not valid answer")
    chk_program_over()


chk_urls()
chk_program_over()
