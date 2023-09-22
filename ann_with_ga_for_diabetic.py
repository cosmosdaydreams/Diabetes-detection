# -*- coding: utf-8 -*-
"""ANN with GA for diabetic.ipynb
"""

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier


from sklearn import model_selection
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

from keras.wrappers.scikit_learn import KerasClassifier

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings('ignore')

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/KBB/diabetes_data_upload.csv')
df.head()

df.columns = ['Age','Gender','Polyuria','Polydipsia','sudden_weight_loss','weakness','Polyphagia','Genital_thrush','visual_blurring','Itching','Irritability','delayed_healing','partial_paresis','muscle_stiffness','Alopecia','Obesity','class']
df.head()

df.info()

df.isnull().sum()

df.isnull().values.any()

from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()
df['Gender_n'] = lb.fit_transform(df['Gender'])  # Male=1, Female=0
df.drop('Gender', axis='columns',inplace=True)
df['Polyuria_n'] = lb.fit_transform(df['Polyuria'])  # Yes=1, No=0
df.drop('Polyuria', axis='columns',inplace=True)
df['Polydipsia_n'] = lb.fit_transform(df['Polydipsia'])  # Yes=1, No=0
df.drop('Polydipsia', axis='columns',inplace=True)
df['sudden_weight_loss_n'] = lb.fit_transform(df['sudden_weight_loss'])  # Yes=1, No=0
df.drop('sudden_weight_loss', axis='columns',inplace=True)
df['weakness_n'] = lb.fit_transform(df['weakness'])  # Yes=1, No=0
df.drop('weakness', axis='columns',inplace=True)
df['Polyphagia_n'] = lb.fit_transform(df['Polyphagia'])  # Yes=1, No=0
df.drop('Polyphagia', axis='columns',inplace=True)
df['Genital_thrush_n'] = lb.fit_transform(df['Genital_thrush'])  # Yes=1, No=0
df.drop('Genital_thrush', axis='columns',inplace=True)
df['visual_blurring_n'] = lb.fit_transform(df['visual_blurring'])  # Yes=1, No=0
df.drop('visual_blurring', axis='columns',inplace=True)
df['Itching_n'] = lb.fit_transform(df['Itching'])  # Yes=1, No=0
df.drop('Itching', axis='columns',inplace=True)
df['Irritability_n'] = lb.fit_transform(df['Irritability'])  # Yes=1, No=0
df.drop('Irritability', axis='columns',inplace=True)
df['delayed_healing_n'] = lb.fit_transform(df['delayed_healing'])  # Yes=1, No=0
df.drop('delayed_healing', axis='columns',inplace=True)
df['partial_paresis_n'] = lb.fit_transform(df['partial_paresis'])  # Yes=1, No=0
df.drop('partial_paresis', axis='columns',inplace=True)
df['muscle_stiffness_n'] = lb.fit_transform(df['muscle_stiffness'])  # Yes=1, No=0
df.drop('muscle_stiffness', axis='columns',inplace=True)
df['Alopecia_n'] = lb.fit_transform(df['Alopecia'])  # Yes=1, No=0
df.drop('Alopecia', axis='columns',inplace=True)
df['Obesity_n'] = lb.fit_transform(df['Obesity'])  # Yes=1, No=0
df.drop('Obesity', axis='columns',inplace=True)
df['class_n'] = lb.fit_transform(df['class'])  # Positive=1, Negative=0
df.drop('class', axis='columns',inplace=True)
df.tail(10)

df.to_csv('diabetes_preposess.csv',index=False,header=True)

df.groupby(['class_n']).mean()

"""Membagi data testing dan training"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

y_train = df['class_n']
x_train = df.drop(labels =['class_n'],axis=1)

ohe = OneHotEncoder()
le = LabelEncoder()

cols = x_train.columns.values
for col in cols:
    x_train[col] = le.fit_transform(x_train[col])

y_train = le.fit_transform(y_train)

ohe = ColumnTransformer([("class", OneHotEncoder(), [1])], remainder = 'passthrough')
x_train = ohe.fit_transform(x_train)
sc = StandardScaler()
x_train = sc.fit_transform(x_train)


x_train, x_test, y_train, y_test = train_test_split(x_train,y_train, test_size = 0.20, random_state = 42)
x_valid, x_test, y_valid, y_test = train_test_split(x_test,y_test, test_size = 0.50, random_state = 42)

len(x_train),len(x_test),len(x_valid)

"""Membangun Model ANN dan GA"""

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

def forward(x, w, activation):
    return activation(np.matmul(x, w))

def accuracy_fn(y, y_hat):
    return (np.where(y == y_hat)[0].size / y_hat.size)

def predict(x, y_hat, weights, activation):
    predictions = np.zeros(shape=(x.shape[0]))

    for idx in range(x.shape[0]):
        r1 = x[idx, :]
        for curr_weights in weights:
            r1 = forward(r1, curr_weights, activation)
        predictions[idx] = np.where(r1 == np.max(r1))[0][0]

    accuracy = accuracy_fn(predictions, y_hat)
    return accuracy, predictions

def fitness(x, y_hat, weights, activation):
    accuracy = np.empty(shape=(weights.shape[0]))
    for idx in range(weights.shape[0]):
        accuracy[idx], _ = predict(x, y_hat, weights[idx, :], activation)
    return accuracy

def mat_to_vector(mat_pop_weights):
    weights_vector = []
    for idx in range(mat_pop_weights.shape[0]):
        curr_vector = []
        for layer_idx in range(mat_pop_weights.shape[1]):
            vector_weights = np.reshape(mat_pop_weights[idx, layer_idx], newshape=(mat_pop_weights[idx, layer_idx].size))
            curr_vector.extend(vector_weights)
        weights_vector.append(curr_vector)
    return np.array(weights_vector)


def vector_to_mat(vector_weights, mat_pop_weights):
    mat_weights = []
    for idx in range(mat_pop_weights.shape[0]):
        start = 0
        end = 0
        for layer_idx in range(mat_pop_weights.shape[1]):
            end = end + mat_pop_weights[idx, layer_idx].size
            curr_vector = vector_weights[idx, start:end]
            mat_layer_weights = np.reshape(curr_vector, newshape=(mat_pop_weights[idx, layer_idx].shape))
            mat_weights.append(mat_layer_weights)
            start = end
    return np.reshape(mat_weights, newshape=mat_pop_weights.shape)

import random
def mating_pool(pop, fitness, num_parents):
    parents = np.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99
    return parents


def crossover(parents, offspring_size):
    offspring = np.empty(offspring_size)
    crossover_point = np.uint32(offspring_size[1]/2)

    for k in range(offspring_size[0]):

        parent1_idx = k%parents.shape[0]
        parent2_idx = (k+1)%parents.shape[0]

        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]

    return offspring


def mutation(offspring_crossover, mutation_percent):
    num_mutations = np.uint32((mutation_percent*offspring_crossover.shape[1]))
    mutation_indices = np.array(random.sample(range(0, offspring_crossover.shape[1]), num_mutations))

    for idx in range(offspring_crossover.shape[0]):
        random_value = np.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, mutation_indices] = offspring_crossover[idx, mutation_indices] + random_value

    return offspring_crossover

"""Menetukan parameter training"""

solution_per_population = 20
num_parents_mating = 4
num_generations = 200
mutation_percent = 0.20

input_shape = x_train.shape[1]
output_shape = len(np.unique(y_train))

initial_weights = []
for curr_sol in np.arange(0, solution_per_population):

    w1 = np.random.uniform(low=-0.1, high=0.1, size=(input_shape, 128))
    w2 = np.random.uniform(low=-0.1, high=0.1, size=(128, 64))
    w3 = np.random.uniform(low=-0.1, high=0.1,size=(64, output_shape))

    initial_weights.append(np.array([w1, w2, w3]))

weights_mat = np.array(initial_weights)
weights_vector = mat_to_vector(weights_mat)

best_outputs = []
accuracies = np.empty(shape=(num_generations))

"""Training Model

"""

from tqdm import tqdm

for generation in tqdm(range(num_generations)):

    # vector to matrix
    weights_mat = vector_to_mat(weights_vector, weights_mat)

    # fitness of the population
    fit = fitness(x_train, y_train, weights_mat, activation=sigmoid)

    # assign first fitness to the array
    accuracies[generation] = fit[0]

    # selecting mating parents from pool
    parents = mating_pool(weights_vector, fit.copy(), num_parents_mating)

    # generate new population using crossover
    offspring_crossover = crossover(parents, offspring_size=(weights_vector.shape[0]-parents.shape[0], weights_vector.shape[1]))

    # adding mutation to the population
    offspring_mutation = mutation(offspring_crossover, mutation_percent=mutation_percent)

    # new population combining parents of crossver and mut
    weights_vector[0:parents.shape[0], :] = parents
    weights_vector[parents.shape[0]:, :] = offspring_mutation

"""Analisis Akurasi dan Nilai Fitness"""

weights_mat = vector_to_mat(weights_vector, weights_mat)
best_weights = weights_mat [0, :]
acc, predictions = predict(x_train, y_train, best_weights, sigmoid)
print("Akurasi dari solusi terbaik adalah: ", acc)

plt.plot(accuracies)
plt.xlabel("Iteration", fontsize=15)
plt.ylabel("Fitness", fontsize=15)
plt.xticks(np.arange(0, num_generations+1, 100))
plt.yticks(np.arange(0, 1, 0.1))
plt.show()

weights_mat = vector_to_mat(weights_vector, weights_mat)
best_weights = weights_mat [0, :]
acc, predictions = predict(x_test, y_test, best_weights, sigmoid)
print("Akurasi dari solusi terbaik adalah : ", acc)
