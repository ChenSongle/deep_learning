import numpy as np

########## Select class/Sample data
### For every class, sample 2 training data
import string
classes = string.ascii_lowercase[:27]      # str 'abc...z'
X_train = np.array(['c', 'b', 'b', 'a', 'c', 'b'])
y_train = np.array([2, 1, 1, 0, 2, 1])
num_samples = 2

for y, cls in enumerate(classes):
    index = np.flatnonzero(y_train == y)   # Return indexes with non-zero values
    if (len(index)>1):
        index = np.random.choice(index, num_samples, replace=False)
        print(classes[y], X_train[index])

X_valid = X_train[2:]                # ndarray(['b' 'a' 'c' 'b'])
X_train = X_train[range(2)]          # ndarray(['c' 'b'])

### Create training/valdiation data
num_gp = 3
X_train = np.array([1, 2, 3, 4, 5, 6])
X_train_folds = np.array(np.array_split(X_train, num_gp)) # Split to 3 groups

size = len(X_train) // num_gp
for v in range(num_gp):
    indexes = list(range(num_gp))
    del indexes[v]
    X_training_data = np.concatenate(X_train_folds[indexes])
    X_valid_data = X_train[v*size:v*size+size]

########## Reshape data
### Flatten image data
X_train = np.array([ [[128, 128, 128], [128, 128, 128]], [[64, 128, 64], [120, 128, 120]] ])
X_train = np.reshape(X_train, (X_train.shape[0], -1))

########## Data preparation
### Subtract mean image
X_train = np.array([ [ [[128, 129], [135, 35]],
                        [[128, 129], [135, 35]] ],
                     [ [[126, 129], [135, 35]],
                        [[128, 129], [135, 37]] ]
                   ], dtype=np.float32)
mean_image = np.mean(X_train, axis=0)
X_train  -= mean_image

### Stack an extra 1
X_train = X_train.reshape((X_train.shape[0], -1))
X_train = np.hstack([X_train, np.ones((X_train.shape[0], 1))])

########## Data calculation
### L2 Norm
from numpy import linalg as LA
a = np.arange(9).reshape((3, 3))
a = a - np.mean(a)

v = LA.norm(a)        # 7.74596669241

### max(0, loss)
loss = np.array( [ [0.2, 0.5],
                     [0.6, -0.4],
                     [-0.2, 0.6]] )
loss = np.maximum(0, loss)

### Avoid divided by zero
x = np.array([2, 3, -1, -3])
y = np.array([2, -3, 1, 4])
x / (np.maximum(1e-8, np.add(x, y)))

########## Training

### Intialize weight for CNN (5x5 filter with 3 input feature map and 7 feature map output)
feature_in = 5 * 5 * 3
params = {}
params['W%d' % 3] = np.sqrt(2.0 / feature_in) * np.random.randn(3, 7, 5, 5)
for k, v in params.iteritems():
    params[k] = v.astype(np.float32)

### Intialize weight for FC (1024 input feature 256 output)
feature_in = 1024
np.sqrt(2.0 / feature_in) * np.random.randn(feature_in, 256)

### Affine
N, D, M = 100, 100, 4
x = np.random.randn(N, 10, 10)
w = np.random.randn(100, 4)
b = np.random.randn(4)
out = x.reshape(x.shape[0], -1).dot(w) + b

### Affine backward

dout = np.random.randn(N, M)
dx = dout.dot(w.T).reshape(x.shape)
dw = x.reshape(x.shape[0], -1).T.dot(dout)
db = np.sum(dout, axis=0)

### CNN Forward


### Temporal output
T, N, D, V, H = 10, 100, 10, 1000, 100

state = {}
x = np.random.randn(N, T, D)
wh = np.random.randn(D, H)
bh = np.zeros(H)
h = np.zeros((N, T, H))

for t in range(T):
  xt = x[:, t, :]
  state[t] = xt.dot(wh) + bh
  h[:, t, :] = state[t]

wo = np.random.randn(H, V)
bo = np.random.randn(V)

out = h.reshape(N * T, H).dot(wo).reshape(N, T, V) + bo

########## Classifier
def softmax_loss(X, y):
  pros = np.exp(X - np.max(X, axis=1, keepdims=True))
  pros /= np.sum(pros, axis=1, keepdims=True)
  N = X.shape[0]
  loss = -np.sum(np.log(pros[np.arange(N), y])) / N
  dX = pros.copy()
  dX[np.arange(N), y] -= 1
  dX /= N
  return loss, dX

X = np.random.randn(10, 5)
y = np.random.randint(5, size=10)

softmax_loss(X, y)

########## Result calculation
### Count accurate prediction
a = np.array([1, 1, 3, 3, 1])
p = np.array([1, 1, 4, 3, 1])
v = np.sum(a==3)
v = np.sum(a==p)
accuracy = float(v)/len(a)

a = np.array([1, 2, 3, 4, 5])
print(a[range(3)])

### Select predicted score
scores = np.array( [ [0.3, 0.7],
                     [0.6, 0.4],
                     [0.4, 0.6]] )
labels = np.array([1, 0, 0])
prediction_score  = scores[range(scores.shape[0]), labels]
prediction_labels = scores.argmax(axis=1)
matches = np.sum(prediction_labels == labels)
accuracy = np.mean(prediction_labels == labels)

