"""
DASC-522 Demo Migration Engine
Handles splitting monolithic notebook into sub-weekly modular demos,
rewriting dataset references to canonical raw GitHub / GCS HTTPS URLs,
adding Open-in-Colab badges, and producing Canvas-ready link tables.
"""

import os
import json
import re
import csv
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

# Constants
DEFAULT_REPO = "DataAnalytics808/DASC-522-demo-repository"
DEFAULT_BRANCH = "main"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{DEFAULT_REPO}/{DEFAULT_BRANCH}/data"
GCS_BASE = "https://storage.googleapis.com/dasc-522-course-data"
SIZE_THRESHOLD_BYTES = 25 * 1024 * 1024  # 25 MB

@dataclass
class DemoDefinition:
    demo_number: str
    title: str
    filename: str
    start_cell: int
    end_cell: int
    datasets: List[str] = field(default_factory=list)
    dataset_storage: str = "GitHub"  # 'GitHub', 'GCS', or 'None'
    description: str = ""
    extra_imports: List[str] = field(default_factory=list)
    setup_code: str = ""

def generate_colab_url(repo: str, branch: str, notebook_path: str) -> str:
    """Generate canonical direct Open-in-Colab URL."""
    # Ensure no leading slash in notebook_path
    clean_path = notebook_path.lstrip("/")
    return f"https://colab.research.google.com/github/{repo}/blob/{branch}/{clean_path}"

def create_colab_badge_cell(colab_url: str) -> dict:
    """Create a Markdown cell containing the Open in Colab badge."""
    markdown_content = (
        f'<a href="{colab_url}" target="_parent">'
        f'<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>'
        f'</a>\n'
    )
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [markdown_content]
    }

def classify_dataset_storage(filename: str, size_bytes: int) -> str:
    """Classify dataset storage location based on the 25 MB rule."""
    if size_bytes > SIZE_THRESHOLD_BYTES:
        return "GCS"
    return "GitHub"

def rewrite_cell_for_colab(source: str, dataset_mapping: Dict[str, str], colab_url: str) -> str:
    """
    Rewrite a cell's source code:
    1. Strip Google Drive mounting and Mac mini path switching.
    2. Replace local file references with canonical DATA_URL or direct fetch.
    """
    lines = source.split("\n")
    cleaned_lines = []
    skip_mode = False

    for line in lines:
        stripped = line.strip()
        # Drop Google Drive mount lines and local Mac chdir
        if "drive.mount" in stripped or "google_drive_path" in stripped:
            continue
        if stripped.startswith("os.chdir(google_drive_path)"):
            continue
        if "from google.colab import files, drive" in stripped:
            line = line.replace(", drive", "").replace("drive,", "")
            if stripped == "from google.colab import files, drive":
                continue
        cleaned_lines.append(line)

    rewritten_source = "\n".join(cleaned_lines)

    # Rewrite dataset reading
    for filename, remote_url in dataset_mapping.items():
        if filename in rewritten_source:
            # Replace 'filename' or "filename" inside common reading/loading functions
            for fn in ["pd.read_csv", "pd.read_excel", "pd.read_table", "tf.keras.models.load_model"]:
                rewritten_source = re.sub(
                    rf'{re.escape(fn)}\(\s*[\'\"]{re.escape(filename)}[\'\"]',
                    f'{fn}("{remote_url}"',
                    rewritten_source
                )

    return rewritten_source

def create_base_notebook_structure() -> dict:
    """Return standard Jupyter notebook v4 template."""
    return {
        "cells": [],
        "metadata": {
            "colab": {
                "provenance": []
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

def extract_demo_notebook(
    master_nb: dict,
    demo: DemoDefinition,
    repo: str = DEFAULT_REPO,
    branch: str = DEFAULT_BRANCH,
    raw_base_url: str = GITHUB_RAW_BASE,
    gcs_base_url: str = GCS_BASE
) -> dict:
    """Extract a single self-contained demo notebook from the master notebook."""
    nb = create_base_notebook_structure()
    nb_path = f"demos/{demo.filename}"
    colab_url = generate_colab_url(repo, branch, nb_path)

    # 1. Add Open in Colab badge cell
    nb["cells"].append(create_colab_badge_cell(colab_url))

    # 2. Build dataset mapping for this demo
    dataset_mapping = {}
    for ds in demo.datasets:
        storage = classify_dataset_storage(ds, 0) # default check
        if ds in ["train-images-idx3-ubyte.gz", "8B datafiles.zip"]:
            dataset_mapping[ds] = f"{gcs_base_url}/{ds}"
        else:
            dataset_mapping[ds] = f"{raw_base_url}/{ds}"

    # 3. Check if extra imports or setup cell are needed
    if demo.extra_imports:
        import_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["\n".join(demo.extra_imports) + "\n"]
        }
        nb["cells"].append(import_cell)

    if demo.setup_code:
        setup_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [demo.setup_code + "\n"]
        }
        nb["cells"].append(setup_cell)

    # 4. Extract and rewrite cells
    for i in range(demo.start_cell, demo.end_cell + 1):
        if i >= len(master_nb["cells"]):
            break
        orig_cell = master_nb["cells"][i]
        new_cell = {
            "cell_type": orig_cell["cell_type"],
            "metadata": orig_cell.get("metadata", {}).copy(),
        }
        if orig_cell["cell_type"] == "code":
            new_cell["outputs"] = orig_cell.get("outputs", []).copy()
            new_cell["execution_count"] = orig_cell.get("execution_count", None)

        # Clear outputs or preserve as needed; preserve outputs where available
        source_str = "".join(orig_cell.get("source", []))

        # Check for cell 1041 missing checkpoint fix
        if "381Sum 153FP 228FN 0.828f1.h5" in source_str:
            source_str = source_str.replace(
                "381Sum 153FP 228FN 0.828f1.h5",
                "347Sum 106FP 241FN 0.837f1.h5"
            )

        # Check for Week 8B data extraction fix: download files programmatically if needed
        if demo.filename == "Week_08_B_Autoencoder.ipynb" and "extract_data('train-images-idx3-ubyte.gz'" in source_str:
            # Prepend download logic before extract_data call
            download_block = (
                "# Programmatically download Fashion-MNIST data files if not present\n"
                "import urllib.request, os\n"
                "base_gcs = 'https://storage.googleapis.com/dasc-522-course-data'\n"
                "base_gh = 'https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data'\n"
                "files_to_fetch = [\n"
                "    ('train-images-idx3-ubyte.gz', base_gcs),\n"
                "    ('train-labels-idx1-ubyte.gz', base_gh),\n"
                "    ('t10k-images-idx3-ubyte.gz', base_gh),\n"
                "    ('t10k-labels-idx1-ubyte.gz', base_gh),\n"
                "    ('autoencoder.weights.h5', base_gh),\n"
                "    ('autoencoder_classification.weights.h5', base_gh)\n"
                "]\n"
                "for fname, src in files_to_fetch:\n"
                "    if not os.path.exists(fname):\n"
                "        print(f'Fetching {fname}...')\n"
                "        urllib.request.urlretrieve(f'{src}/{fname}', fname)\n\n"
            )
            source_str = download_block + source_str

        # Check for Week 9F Cade data files download
        if demo.filename == "Week_09_F_Checkpointing.ipynb" and 'pd.read_csv("Cade_X.csv")' in source_str:
            download_block = (
                "# Programmatically download required datasets for checkpointing demo\n"
                "import urllib.request, os\n"
                "base_gh = 'https://raw.githubusercontent.com/DataAnalytics808/DASC-522-demo-repository/main/data'\n"
                "for f in ['Cade_X.csv', 'Cade_y.csv', 'best_model.keras', '347Sum 106FP 241FN 0.837f1.h5']:\n"
                "    if not os.path.exists(f):\n"
                "        urllib.request.urlretrieve(f'{base_gh}/{f}', f)\n\n"
            )
            source_str = download_block + source_str

        rewritten = rewrite_cell_for_colab(source_str, dataset_mapping, colab_url)
        new_cell["source"] = [l + "\n" for l in rewritten.split("\n")[:-1]] + ([rewritten.split("\n")[-1]] if rewritten.split("\n")[-1] else [])
        nb["cells"].append(new_cell)

    return nb

def build_colab_links_table(demos: List[DemoDefinition], repo: str, branch: str) -> Tuple[str, List[Dict[str, str]]]:
    """Build markdown table and CSV rows for COLAB_LINKS."""
    csv_rows = []
    md_lines = [
        "# DASC-522 Course Demonstrations — Direct Colab Launch Links\n",
        "These direct links open each demonstration directly in Google Colab without navigating GitHub.\n",
        "| Demo # | Demonstration Title | GitHub Notebook Path | Direct Open-in-Colab URL | Dataset(s) Used | Storage Location |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for d in demos:
        nb_path = f"demos/{d.filename}"
        colab_url = generate_colab_url(repo, branch, nb_path)
        ds_str = ", ".join(d.datasets) if d.datasets else "None"
        storage_str = d.dataset_storage

        md_line = f"| **{d.demo_number}** | {d.title} | [`{nb_path}`]({nb_path}) | [Open in Colab]({colab_url}) | {ds_str} | {storage_str} |"
        md_lines.append(md_line)

        csv_rows.append({
            "Demo number": d.demo_number,
            "Notebook title": d.title,
            "GitHub notebook path": nb_path,
            "Direct Open-in-Colab URL": colab_url,
            "Dataset(s) used": ds_str,
            "Dataset storage location": storage_str
        })

    return "\n".join(md_lines) + "\n", csv_rows

def get_all_demo_definitions() -> List[DemoDefinition]:
    """Canonical registry of all 31 demonstrations across Weeks 2 through 9."""
    return [
        # Week 2
        DemoDefinition(
            demo_number="Week 02 A",
            title="Regression Review",
            filename="Week_02_A_Regression_Review.ipynb",
            start_cell=10, end_cell=15,
            datasets=[],
            dataset_storage="None",
            description="OLS linear regression review with statsmodels, confidence intervals, and residual QQ plots using Iris data."
        ),
        DemoDefinition(
            demo_number="Week 02 B",
            title="Classification",
            filename="Week_02_B_Classification.ipynb",
            start_cell=16, end_cell=31,
            datasets=["GRE.csv"],
            dataset_storage="GitHub",
            description="Binary logistic regression classification on graduate school admissions dataset with statsmodels and scikit-learn."
        ),
        DemoDefinition(
            demo_number="Week 02 C",
            title="Tree Based Regression & Classification",
            filename="Week_02_C_Tree_Based_Regression_Classification.ipynb",
            start_cell=32, end_cell=156,
            datasets=["Carseats.csv", "Heart.csv", "Hitters.csv", "ISLR_Hitters.csv", "boston_house_prices.csv"],
            dataset_storage="GitHub",
            setup_code="import os\nos.makedirs('images/decision_trees', exist_ok=True)",
            description="Decision trees, bagging, random forests, and gradient boosting using ISLR and Hands-On ML examples."
        ),
        DemoDefinition(
            demo_number="Week 02 Bonus",
            title="To Intercept or Not",
            filename="Week_02_Bonus_To_Intercept_or_Not.ipynb",
            start_cell=157, end_cell=175,
            datasets=["FY20AuditData2.csv"],
            dataset_storage="GitHub",
            description="Statistical deep dive into fitting models with and without y-intercept and assessing residual implications."
        ),
        # Week 3
        DemoDefinition(
            demo_number="Week 03 A",
            title="Hierarchical Clustering & K-Means",
            filename="Week_03_A_Hierarchical_Clustering_KMeans.ipynb",
            start_cell=178, end_cell=213,
            datasets=[],
            dataset_storage="External URL",
            description="Unsupervised learning: hierarchical agglomerative clustering and K-means with dendrograms on Mall Customers."
        ),
        DemoDefinition(
            demo_number="Week 03 B",
            title="PCA & Anomaly Detection",
            filename="Week_03_B_PCA_Anomaly_Detection.ipynb",
            start_cell=214, end_cell=222,
            datasets=[],
            dataset_storage="None",
            extra_imports=["import matplotlib.pyplot as plt"],
            description="Principal Component Analysis for dimensionality reduction and EllipticEnvelope anomaly detection."
        ),
        DemoDefinition(
            demo_number="Week 03 Bonus",
            title="Raindrop Plot Demo",
            filename="Week_03_Bonus_Raindrop_Plot.ipynb",
            start_cell=223, end_cell=229,
            datasets=["drug_consumption.xlsx"],
            dataset_storage="GitHub",
            extra_imports=["import pandas as pd", "import matplotlib.pyplot as plt", "import seaborn as sns"],
            description="Data visualization raincloud / raindrop plots on drug consumption dataset."
        ),
        # Week 4
        DemoDefinition(
            demo_number="Week 04 A",
            title="Stepwise Selection",
            filename="Week_04_A_Stepwise_Selection.ipynb",
            start_cell=231, end_cell=253,
            datasets=["UScrime 2.csv"],
            dataset_storage="GitHub",
            description="Stepwise feature selection using brute force forward / backward elimination and AIC/BIC evaluation on US Crime data."
        ),
        DemoDefinition(
            demo_number="Week 04 B",
            title="L1 & L2 Regularization",
            filename="Week_04_B_L1_L2_Regularization.ipynb",
            start_cell=254, end_cell=321,
            datasets=["Hitters.csv", "Hitters_X_train.csv", "Hitters_X_test.csv", "Hitters_y_train.csv", "Hitters_y_test.csv"],
            dataset_storage="GitHub",
            description="Ridge regression (L2), Lasso (L1), Principal Components Regression, and Partial Least Squares on Hitters dataset."
        ),
        DemoDefinition(
            demo_number="Week 04 C",
            title="Natural Language Processing",
            filename="Week_04_C_Natural_Language_Processing.ipynb",
            start_cell=322, end_cell=352,
            datasets=["NLP Training data.csv"],
            dataset_storage="GitHub",
            description="Text classification NLP workflow comparing classical ML models against dense neural networks."
        ),
        DemoDefinition(
            demo_number="Week 04 Bonus",
            title="Standard Plot Format",
            filename="Week_04_Bonus_Standard_Plot_Format.ipynb",
            start_cell=353, end_cell=357,
            datasets=[],
            dataset_storage="None",
            description="Matplotlib formatting standards and templates for course presentations and reports."
        ),
        # Week 5
        DemoDefinition(
            demo_number="Week 05 A",
            title="Pima Indian Classification",
            filename="Week_05_A_Pima_Indian_Classification.ipynb",
            start_cell=359, end_cell=369,
            datasets=["5A pima-indians-diabetes.data.csv"],
            dataset_storage="GitHub",
            description="Binary classification pipeline and performance metric analysis on Pima Indians diabetes dataset."
        ),
        DemoDefinition(
            demo_number="Week 05 Bonus",
            title="Plotting Histograms of Numeric Variables",
            filename="Week_05_Bonus_Histograms.ipynb",
            start_cell=370, end_cell=372,
            datasets=["Z_X.csv", "Z_y.csv"],
            dataset_storage="GitHub",
            extra_imports=["import pandas as pd", "import matplotlib.pyplot as plt", "import seaborn as sns"],
            description="Feature distribution visualization and skewness inspection across multiple numeric variables."
        ),
        # Week 6
        DemoDefinition(
            demo_number="Week 06 A",
            title="Early Stopping",
            filename="Week_06_A_Early_Stopping.ipynb",
            start_cell=374, end_cell=383,
            datasets=[],
            dataset_storage="None",
            description="Mitigating neural network overfitting using Keras EarlyStopping callback with validation loss monitoring."
        ),
        DemoDefinition(
            demo_number="Week 06 B",
            title="Optimization",
            filename="Week_06_B_Optimization.ipynb",
            start_cell=384, end_cell=403,
            datasets=[],
            dataset_storage="None",
            description="Evaluating Adam, SGD, RMSprop, learning rates, momentum, and batch normalization on neural network convergence."
        ),
        DemoDefinition(
            demo_number="Week 06 C",
            title="Resampling & Cross Validation",
            filename="Week_06_C_Resampling_Cross_Validation.ipynb",
            start_cell=404, end_cell=471,
            datasets=["5A pima-indians-diabetes.data.csv"],
            dataset_storage="GitHub",
            description="Comprehensive cross-validation techniques: K-Fold, Stratified K-Fold, ShuffleSplit, LOOCV, and LPOCV."
        ),
        DemoDefinition(
            demo_number="Week 06 D",
            title="Pima Indian Classification Multi-Model",
            filename="Week_06_D_Pima_Indian_Classification.ipynb",
            start_cell=472, end_cell=482,
            datasets=["5A pima-indians-diabetes.data.csv"],
            dataset_storage="GitHub",
            description="Comparing multiple classification model architectures on Pima Indian diabetes data."
        ),
        DemoDefinition(
            demo_number="Week 06 Bonus",
            title="Dataset Splitting Patterns",
            filename="Week_06_Bonus_Splitting.ipynb",
            start_cell=483, end_cell=484,
            datasets=[],
            dataset_storage="None",
            extra_imports=["import pandas as pd", "import numpy as np"],
            setup_code=("# Initialize synthetic demonstration dataset 'df2' for splitting demo\n"
                        "np.random.seed(42)\n"
                        "df2 = pd.DataFrame({\n"
                        "    'x': np.random.randn(200),\n"
                        "    'y': np.random.randn(200) * 2 + 1,\n"
                        "    'THC': np.random.choice([0, 1], size=200),\n"
                        "    'Length': np.random.uniform(10, 50, size=200)\n"
                        "})"),
            description="Techniques for two-way and three-way train/validation/test dataset splitting in scikit-learn and Keras."
        ),
        # Week 7
        DemoDefinition(
            demo_number="Week 07 A",
            title="Regression TensorFlow Example",
            filename="Week_07_A_Regression_TensorFlow.ipynb",
            start_cell=486, end_cell=616,
            datasets=["dnn_model.keras"],
            dataset_storage="GitHub",
            description="Predicting fuel efficiency with TensorFlow Keras: Normalization layer, single-variable linear, multiple inputs, and DNN regression."
        ),
        DemoDefinition(
            demo_number="Week 07 B",
            title="Binary Classification with TensorFlow",
            filename="Week_07_B_Binary_Classification.ipynb",
            start_cell=617, end_cell=637,
            datasets=[],
            dataset_storage="External URL",
            description="Binary classification on California Housing data with logistic regression vs all-in-one neural network and threshold sweep."
        ),
        DemoDefinition(
            demo_number="Week 07 C",
            title="Hyperparameter Classification",
            filename="Week_07_C_Hyperparameter_Classification.ipynb",
            start_cell=638, end_cell=657,
            datasets=["Diabetes.csv"],
            dataset_storage="GitHub",
            description="Hyperparameter tuning for neural network classification thresholds on Diabetes dataset."
        ),
        # Week 8
        DemoDefinition(
            demo_number="Week 08 A",
            title="Autoencoder Architecture",
            filename="Week_08_A_Autoencoder.ipynb",
            start_cell=659, end_cell=687,
            datasets=[],
            dataset_storage="None",
            description="Building autoencoder architectures with TensorFlow Keras custom layers and training loops on MNIST."
        ),
        DemoDefinition(
            demo_number="Week 08 B",
            title="Autoencoder for Feature Extraction & Classification",
            filename="Week_08_B_Autoencoder.ipynb",
            start_cell=688, end_cell=739,
            datasets=["train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz", "t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz", "autoencoder.weights.h5", "autoencoder_classification.weights.h5"],
            dataset_storage="GCS + GitHub",
            description="Fashion-MNIST autoencoder representation learning and downstream classification with frozen encoder layers."
        ),
        DemoDefinition(
            demo_number="Week 08 C",
            title="Dropout Regularization",
            filename="Week_08_C_Dropout_Regularization.ipynb",
            start_cell=740, end_cell=743,
            datasets=[],
            dataset_storage="None",
            description="Dropout regularization mechanics and effects on dense network weights."
        ),
        DemoDefinition(
            demo_number="Week 08 D",
            title="Neural Network Regularization",
            filename="Week_08_D_NN_Regularization.ipynb",
            start_cell=744, end_cell=820,
            datasets=[],
            dataset_storage="External URL",
            description="Strategies to prevent overfitting on the Higgs dataset: Tiny, Small, Medium, Large models, L2, and combined Dropout."
        ),
        DemoDefinition(
            demo_number="Week 08 Bonus",
            title="Trivial Models Baseline",
            filename="Week_08_Bonus_Trivial_Models.ipynb",
            start_cell=821, end_cell=822,
            datasets=[],
            dataset_storage="None",
            description="Establishing mean/mode dummy predictor baselines to contextualize complex ML model performance."
        ),
        # Week 9
        DemoDefinition(
            demo_number="Week 09 C",
            title="General Machine Learning Debugging",
            filename="Week_09_C_General_ML_Debugging.ipynb",
            start_cell=824, end_cell=866,
            datasets=[],
            dataset_storage="None",
            description="Case studies in debugging ML models: diagnosing exploding gradients, loss plateauing, and learning rate tuning."
        ),
        DemoDefinition(
            demo_number="Week 09 D",
            title="Debugging in Regression",
            filename="Week_09_D_Debugging_Regression.ipynb",
            start_cell=867, end_cell=939,
            datasets=[],
            dataset_storage="External URL",
            description="Debugging regression models on Wine Quality dataset: checking data splits, linear baselines, nonlinear modeling, and bug isolation."
        ),
        DemoDefinition(
            demo_number="Week 09 E",
            title="Debugging in Classification",
            filename="Week_09_E_Debugging_Classification.ipynb",
            start_cell=940, end_cell=1013,
            datasets=[],
            dataset_storage="External URL",
            description="Debugging classification on MNIST: class imbalance checks, loss formulation bugs, model complexity, and data skew."
        ),
        DemoDefinition(
            demo_number="Week 09 F",
            title="Model Checkpointing & Hyperparameter Logging",
            filename="Week_09_F_Checkpointing.ipynb",
            start_cell=1014, end_cell=1041,
            datasets=["Cade_X.csv", "Cade_y.csv", "batch_output.csv", "best_model.keras", "347Sum 106FP 241FN 0.837f1.h5"],
            dataset_storage="GitHub",
            description="Automating ModelCheckpoint callbacks, naming checkpoints by performance, and logging hyperparameters to CSV."
        ),
        DemoDefinition(
            demo_number="Week 09 Bonus",
            title="Neural Network Architecture Visualization",
            filename="Week_09_Bonus_Ann_viz.ipynb",
            start_cell=1042, end_cell=1043,
            datasets=[],
            dataset_storage="None",
            description="Visualizing neural network layer topologies with ann_visualizer."
        ),
    ]

def generate_datasets_markdown(demos: List[DemoDefinition], datasets_dir: str, repo: str, branch: str) -> str:
    """Generate DATASETS.md documenting each dataset, size, notebooks using it, storage location, and canonical URL."""
    # Map datasets to demos
    dataset_usage = {}
    for d in demos:
        for ds in d.datasets:
            dataset_usage.setdefault(ds, []).append(f"{d.demo_number} ({d.title})")

    # Inventory all files in datasets_dir
    files_info = []
    if os.path.exists(datasets_dir):
        for root, dirs, files in os.walk(datasets_dir):
            for f in sorted(files):
                if f == ".DS_Store" or f == "mito-starter-notebook.ipynb":
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, datasets_dir)
                size = os.path.getsize(full_path)
                storage = classify_dataset_storage(f, size)
                if storage == "GCS":
                    canonical_url = f"https://storage.googleapis.com/dasc-522-course-data/{f}"
                else:
                    canonical_url = f"https://raw.githubusercontent.com/{repo}/{branch}/data/{rel_path}"

                used_by = dataset_usage.get(f, [])
                used_by_str = ", ".join(used_by) if used_by else "*Supplementary / Course Reference*"

                files_info.append({
                    "name": f,
                    "rel_path": rel_path,
                    "size": size,
                    "size_str": f"{size:,} bytes ({size/(1024*1024):.2f} MB)" if size > 1024*1024 else f"{size:,} bytes ({size/1024:.1f} KB)",
                    "storage": storage,
                    "url": canonical_url,
                    "used_by": used_by_str
                })

    md_lines = [
        "# DASC-522 Course Datasets Directory\n",
        "This document lists every dataset used in the DASC-522 course demonstrations, its size, storage tier, using notebooks, and canonical HTTPS download URL.\n",
        "## Storage Policy Summary",
        "- **GitHub (`data/`)**: Datasets <= 25 MB are stored directly in this repository and accessed via public raw GitHub URLs.",
        "- **Google Cloud Storage (GCS)**: Datasets > 25 MB are stored in a dedicated public course bucket (`dasc-522-course-data`) with anonymous read access.",
        "- **Direct Colab Loading**: Notebooks load datasets directly via HTTPS URLs without requiring student logins, manual downloads, or Google Drive mounting.\n",
        "## Datasets Inventory Table\n",
        "| Dataset File | Size | Storage | Notebook(s) Using Dataset | Canonical Download URL |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    for item in files_info:
        md_lines.append(
            f"| `{item['rel_path']}` | {item['size_str']} | **{item['storage']}** | {item['used_by']} | [URL]({item['url']}) |"
        )

    return "\n".join(md_lines) + "\n"

def generate_readme_markdown(demos: List[DemoDefinition], repo: str, branch: str) -> str:
    """Generate instructor-facing README.md covering delivery architecture, URLs, and maintenance."""
    lines = [
        "# DASC-522 Machine Learning Demonstrations Repository\n",
        "Welcome to the official repository for **DASC-522 Machine Learning** demonstration notebooks and datasets.\n",
        "## Repository Architecture & Delivery Mechanism\n",
        "This repository serves as the single source of truth for all course demonstrations. It is designed for seamless delivery to students via Canvas LMS and Google Colab:\n",
        "```",
        "Canvas LMS (Module External URL)",
        "       │",
        "       ▼",
        "Direct Colab Launch Link (colab.research.google.com/github/...)",
        "       │",
        "       ▼",
        "Google Colab Environment (Student Account)",
        "       │",
        "       ▼",
        "Select 'Run All' -> Notebook programmatically downloads datasets from GitHub / GCS",
        "```\n",
        "### Key Principles",
        "1. **Zero Student Overhead**: Students do not need a GitHub account, do not need GCP credentials, and do not need to clone the repo or mount Google Drive.",
        "2. **Self-Contained Notebooks**: Every demonstration notebook obtains its required data programmatically via public HTTPS URLs.",
        "3. **Track Current Colab**: Demonstration code runs against today's standard Colab runtime without artificial package freezing or pinned historical libraries.",
        "4. **No Homework Solutions**: This repository contains demonstration notebooks only. Homework solutions are maintained separately.\n",
        "## Directory Structure\n",
        "```",
        "├── demos/             # Sub-weekly self-contained Colab demonstration notebooks",
        "│   ├── Week_02_A_Regression_Review.ipynb",
        "│   ├── Week_02_B_Classification.ipynb",
        "│   └── ...",
        "├── data/              # Small course datasets (<= 25 MB) stored directly in GitHub",
        "│   ├── GRE.csv",
        "│   ├── Hitters.csv",
        "│   └── ...",
        "├── maintenance/       # Maintenance and migration scripts",
        "│   └── migrate.py",
        "├── README.md          # Instructor-facing repository documentation (this file)",
        "├── DATASETS.md        # Comprehensive dataset inventory, sizes, and URLs",
        "├── COLAB_LINKS.md     # Ready-to-copy Canvas external URLs for all demonstrations",
        "└── colab_links.csv    # Machine-readable Canvas link exports",
        "```\n",
        "## Dataset Storage Tiering\n",
        "- **Small Datasets (<= 25 MB)**: Stored under `/data/`. Accessed via:",
        f"  `https://raw.githubusercontent.com/{repo}/{branch}/data/<filename>`",
        "- **Large Datasets (> 25 MB)**: Stored in dedicated public read-only Google Cloud Storage bucket (`dasc-522-course-data`). Accessed via:",
        "  `https://storage.googleapis.com/dasc-522-course-data/<filename>`\n",
        "## Canvas Integration\n",
        "To add a demonstration into Canvas as a module item:",
        "1. Open [`COLAB_LINKS.md`](COLAB_LINKS.md).",
        "2. Copy the corresponding **Direct Open-in-Colab URL** for the demo.",
        "3. In Canvas, add an **External URL** item named `Open in Colab`.",
        "4. Students click the link and immediately begin working in Google Colab.\n",
        "## Demonstration Summary\n",
        f"Total Demonstrations: **{len(demos)}**\n",
        "| Week | Demo # | Demonstration Name | Notebook File |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for d in demos:
        lines.append(f"| {d.demo_number.split()[0]} {d.demo_number.split()[1]} | **{d.demo_number}** | {d.title} | [`{d.filename}`](demos/{d.filename}) |")

    return "\n".join(lines) + "\n"

def run_full_migration(
    master_nb_path: str,
    datasets_dir: str,
    output_repo_path: str,
    repo: str = DEFAULT_REPO,
    branch: str = DEFAULT_BRANCH
) -> dict:
    """Execute complete migration into target repository directory."""
    import shutil
    print(f"Starting migration from '{master_nb_path}' into '{output_repo_path}'...")

    demos_dir = os.path.join(output_repo_path, "demos")
    data_dir = os.path.join(output_repo_path, "data")
    maint_dir = os.path.join(output_repo_path, "maintenance")

    os.makedirs(demos_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(maint_dir, exist_ok=True)

    # 1. Copy datasets <= 25MB to data/
    copied_datasets = []
    gcs_datasets = []
    if os.path.exists(datasets_dir):
        for root, dirs, files in os.walk(datasets_dir):
            for f in sorted(files):
                if f == ".DS_Store" or f == "mito-starter-notebook.ipynb":
                    continue
                full_src = os.path.join(root, f)
                rel_path = os.path.relpath(full_src, datasets_dir)
                size = os.path.getsize(full_src)
                if size <= SIZE_THRESHOLD_BYTES:
                    dest_path = os.path.join(data_dir, rel_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(full_src, dest_path)
                    copied_datasets.append((rel_path, size))
                else:
                    gcs_datasets.append((rel_path, size))

    print(f"Copied {len(copied_datasets)} small datasets to data/")
    print(f"Identified {len(gcs_datasets)} large datasets for GCS")

    # 2. Load master notebook
    with open(master_nb_path, "r", encoding="utf-8") as f:
        master_nb = json.load(f)

    # 3. Extract all demo notebooks
    demos = get_all_demo_definitions()
    generated_notebooks = []
    for d in demos:
        nb_dict = extract_demo_notebook(master_nb, d, repo=repo, branch=branch)
        out_path = os.path.join(demos_dir, d.filename)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(nb_dict, f, indent=1)
        generated_notebooks.append(out_path)
    print(f"Generated {len(generated_notebooks)} demo notebooks under demos/")

    # 4. Generate COLAB_LINKS.md and colab_links.csv
    colab_links_md, colab_csv_rows = build_colab_links_table(demos, repo, branch)
    with open(os.path.join(output_repo_path, "COLAB_LINKS.md"), "w", encoding="utf-8") as f:
        f.write(colab_links_md)

    csv_path = os.path.join(output_repo_path, "colab_links.csv")
    fieldnames = [
        "Demo number",
        "Notebook title",
        "GitHub notebook path",
        "Direct Open-in-Colab URL",
        "Dataset(s) used",
        "Dataset storage location"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(colab_csv_rows)
    print("Generated COLAB_LINKS.md and colab_links.csv")

    # 5. Generate DATASETS.md
    datasets_md = generate_datasets_markdown(demos, datasets_dir, repo, branch)
    with open(os.path.join(output_repo_path, "DATASETS.md"), "w", encoding="utf-8") as f:
        f.write(datasets_md)
    print("Generated DATASETS.md")

    # 6. Generate README.md
    readme_md = generate_readme_markdown(demos, repo, branch)
    with open(os.path.join(output_repo_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_md)
    print("Generated README.md")

    # 7. Copy migrate.py to maintenance/
    shutil.copy2(__file__, os.path.join(maint_dir, "migrate.py"))

    # 8. Create .gitignore
    gitignore_content = ".DS_Store\n__pycache__/\n*.pyc\n.ipynb_checkpoints/\n"
    with open(os.path.join(output_repo_path, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore_content)

    return {
        "notebooks_count": len(generated_notebooks),
        "small_datasets_count": len(copied_datasets),
        "gcs_datasets_count": len(gcs_datasets),
        "demos_dir": demos_dir,
        "data_dir": data_dir
    }

if __name__ == "__main__":
    import sys
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    master_path = os.path.join(base_dir, "DASC_522_all_code_20260326_pandas_3_fix.ipynb")
    ds_path = os.path.join(base_dir, "Datasets")
    repo_path = os.path.join(base_dir, "repo_clone")
    run_full_migration(master_path, ds_path, repo_path)

