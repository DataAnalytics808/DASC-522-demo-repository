# DASC-522 Course Datasets Directory

This document lists each dataset used in the DASC-522 course demonstrations, its size, storage location, using notebooks, and canonical HTTPS download URL.

## Storage Policy Summary
- **GitHub (`data/`)**: All demonstration datasets (all <= 25 MB) are stored directly in this repository and accessed via public raw GitHub URLs.
- **Built-in / Public Datasets**: Standard benchmark datasets (e.g. Fashion-MNIST, MNIST, California Housing, Higgs) are loaded directly via Keras built-in loaders or public mirrors.
- **Google Cloud Storage**: Not required. Zero cloud infrastructure or hosting cost.
- **Direct Colab Loading**: Notebooks load datasets directly via HTTPS URLs without requiring student logins, manual downloads, or Google Drive mounting.

## Datasets Inventory Table

Total Active Datasets: **32**

| Dataset File | Size | Storage | Notebook(s) Using Dataset | Canonical Download URL |
| :--- | :--- | :--- | :--- | :--- |
| `347Sum 106FP 241FN 0.837f1.h5` | 1,062,016 bytes (1.01 MB) | **GitHub** | Week 09 F (Model Checkpointing & Hyperparameter Logging) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/347Sum 106FP 241FN 0.837f1.h5) |
| `5A pima-indians-diabetes.data.csv` | 23,278 bytes (22.7 KB) | **GitHub** | Week 05 A (Pima Indian Classification), Week 06 C (Resampling & Cross Validation), Week 06 D (Pima Indian Classification Multi-Model) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/5A pima-indians-diabetes.data.csv) |
| `Cade_X.csv` | 6,173,361 bytes (5.89 MB) | **GitHub** | Week 09 F (Model Checkpointing & Hyperparameter Logging) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Cade_X.csv) |
| `Cade_y.csv` | 58,626 bytes (57.3 KB) | **GitHub** | Week 09 F (Model Checkpointing & Hyperparameter Logging) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Cade_y.csv) |
| `Carseats.csv` | 19,044 bytes (18.6 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Carseats.csv) |
| `Diabetes.csv` | 23,875 bytes (23.3 KB) | **GitHub** | Week 07 C (Hyperparameter Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Diabetes.csv) |
| `FY20AuditData2.csv` | 15,542 bytes (15.2 KB) | **GitHub** | Week 02 Bonus (To Intercept or Not) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/FY20AuditData2.csv) |
| `GRE.csv` | 5,489 bytes (5.4 KB) | **GitHub** | Week 02 B (Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/GRE.csv) |
| `Heart.csv` | 19,925 bytes (19.5 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Heart.csv) |
| `Hitters.csv` | 27,687 bytes (27.0 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification), Week 04 B (L1 & L2 Regularization) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Hitters.csv) |
| `Hitters_X_test.csv` | 10,205 bytes (10.0 KB) | **GitHub** | Week 04 B (L1 & L2 Regularization) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Hitters_X_test.csv) |
| `Hitters_X_train.csv` | 10,041 bytes (9.8 KB) | **GitHub** | Week 04 B (L1 & L2 Regularization) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Hitters_X_train.csv) |
| `Hitters_y_test.csv` | 1,271 bytes (1.2 KB) | **GitHub** | Week 04 B (L1 & L2 Regularization) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Hitters_y_test.csv) |
| `Hitters_y_train.csv` | 1,281 bytes (1.3 KB) | **GitHub** | Week 04 B (L1 & L2 Regularization) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Hitters_y_train.csv) |
| `ISLR_Hitters.csv` | 28,010 bytes (27.4 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/ISLR_Hitters.csv) |
| `NLP Training data.csv` | 21,380 bytes (20.9 KB) | **GitHub** | Week 04 C (Natural Language Processing) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/NLP Training data.csv) |
| `UScrime 2.csv` | 3,376 bytes (3.3 KB) | **GitHub** | Week 04 A (Stepwise Selection) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/UScrime 2.csv) |
| `Z_X.csv` | 212,419 bytes (207.4 KB) | **GitHub** | Week 05 Bonus (Plotting Histograms of Numeric Variables) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Z_X.csv) |
| `Z_y.csv` | 3,774 bytes (3.7 KB) | **GitHub** | Week 05 Bonus (Plotting Histograms of Numeric Variables) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/Z_y.csv) |
| `batch_output.csv` | 20,546 bytes (20.1 KB) | **GitHub** | Week 09 F (Model Checkpointing & Hyperparameter Logging) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/batch_output.csv) |
| `best_model.keras` | 1,052,037 bytes (1.00 MB) | **GitHub** | Week 09 F (Model Checkpointing & Hyperparameter Logging) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/best_model.keras) |
| `boston_house_prices.csv` | 35,200 bytes (34.4 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/boston_house_prices.csv) |
| `dnn_model.keras` | 87,361 bytes (85.3 KB) | **GitHub** | Week 07 A (Regression TensorFlow Example) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/dnn_model.keras) |
| `drug_consumption.xlsx` | 308,300 bytes (301.1 KB) | **GitHub** | Week 03 Bonus (Raindrop Plot Demo) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/drug_consumption.xlsx) |
| `images/decision_trees/decision_tree_decision_boundaries_plot.png` | 98,058 bytes (95.8 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/images/decision_trees/decision_tree_decision_boundaries_plot.png) |
| `images/decision_trees/decision_tree_instability_plot.png` | 88,088 bytes (86.0 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/images/decision_trees/decision_tree_instability_plot.png) |
| `images/decision_trees/iris_tree.dot` | 826 bytes (0.8 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/images/decision_trees/iris_tree.dot) |
| `images/decision_trees/min_samples_leaf_plot.png` | 112,229 bytes (109.6 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/images/decision_trees/min_samples_leaf_plot.png) |
| `images/decision_trees/regression_tree.dot` | 933 bytes (0.9 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/images/decision_trees/regression_tree.dot) |
| `images/decision_trees/sensitivity_to_rotation_plot.png` | 160,796 bytes (157.0 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/images/decision_trees/sensitivity_to_rotation_plot.png) |
| `images/decision_trees/tree_regression_plot.png` | 151,104 bytes (147.6 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/images/decision_trees/tree_regression_plot.png) |
| `images/decision_trees/tree_regression_regularization_plot.png` | 175,108 bytes (171.0 KB) | **GitHub** | Week 02 C (Tree Based Regression & Classification) | [URL](https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data/images/decision_trees/tree_regression_regularization_plot.png) |
