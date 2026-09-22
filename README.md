# DASC-522 Machine Learning Demonstrations Repository

Welcome to the official repository for **DASC-522 Machine Learning** demonstration notebooks and datasets.

## Repository Architecture & Delivery Mechanism

This repository serves as the single source of truth for all course demonstrations. It is designed for seamless delivery to students via Canvas LMS and Google Colab:

```
Canvas LMS (Module External URL)
       │
       ▼
Direct Colab Launch Link (colab.research.google.com/github/...)
       │
       ▼
Google Colab Environment (Student Account)
       │
       ▼
Select 'Run All' -> Notebook programmatically obtains required datasets and executes
```

### Key Principles
1. **Zero Student Overhead**: Students do not need a GitHub account, do not need GCP credentials, and do not need to clone the repo or mount Google Drive.
2. **Self-Contained Notebooks**: Every demonstration notebook obtains its required data programmatically via public HTTPS URLs or Keras built-in datasets.
3. **Track Current Colab**: Demonstration code runs against today's standard Colab runtime without artificial package freezing or pinned historical libraries.
4. **No Homework Solutions**: This repository contains demonstration notebooks only. Homework solutions are maintained separately.

## Directory Structure

```
├── demos/             # Sub-weekly self-contained Colab demonstration notebooks
│   ├── Week_02_A_Regression_Review.ipynb
│   ├── Week_02_B_Classification.ipynb
│   └── ...
├── data/              # Course datasets (all <= 25 MB) stored directly in GitHub
│   ├── GRE.csv
│   ├── Hitters.csv
│   └── ...
├── maintenance/       # Maintenance and migration scripts
│   └── migrate.py
├── README.md          # Instructor-facing repository documentation (this file)
├── DATASETS.md        # Comprehensive dataset inventory, sizes, and URLs
├── COLAB_LINKS.md     # Ready-to-copy Canvas external URLs for all demonstrations
└── colab_links.csv    # Machine-readable Canvas link exports
```

## Dataset Storage

- **Repository Datasets (`/data/`)**: Stored under `/data/`. Accessed via:
  `https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/<filename>`
- **Built-in Benchmark Datasets**: Datasets like Fashion-MNIST and MNIST are loaded directly via Keras built-in loaders (`keras.datasets.fashion_mnist.load_data()`), eliminating any requirement for Google Cloud Storage or external buckets.

## Canvas Integration

To add a demonstration into Canvas as a module item:
1. Open [`COLAB_LINKS.md`](COLAB_LINKS.md).
2. Copy the corresponding **Direct Open-in-Colab URL** for the demo.
3. In Canvas, add an **External URL** item named `Open in Colab`.
4. Students click the link and immediately begin working in Google Colab.

## Demonstration Summary

Total Demonstrations: **31**

| Week | Demo # | Demonstration Name | Notebook File |
| :--- | :--- | :--- | :--- |
| Week 02 | **Week 02 A** | Regression Review | [`Week_02_A_Regression_Review.ipynb`](demos/Week_02_A_Regression_Review.ipynb) |
| Week 02 | **Week 02 B** | Classification | [`Week_02_B_Classification.ipynb`](demos/Week_02_B_Classification.ipynb) |
| Week 02 | **Week 02 C** | Tree Based Regression & Classification | [`Week_02_C_Tree_Based_Regression_Classification.ipynb`](demos/Week_02_C_Tree_Based_Regression_Classification.ipynb) |
| Week 02 | **Week 02 Bonus** | To Intercept or Not | [`Week_02_Bonus_To_Intercept_or_Not.ipynb`](demos/Week_02_Bonus_To_Intercept_or_Not.ipynb) |
| Week 03 | **Week 03 A** | Hierarchical Clustering & K-Means | [`Week_03_A_Hierarchical_Clustering_KMeans.ipynb`](demos/Week_03_A_Hierarchical_Clustering_KMeans.ipynb) |
| Week 03 | **Week 03 B** | PCA & Anomaly Detection | [`Week_03_B_PCA_Anomaly_Detection.ipynb`](demos/Week_03_B_PCA_Anomaly_Detection.ipynb) |
| Week 03 | **Week 03 Bonus** | Raindrop Plot Demo | [`Week_03_Bonus_Raindrop_Plot.ipynb`](demos/Week_03_Bonus_Raindrop_Plot.ipynb) |
| Week 04 | **Week 04 A** | Stepwise Selection | [`Week_04_A_Stepwise_Selection.ipynb`](demos/Week_04_A_Stepwise_Selection.ipynb) |
| Week 04 | **Week 04 B** | L1 & L2 Regularization | [`Week_04_B_L1_L2_Regularization.ipynb`](demos/Week_04_B_L1_L2_Regularization.ipynb) |
| Week 04 | **Week 04 C** | Natural Language Processing | [`Week_04_C_Natural_Language_Processing.ipynb`](demos/Week_04_C_Natural_Language_Processing.ipynb) |
| Week 04 | **Week 04 Bonus** | Standard Plot Format | [`Week_04_Bonus_Standard_Plot_Format.ipynb`](demos/Week_04_Bonus_Standard_Plot_Format.ipynb) |
| Week 05 | **Week 05 A** | Pima Indian Classification | [`Week_05_A_Pima_Indian_Classification.ipynb`](demos/Week_05_A_Pima_Indian_Classification.ipynb) |
| Week 05 | **Week 05 Bonus** | Plotting Histograms of Numeric Variables | [`Week_05_Bonus_Histograms.ipynb`](demos/Week_05_Bonus_Histograms.ipynb) |
| Week 06 | **Week 06 A** | Early Stopping | [`Week_06_A_Early_Stopping.ipynb`](demos/Week_06_A_Early_Stopping.ipynb) |
| Week 06 | **Week 06 B** | Optimization | [`Week_06_B_Optimization.ipynb`](demos/Week_06_B_Optimization.ipynb) |
| Week 06 | **Week 06 C** | Resampling & Cross Validation | [`Week_06_C_Resampling_Cross_Validation.ipynb`](demos/Week_06_C_Resampling_Cross_Validation.ipynb) |
| Week 06 | **Week 06 D** | Pima Indian Classification Multi-Model | [`Week_06_D_Pima_Indian_Classification.ipynb`](demos/Week_06_D_Pima_Indian_Classification.ipynb) |
| Week 06 | **Week 06 Bonus** | Dataset Splitting Patterns | [`Week_06_Bonus_Splitting.ipynb`](demos/Week_06_Bonus_Splitting.ipynb) |
| Week 07 | **Week 07 A** | Regression TensorFlow Example | [`Week_07_A_Regression_TensorFlow.ipynb`](demos/Week_07_A_Regression_TensorFlow.ipynb) |
| Week 07 | **Week 07 B** | Binary Classification with TensorFlow | [`Week_07_B_Binary_Classification.ipynb`](demos/Week_07_B_Binary_Classification.ipynb) |
| Week 07 | **Week 07 C** | Hyperparameter Classification | [`Week_07_C_Hyperparameter_Classification.ipynb`](demos/Week_07_C_Hyperparameter_Classification.ipynb) |
| Week 08 | **Week 08 A** | Autoencoder Architecture | [`Week_08_A_Autoencoder.ipynb`](demos/Week_08_A_Autoencoder.ipynb) |
| Week 08 | **Week 08 B** | Autoencoder for Feature Extraction & Classification | [`Week_08_B_Autoencoder.ipynb`](demos/Week_08_B_Autoencoder.ipynb) |
| Week 08 | **Week 08 C** | Dropout Regularization | [`Week_08_C_Dropout_Regularization.ipynb`](demos/Week_08_C_Dropout_Regularization.ipynb) |
| Week 08 | **Week 08 D** | Neural Network Regularization | [`Week_08_D_NN_Regularization.ipynb`](demos/Week_08_D_NN_Regularization.ipynb) |
| Week 08 | **Week 08 Bonus** | Trivial Models Baseline | [`Week_08_Bonus_Trivial_Models.ipynb`](demos/Week_08_Bonus_Trivial_Models.ipynb) |
| Week 09 | **Week 09 C** | General Machine Learning Debugging | [`Week_09_C_General_ML_Debugging.ipynb`](demos/Week_09_C_General_ML_Debugging.ipynb) |
| Week 09 | **Week 09 D** | Debugging in Regression | [`Week_09_D_Debugging_Regression.ipynb`](demos/Week_09_D_Debugging_Regression.ipynb) |
| Week 09 | **Week 09 E** | Debugging in Classification | [`Week_09_E_Debugging_Classification.ipynb`](demos/Week_09_E_Debugging_Classification.ipynb) |
| Week 09 | **Week 09 F** | Model Checkpointing & Hyperparameter Logging | [`Week_09_F_Checkpointing.ipynb`](demos/Week_09_F_Checkpointing.ipynb) |
| Week 09 | **Week 09 Bonus** | Neural Network Architecture Visualization | [`Week_09_Bonus_Ann_viz.ipynb`](demos/Week_09_Bonus_Ann_viz.ipynb) |
