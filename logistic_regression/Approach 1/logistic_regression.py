import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
import seaborn as sns


# Sigmoid Function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# Implementation of the stochastic gradient descent
def gradient_descent(X, y, params, learning_rate, iterations):
    m = len(y)
    cost_history = np.zeros((iterations, 1))

    for i in range(iterations):
        params = params - (learning_rate/m) * (X.T @ (sigmoid(X @ params) - y)) 
        cost_history[i] = compute_cost(X, y, params)

    return (cost_history, params)


# Computing the cost via the negative log loss
def compute_cost(X, y, theta):
    m = len(y)
    h = sigmoid(X @ theta)
    epsilon = 1e-5
    cost = (1/m)*(((-y).T @ np.log(h + epsilon))-((1-y).T @ np.log(1-h + epsilon)))
    return cost


def predict(X, params):
    return np.round(sigmoid(X @ params))


# Driver Code

# Used scikit-learn to make a random binary classification dataset
X, y = make_classification(n_samples=500, n_features=2, n_redundant=0, n_informative=1,
                             n_clusters_per_class=1, random_state=14)

y = y[:, np.newaxis]

sns.set_style('white')
sns.scatterplot(X[:, 0], X[:, 1], hue=y.reshape(-1))

m = len(y)

X = np.hstack((np.ones((m, 1)), X))
n = np.size(X, 1)
params = np.zeros((n, 1))

iterations = 1000  # Number of iterations
learning_rate = 0.01  # Learning rate of stochastic gradient descent

initial_cost = compute_cost(X, y, params)

print("Initial Cost is: {} \n".format(initial_cost))

(cost_history, params_optimal) = gradient_descent(X, y, params, learning_rate, iterations)

print("Optimal Parameters are: \n", params_optimal, "\n")

plt.figure()
sns.set_style('white')
plt.plot(range(len(cost_history)), cost_history, 'r')
plt.title("Convergence Graph of Cost Function")
plt.xlabel("Number of Iterations")
plt.ylabel("Cost")
plt.show()

y_pred = predict(X, params_optimal)
score = float(sum(y_pred == y)) / float(len(y))

print("Score is : ", score)

slope = -(params_optimal[1] / params_optimal[2])
intercept = -(params_optimal[0] / params_optimal[2])

sns.set_style('white')
sns.scatterplot(X[:, 1], X[:, 2], hue=y.reshape(-1))

ax = plt.gca()
ax.autoscale(False)
x_vals = np.array(ax.get_xlim())
y_vals = intercept + (slope * x_vals)
plt.title('Division Proposed by our Trained Model')
plt.plot(x_vals, y_vals, c="k")
plt.show()