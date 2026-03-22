dictionary = {"bob": 1 , "ahmed": 2}

test = dictionary.values()
for i in test:
    if i > 1:
        key = i
        
a = dictionary.items()

for i in a:
    if (i[1]) == key:
        value = i[0]

dictionary.pop(value)

print(dictionary)