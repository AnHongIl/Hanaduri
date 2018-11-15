from apps.models import Writings

f = open("../writings.txt", 'r')
cnt = 0
title = []
body = []
category = []
admin = []
legis = []
keywords = []
while True:
    line = f.readline().rstrip()
    if not line: break
    if cnt % 6 ==  0:
        title.append(line)
    elif cnt % 6 == 1:
        body.append(line)
    elif cnt % 6== 2:
        category.append(line)
    elif cnt % 6== 3:
        admin.append(line)
    elif cnt % 6 == 4:
        legis.append(line)
    elif cnt % 6 == 5:
        keywords.append(line)
    cnt += 1
f.close()

for i in range(3):
    wt = Writings(title=title[i], body=body[i], category=category[i], administration=admin[i], legislature=legis[i], keywords=keywords[i])
    print(wt)
    wt.save()
