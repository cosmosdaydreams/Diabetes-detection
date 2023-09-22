# Diabetes-detection

This code attempts to optimize the weights of an ANN model using GA with the goal of improving classification accuracy on the diabetes dataset. This process enables automated modeling that selects the best weights to enhance model performance.

Here's an explanation of the main steps present in the code:


**1. Import Libraries:**
   The code starts by importing various libraries that will be used in the process, including numpy, pandas, tensorflow, sklearn, keras, matplotlib, seaborn, and others.

**2. Read Data:**
   The diabetes dataset is read from the 'diabetes_data_upload.csv' file located on Google Drive.

**3. Data Preprocessing:**
   The dataset then undergoes several preprocessing steps, including renaming columns, encoding categorical variables into numeric ones, and dropping unused columns. The result is saved in the 'diabetes_preposess.csv' file.

**4. Data Splitting:**
   The data is split into three parts: training, validation, and testing using train_test_split. The split is done twice to obtain three different sets of data.

**5. Activation Function Definition:**
   Two activation functions are defined, namely sigmoid and ReLU.

**6. Definition of GA Functions:**
   Several GA functions are defined, including the fitness function, matrix to vector conversion, vector to matrix conversion, mating pool formation, crossover, and mutation.

**7. GA Parameters:**
   Some parameters for the GA are specified, such as the number of solutions in the population, the number of parents to mate, the number of generations, and the mutation percentage.

**8. Population Initialization:**
   The initial population is initialized with random weights that influence the ANN model.

**9. Model Training:**
    The model training process is performed using GA. Each generation, different models are tested by calculating their accuracy on the training data.

**10. Analysis of Results:**
    The best accuracy result from the models produced by GA is evaluated on both the training data and the testing data.
