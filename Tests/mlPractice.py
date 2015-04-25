from sklearn import datasets
from sklearn import svm
import matplotlib.pyplot as plt

iris = datasets.load_iris()
digits = datasets.load_digits()

clf = svm.SVC(gamma=.001, C=100)
clf.fit(digits.data[:-1], digits.target[:-1])

# print clf.predict(digits.data[-1])

print digits.data[:2]