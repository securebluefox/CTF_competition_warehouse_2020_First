from flag import flag
def pairing(a,b):
    shell = max(a, b)
    step = min(a, b)
    if step == b:
        flag = 0
    else:
        flag = 1
    return shell ** 2 + step * 2 + flag

def encrypt(message):
    res = ''
    for i in range(0,len(message),2):
        res += str(pairing(message[i],message[i+1]))
    return res

print(encrypt(flag))
# 1186910804152291019933541010532411051999082499105051010395199519323297119520312715722