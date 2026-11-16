# FreshCart Data Engineering Projects

This repository contains three small, independently runnable data projects:

1. A Snowflake ELT notebook using sample FreshCart order data.
2. An Iris classification pipeline built with Mage.
3. A RabbitMQ topic-routing demo with a Streamlit dashboard.

## Repository layout

```text
elt/freshcart_elt.ipynb            Sample-data ELT workflow for Snowflake
iris_project/                      Mage Iris classification project
  data_loaders/                    Loads the Iris dataset
  transformers/                    Splits data, trains, and evaluates the model
  data_exporters/                  Exports test predictions
  pipelines/iris_classifier/       Mage pipeline graph and variables
stream/                            RabbitMQ dispatcher, drivers, and dashboard
tests/                             Automated project tests
requirements.txt                   Python dependency pins
.github/workflows/ci.yml           GitHub Actions test workflow
```

## Requirements and installation

The project is tested with Python 3.12. From the repository root in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Iris Mage pipeline

The pipeline uses scikit-learn's built-in Iris dataset (150 rows), creates an
80/20 train/test split, trains a decision tree, and evaluates its predictions.
The Mage pipeline variable `max_depth` is currently set to `5`.

### Run from the command line

From the repository root:

```powershell
.\.venv\Scripts\mage.exe run iris_project iris_classifier
```

The evaluation block prints a confusion matrix and accuracy, macro-precision,
macro-recall, and macro-F1 metrics. The training block saves `iris_model.pkl`;
the exporter saves `iris_predictions.csv`. Both paths are relative to the
pipeline process's current working directory.

### Open the Mage UI

```powershell
.\.venv\Scripts\python.exe iris_project\main.py
```

This starts Mage if it is not already running and opens the Iris pipeline at
<http://localhost:6789/pipelines/iris_classifier>. The launcher opens the UI;
it does not itself run the pipeline.

**Windows note:** In this project's Mage 0.9.80 setup, the UI's Run Once has
previously failed inside Mage's process queue with `KeyError: 'generic_job_2'`,
while the CLI pipeline run succeeded. If this UI issue occurs, use the CLI
command above; it is separate from the model's training and evaluation logic.

### Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/test_prepare_data.py
```

GitHub Actions runs the complete test suite on pushes and pull requests to
`main`.

## FreshCart ELT notebook

Open `elt/freshcart_elt.ipynb` in Jupyter and run its cells from top to bottom.
It demonstrates extracting mock website/mobile order and reference data,
loading raw data into Snowflake, and transforming it into silver and gold
tables. The notebook uses sample data rather than calling live order APIs.

The notebook needs `snowflake-connector-python` and access to a Snowflake
account. Review its connection settings and supply your own credentials; never
commit passwords or other secrets.

## RabbitMQ dispatch demo

`stream/app.py` is a Streamlit dashboard for a RabbitMQ topic exchange. It
starts a message dispatcher and selected driver consumers, displays ACK/NACK
events, and includes a fixed topic-routing test. The app requires a reachable
RabbitMQ broker and a root-level `.env` file containing:

```dotenv
RABBITMQ_URL=amqps://<your-broker-connection-url>
```

The `.env` file is ignored by Git. Do not commit broker credentials.

The base `requirements.txt` includes the RabbitMQ client and dotenv support.
The dashboard also needs `streamlit` and `streamlit-autorefresh`; install them
if you plan to run this optional component:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit streamlit-autorefresh
.\.venv\Scripts\python.exe -m streamlit run stream/app.py
```

The root-level `sample.py`, `test_connection.py`, `test_tls.py`, and
`test_tls12.py` are standalone RabbitMQ connection/TLS diagnostics. They are
not required to run the Iris pipeline or the ELT notebook.