import os.path


def estimate(t1, t2, m):
	return t1 + (t2 * m)


def load_theta():
	if os.path.isfile('theta'):
		with open('theta', 'r') as f:
			t1 = float(f.readline().split('=')[0])
			t2 = float(f.readline().split('=')[0])
	else:
		t1 = 0
		t2 = 0
	return t1, t2


if __name__ == '__main__':
	theta1, theta2 = load_theta()
	mileage = float(input('Enter mileage: '))
	estimate = estimate(theta1, theta2, mileage)
	print(f'Price estimate for {mileage} miles is {estimate}')
