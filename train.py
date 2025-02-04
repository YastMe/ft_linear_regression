from estimate import estimate

def read_data(file: str) -> list:
	try:
		f = open(file, "r", encoding="utf-8")
		data = f.readlines()
		f.close()
		try:
			int(data[0].split(",")[0])
			int(data[0].split(",")[1])
		except ValueError:
			del data[0]
		if data[-1] == "\n":
			del data[-1]
		data = [line.split(",") for line in data]
		data = [[float(element) for element in line] for line in data]
		return data
	except FileNotFoundError:
		print("File not found")
		exit(1)
	except ValueError:
		print("Wrong data format")
		exit(1)


class LinearRegression:
	def __init__(self, file="data.csv"):
		"""
			Sets up a linear regression model's starting values
		"""
		# Hyperparameters
		self.learning_rate = 0.01
		self.theta0 = 0
		self.theta1 = 0

		# Init data
		self.data_raw = read_data(file)
		self.km_raw = [line[0] for line in self.data_raw]
		self.prices = [line[1] for line in self.data_raw]
		self.m = len(self.data_raw)

		# Metadata
		self.mean_km = sum(self.km_raw) / self.m
		self.standard_devi_km = (sum([(kms - self.mean_km) ** 2 for kms in self.km_raw]) / self.m) ** 0.5

		# Normalize data
		self.kms = [
			(km - self.mean_km) / self.standard_devi_km for km in self.km_raw
		]

		# Logs
		self.loss_accuracy = []


	def calculate_errors(self):
		"""
			Calculates the loss and accuracy of the model for the current theta values

			:return:
			float: t0_error
			float: t1_error
			float: total_loss
		"""
		t0_error = 0
		t1_error = 0
		total_loss = 0

		for i in range(self.m - 1):
			predict = estimate(
				self.theta0,
				self.theta1,
				self.km_raw[i]
			)
			error = (predict[0] - self.prices[i])
			t0_error += error
			t1_error += error * self.kms[i]
			total_loss += abs(error)

		total_loss /= self.m
		return t0_error, t1_error, total_loss

	def train(self):
		max_iter = 1000

		for iteration in range(max_iter):
			t0_error, t1_error, total_loss = self.calculate_errors()
			self.theta0 += self.learning_rate * t0_error
			self.theta1 += self.learning_rate * t1_error
			self.loss_accuracy.append(total_loss)

			if len(self.loss_accuracy) > 1 and round(self.loss_accuracy[-1], 6) == round(self.loss_accuracy[-2], 6):
				break

			self.theta0 -= self.theta1 * self.mean_km / self.standard_devi_km
			self.theta1 /= self.standard_devi_km

			# Plot states


	def save(self, file: str = "thetas"):
		with open(file, "w", encoding="utf-8") as f:
			f.write(f"{str(self.theta0)},{str(self.theta1)}")


if __name__ == "__main__":
	regressor = LinearRegression()
	regressor.train()
	regressor.save()