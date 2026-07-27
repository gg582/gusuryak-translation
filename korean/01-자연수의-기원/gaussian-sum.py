x = [1, 10]

for i in range(len(x)):
    x[i] *= 10

s = sum(x)
s /= 2

assert s == 55
print("1+2+3+4+5+6+7+8+9+10 == ((1+10)*10)/2")

