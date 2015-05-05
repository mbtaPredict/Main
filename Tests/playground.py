import matplotlib.pyplot as plt

X = range(10)
Y1 = range(10)
Y2 = range(5,10) + range(5)

first, = plt.plot(X, Y1, label='First')
second, = plt.plot(X, Y2, label='Second')
plt.title('This is a Title', fontsize=30)
plt.xlabel('X Axis', fontsize=20)
# plt.xlabel.set_fontsize(20)
plt.legend(fontsize=20)
plt.show()