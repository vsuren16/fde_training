# def count():
#     for i in range(1,6):
#         yield i 

# for num in count():
#     print(num)

def my_gen():
    yield 1
    yield 2 
    yield 3 

for value in my_gen():
    print(value)