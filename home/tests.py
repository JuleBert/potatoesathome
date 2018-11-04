import re
test = 'http://localhost:8000/activate/OQ/50z-3d8fb0cc206cdaeec9da/'
re_activate = re.compile('activate/[0-9a-zA-Z]{2}/[0-9a-zA-Z\-]+')
#re_activate = re.compile('activate/[0-9a-fA-F]+/')
print(re_activate.search(test))