
phrase = "oh kdfkdjh yrxv shuphwwudlw gdvvxuhu od frqilghqwldolwh vlpsohphqw"

print("%s"%phrase)

print(len(phrase))

decode=""
for i in range(len(phrase)):
    c= phrase[i]
    if c !=' ':
        d = ord(c)-3
        decode=decode+chr(d)
    else :
        decode=decode+" "

print(decode)   