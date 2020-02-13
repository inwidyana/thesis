#%%
# Commented out IPython magic to ensure Python compatibility.
from __future__ import absolute_import, division, print_function, unicode_literals

import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from math import sqrt

from keras import regularizers

print(tf.__version__)

#%%
root_path = './processed data/'
dataset_path = root_path + 'data.csv'

raw_dataset = pd.read_csv(dataset_path, sep=",")
dataset = raw_dataset.copy()
dataset.head()

#%%
dataset.corr(method='pearson')

#%%
topop = [
  'tmp_3', 'tmp_4', 'tmp_5', 'tmp_6', 'tmp_7', 'tmp_8', 'tmp_9', 'tmp_10', 'tmp_11', 'tmp_12',
  'pre_3', 'pre_4', 'pre_5', 'pre_6', 'pre_7', 'pre_8', 'pre_9', 'pre_10', 'pre_11', 'pre_12'
]

for col in topop:
  dataset.pop(col)

dataset.tail()

#%%
train_dataset = dataset.sample(frac=0.75,random_state=0)
test_dataset = dataset.drop(train_dataset.index)

train_dataset.tail()

#%%
dataset.describe(include='all')

#%%
train_stats = train_dataset.describe(include='all')
train_stats.pop('yield')
train_stats = train_stats.transpose()
train_stats

#%%
train_labels = train_dataset.pop('yield')
test_labels = test_dataset.pop('yield')

#%%
def norm(x):
  return (x - train_stats['mean']) / train_stats['std']

previous_year = test_dataset.copy()
previous_year = previous_year.pop('yield_t-1')

#%%
# normed_train_data = norm(train_dataset)
# normed_test_data = norm(test_dataset)

normed_train_data = train_dataset
normed_test_data = test_dataset

normed_train_data.tail()

#%%
def build_model():
  leaky_relu = lambda x: keras.activations.relu(x, alpha=0.1)
  
  model = keras.Sequential([
    layers.Dense(6, activation=leaky_relu, input_shape=[len(train_dataset.keys())]),
#     layers.Dense(2, activation=leaky_relu, input_shape=[len(train_dataset.keys())]),
#     layers.Dense(4, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(1)
  ])
  
  optimizer = tf.keras.optimizers.Adam(lr=0.01)
#   optimizer = tf.keras.optimizers.SGD(lr=0.01, momentum=0.00001, nesterov=True)
#   optimizer = tf.keras.optimizers.SGD(lr=0.01, momentum=0.01)

#%%
  model.compile(loss='mean_absolute_error',
                optimizer=optimizer,
                metrics=['mean_squared_error'])
  return model

model = build_model()

model.summary()

#%%
example_batch = train_dataset[:10]
example_result = model.predict(example_batch)
example_result

#%%
EPOCHS = 100
# early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

history = model.fit(
  normed_train_data, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
#   callbacks=[early_stop]
)

#%%
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()

#%%
def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch

  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error [$qu/ha^2$]')
  plt.plot(hist['epoch'], hist['mean_squared_error'], label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_squared_error'], label = 'Val Error')
#   plt.ylim([0,1000000000])
  plt.legend()
  plt.show()


plot_history(history)

#%%
test_predictions = model.predict(normed_test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [qu/ha]')
plt.ylabel('Predictions [qu/ha]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])

loss, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
persistence_errors = (previous_year - test_labels)

error = test_predictions - test_labels
plt.hist(error)
plt.xlabel("Prediction Error [qu/ha]")
_ = plt.ylabel("Count")

plt.hist(persistence_errors)
plt.xlabel("Persistence Error [qu/ha]")
_ = plt.ylabel("Count")

persistence_error = pow(persistence_errors.sum(axis=0), 2)
persistence_error = persistence_error / len(persistence_errors)

print("Testing set Mean Abs Error: {:5.2f} qu/ha".format(loss))
print("Testing set Root Mean Squared Error: {:5.2f} qu/ha".format(sqrt(mse)))
print("Persistence set Root Mean Squared Error: {:5.2f} qu/ha".format(sqrt(persistence_error)))

