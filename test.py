import matplotlib.pyplot as plt

x = range(5, 35, 5)
y1 = [1.09099629071, 1.0872970665, 1.08608732811, 1.08543888468, 1.08524403509, 1.08499849802]
y2 = [1.02334574482, 1.00098761019, 0.993408089232, 0.9906119682, 0.990007914983, 0.989678687427]
plt.figure(figsize=(16, 9))
plt.plot(x, y1, label='Cosine', linewidth=3, color='r', marker='o', markerfacecolor='red', markersize=15)
plt.plot(x, y2, label='Adjusted', linewidth=3, color='g', marker='s', markerfacecolor='green', markersize=15)
plt.xlabel('K(Number of Neighbors)', fontsize=25)
plt.ylabel('MSE', fontsize=25)
plt.legend()
# plt.show()
plt.savefig("result.jpg")
