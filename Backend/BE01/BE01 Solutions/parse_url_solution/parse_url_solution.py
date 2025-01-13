url = input("Please enter a URL >> ")

parts = url.split('?')

host = parts [0].split("//")[1]
print("Host is " + host)

params = parts[1].split('&')
for param in params:
  values = param.split('=')
  print("Name is " + values[0] + ", value is " + values[1])
