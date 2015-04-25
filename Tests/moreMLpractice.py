from sklearn import datasets
from sklearn import svm

data = []
target = []

for x in xrange(1000):
	data.append([float(x), x/2.0, x/3.0, x/4.0, x/5.0, x/6.0, x/7.0, x/8.0, x/9.0, x/10.0])
	target.append(float(x))

target[-6] = 1

clf = svm.SVC(gamma=.001, C=100)

stop = -5

clf.fit(data[:stop], target[:stop])

# print data[1]
# print target

print clf.predict(data[stop:])
print target[stop:]