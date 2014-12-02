import numpy as np
import pprint

# nonZeroIndicesCount = np.zeros(10000)
impersonateCount = np.zeros(6)
for k in xrange(10000):
	sum = np.zeros(90)
	for i in xrange(1,30):
		indexesSet = np.random.randint(90, size=5)
		random_array = np.zeros(90)
		for j in xrange(5):
			random_array[indexesSet[j]] = 1
		sum = np.add(sum, random_array)
	# nonZeroIndicesCount[k] = np.shape(np.nonzero(sum))[1]
	indexesSet = np.random.randint(90, size=5)
	random_array = np.zeros(90)
	for j in xrange(5):
		random_array[indexesSet[j]] = 1
	impersonateCount[np.shape(np.nonzero(np.multiply(random_array, sum)))[1]] += 1
# print np.mean(nonZeroIndicesCount >= 68)
print impersonateCount

print 73*72*71*70*69/(90*89*88*87*86)