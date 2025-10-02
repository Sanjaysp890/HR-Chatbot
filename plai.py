str1  ="adasdasd"
unique_str = list(set(str1))
count = {}
for  i in unique_str:
    count[i] = str1.count(i)
odd_count  = False
for i in count:
    if count[i]%2 != 0:
        odd_count = True

for i in count:
    count[i] = count[i]//2*2


sum = 0
for i in count:
    sum = sum+count[i]
sum = sum+ odd_count
print(sum)