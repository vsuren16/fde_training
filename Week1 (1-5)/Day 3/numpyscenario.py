import numpy as np  

marks = np.array([78,85,90,66,88])

print("Highest mark is: ",np.max(marks))
print("Lowest mark is: ",np.min(marks))
print("Average mark is: ",np.mean(marks))

updated_marks = marks+5
print("Updated marks after addition of grace mark: ",updated_marks)