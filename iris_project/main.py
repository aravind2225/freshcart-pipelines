from iris_project.data_exporters.save_results import export_data
from iris_project.data_loaders.load_iris import load_data
from iris_project.transformers.evaluate_model import evaluate
from iris_project.transformers.prepare_data import transform
from iris_project.transformers.train_model import train


def main(max_depth: int = 3):
    """Run the Iris pipeline and return its evaluation metrics."""
    data = load_data()
    prepared_data = transform(data)
    predictions = train(prepared_data, max_depth=max_depth)
    metrics = evaluate(predictions)
    export_data(predictions)

    print("\nEvaluation metrics:")
    print(metrics.to_string(index=False))
    return metrics


if __name__ == "__main__":
    main()
