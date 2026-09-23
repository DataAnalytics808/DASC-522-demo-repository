# DASC-522: Machine Learning Demonstrations

Welcome to the demonstration repository for **DASC-522 Machine Learning**. This collection provides self-contained, reproducible Jupyter notebooks designed for interactive learning in Google Colab.

---

## How It Works

Each demonstration in this repository is designed to run seamlessly in the cloud without requiring local Python installation, manual file downloads, or Google Drive mounting:

1. **Launch in Colab**: Click the provided Colab link for any demonstration in [`COLAB_LINKS.md`](COLAB_LINKS.md).
2. **Copy to Drive**: Select **Copy to Drive** at the top of the notebook to save an editable copy to your own Google account.
3. **Run All**: Execute the cells in sequence. Datasets are fetched programmatically from the repository or standard library loaders.

```
Demonstration Link ──> Google Colab ──> Automatic Data Retrieval ──> Interactive Execution
```

---

## Key Principles

- **Zero Setup Overhead**: All code executes in standard Google Colab environments. No local environment configuration, API keys, or manual uploads are required.
- **Self-Contained Execution**: Every notebook automatically downloads its required datasets via secure HTTPS URLs or imports standard benchmark datasets directly through Scikit-Learn and Keras.
- **Current Library Compatibility**: Code is maintained and verified against current versions of Python, TensorFlow / Keras, and Scikit-Learn on standard Colab runtimes.

---

## Repository Structure

```
├── demos/             # 36 self-contained Colab demonstration and course notebooks
│   ├── Week_02_1_Regression_Review.ipynb
│   ├── Week_02_2_Classification.ipynb
│   ├── 4 Week 4A feature_selection_expanded with BIC and RFE v3.ipynb
│   ├── Homework_2_template_v7.ipynb
│   ├── Homework_3_template_v5.ipynb
│   ├── load_database_tutorial_v2.ipynb
│   └── ...
├── data/              # Course datasets loaded programmatically by the notebooks
│   ├── GRE.csv
│   ├── Hitters.csv
│   ├── lightning_data.db
│   ├── weather_data.db
│   └── ...
├── COLAB_LINKS.md     # Complete catalog of direct Colab launch links and CPU runtimes
└── README.md          # Repository overview and guide (this file)
```

---

## Dataset Storage & Access

- **Course Datasets (`data/`)**: Small tabular datasets, SQLite databases, and reference files are hosted directly in the `data/` directory and fetched programmatically via raw GitHub URLs:
  `https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/<filename>`
- **Standard Benchmark Datasets**: Standard benchmarks (such as Fashion-MNIST and Wine) are loaded directly via Keras and Scikit-Learn dataset utilities (`keras.datasets.fashion_mnist.load_data()`, `sklearn.datasets.load_wine()`), avoiding external storage dependencies.

---

## Course Demonstrations & Notebooks

Total Notebooks: **36** (See [`COLAB_LINKS.md`](COLAB_LINKS.md) for direct one-click Colab launch links and measured CPU runtimes).

| Week / Item | Title | Topic | Notebook Path |
| :--- | :--- | :--- | :--- |
| **Week 02.1** | Regression Review | OLS regression, metrics, and diagnostics | [`demos/Week_02_1_Regression_Review.ipynb`](demos/Week_02_1_Regression_Review.ipynb) |
| **Week 02.2** | Classification | Logistic Regression, LDA, and QDA | [`demos/Week_02_2_Classification.ipynb`](demos/Week_02_2_Classification.ipynb) |
| **Week 02.3** | Tree-Based Methods | Decision trees for regression and classification | [`demos/Week_02_3_Tree_Based_Regression_Classification.ipynb`](demos/Week_02_3_Tree_Based_Regression_Classification.ipynb) |
| **Week 02 Bonus** | Intercept Diagnostics | Analysis of model fit with and without an intercept | [`demos/Week_02_Bonus_To_Intercept_or_Not.ipynb`](demos/Week_02_Bonus_To_Intercept_or_Not.ipynb) |
| **Week 03.1** | Clustering | Hierarchical clustering and K-Means | [`demos/Week_03_1_Hierarchical_Clustering_KMeans.ipynb`](demos/Week_03_1_Hierarchical_Clustering_KMeans.ipynb) |
| **Week 03.2** | PCA & Anomaly Detection | Dimensionality reduction and outlier detection | [`demos/Week_03_2_PCA_Anomaly_Detection.ipynb`](demos/Week_03_2_PCA_Anomaly_Detection.ipynb) |
| **Week 03 Bonus** | Raindrop Plot | Data visualization with custom raindrop plots | [`demos/Week_03_Bonus_Raindrop_Plot.ipynb`](demos/Week_03_Bonus_Raindrop_Plot.ipynb) |
| **Week 03 Readings**| Feature Transformation | Box-Cox transforms and feature standardization | [`demos/Week_03_Readings_Standardize_Transform.ipynb`](demos/Week_03_Readings_Standardize_Transform.ipynb) |
| **Week 04.1** | Stepwise Selection | Best subset, forward, and backward selection | [`demos/Week_04_1_Stepwise_Selection.ipynb`](demos/Week_04_1_Stepwise_Selection.ipynb) |
| **Week 04.2** | Regularization | Ridge (L2) and Lasso (L1) regression | [`demos/Week_04_2_L1_L2_Regularization.ipynb`](demos/Week_04_2_L1_L2_Regularization.ipynb) |
| **Week 04.3** | Natural Language Processing | Text classification with TF-IDF and Naive Bayes | [`demos/Week_04_3_Natural_Language_Processing.ipynb`](demos/Week_04_3_Natural_Language_Processing.ipynb) |
| **Week 04 Bonus** | Plot Formatting | Consistent visualization styles for publication | [`demos/Week_04_Bonus_Standard_Plot_Format.ipynb`](demos/Week_04_Bonus_Standard_Plot_Format.ipynb) |
| **Week 04A** | Feature Selection (BIC & RFE) | Powersets, AIC/BIC selection, and Recursive Feature Elimination | [`demos/4 Week 4A feature_selection_expanded with BIC and RFE v3.ipynb`](demos/4%20Week%204A%20feature_selection_expanded%20with%20BIC%20and%20RFE%20v3.ipynb) |
| **Week 05.1** | Neural Network Basics | Multi-layer perceptron on Pima diabetes data | [`demos/Week_05_1_Pima_Indian_Classification.ipynb`](demos/Week_05_1_Pima_Indian_Classification.ipynb) |
| **Week 05 Bonus** | Numeric Distributions | Exploratory histogram visualization | [`demos/Week_05_Bonus_Histograms.ipynb`](demos/Week_05_Bonus_Histograms.ipynb) |
| **Week 06.1** | Early Stopping | Regularization and loss monitoring during training | [`demos/Week_06_1_Early_Stopping.ipynb`](demos/Week_06_1_Early_Stopping.ipynb) |
| **Week 06.2** | Optimization | Gradient descent optimizers and learning rates | [`demos/Week_06_2_Optimization.ipynb`](demos/Week_06_2_Optimization.ipynb) |
| **Week 06.3** | Cross-Validation | K-Fold, Stratified K-Fold, and leave-one-out CV | [`demos/Week_06_3_Resampling_Cross_Validation.ipynb`](demos/Week_06_3_Resampling_Cross_Validation.ipynb) |
| **Week 06.4** | Model Comparison | Comparing neural network architectures | [`demos/Week_06_4_Pima_Indian_Classification.ipynb`](demos/Week_06_4_Pima_Indian_Classification.ipynb) |
| **Week 06 Bonus** | Data Splitting | Train, validation, and test split strategies | [`demos/Week_06_Bonus_Splitting.ipynb`](demos/Week_06_Bonus_Splitting.ipynb) |
| **Week 07.1** | TensorFlow Regression | Building regression models with Keras | [`demos/Week_07_1_Regression_TensorFlow.ipynb`](demos/Week_07_1_Regression_TensorFlow.ipynb) |
| **Week 07.2** | Binary Classification | Deep learning for binary classification | [`demos/Week_07_2_Binary_Classification.ipynb`](demos/Week_07_2_Binary_Classification.ipynb) |
| **Week 07.3** | Hyperparameter Sweeps | Systematic hyperparameter tuning | [`demos/Week_07_3_Hyperparameter_Classification.ipynb`](demos/Week_07_3_Hyperparameter_Classification.ipynb) |
| **Week 08.1** | Autoencoders | Dimensionality reduction with autoencoders | [`demos/Week_08_1_Autoencoder.ipynb`](demos/Week_08_1_Autoencoder.ipynb) |
| **Week 08.2** | Image Autoencoders | Feature extraction and classification on Fashion-MNIST | [`demos/Week_08_2_Autoencoder.ipynb`](demos/Week_08_2_Autoencoder.ipynb) |
| **Week 08.3** | Dropout Regularization | Preventing overfitting with dropout layers | [`demos/Week_08_3_Dropout_Regularization.ipynb`](demos/Week_08_3_Dropout_Regularization.ipynb) |
| **Week 08.4** | Deep Network Regularization | Weight decay, dropout, and capacity tuning | [`demos/Week_08_4_NN_Regularization.ipynb`](demos/Week_08_4_NN_Regularization.ipynb) |
| **Week 08 Bonus** | Baseline Models | Establishing baseline performance thresholds | [`demos/Week_08_Bonus_Trivial_Models.ipynb`](demos/Week_08_Bonus_Trivial_Models.ipynb) |
| **Week 09.1** | ML Debugging | Diagnosing common model training issues | [`demos/Week_09_1_General_ML_Debugging.ipynb`](demos/Week_09_1_General_ML_Debugging.ipynb) |
| **Week 09.2** | Regression Debugging | Identifying error causes in regression models | [`demos/Week_09_2_Debugging_Regression.ipynb`](demos/Week_09_2_Debugging_Regression.ipynb) |
| **Week 09.3** | Classification Debugging | Troubleshooting classification convergence | [`demos/Week_09_3_Debugging_Classification.ipynb`](demos/Week_09_3_Debugging_Classification.ipynb) |
| **Week 09.4** | Model Checkpointing | Saving optimal model weights during training | [`demos/Week_09_4_Checkpointing.ipynb`](demos/Week_09_4_Checkpointing.ipynb) |
| **Week 09 Bonus** | Network Visualization | Visualizing network topology with `ann_visualizer` | [`demos/Week_09_Bonus_Ann_viz.ipynb`](demos/Week_09_Bonus_Ann_viz.ipynb) |
| **HW 2** | Homework 2 Template | Classical ML, feature transformations, and Logit modeling | [`demos/Homework_2_template_v7.ipynb`](demos/Homework_2_template_v7.ipynb) |
| **HW 3** | Homework 3 Template | SQL database loading, BIC selection, and RFE on weather data | [`demos/Homework_3_template_v5.ipynb`](demos/Homework_3_template_v5.ipynb) |
| **Tutorial** | Load Database Tutorial | Querying multiple SQLite database tables and fitting Logit model | [`demos/load_database_tutorial_v2.ipynb`](demos/load_database_tutorial_v2.ipynb) |
