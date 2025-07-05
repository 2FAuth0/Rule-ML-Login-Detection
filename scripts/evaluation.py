import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import os

def evaluate_and_save_metrics(df, label_col, pred_col, name, out_dir = "results/evaluation"):
    os.makedirs(out_dir, exist_ok = True)

    # 1) Metrics Report
    y_true = df[label_col]
    y_pred = df[pred_col]

    report_dict = classification_report(y_true, y_pred, output_dict = True, digits = 4)
    report_text = classification_report(y_true, y_pred, digits = 4)
    matrix = confusion_matrix(y_true, y_pred)

    # Save metrics to text file
    with open(f"{out_dir}/{name.lower().replace(' ', '_')}_metrics.txt", "w") as f:
        f.write(f"==== {name} ====\n\n")
        f.write(report_text + "\n")
        f.write("Confusion Matrix:\n")
        f.write(str(matrix)+ "\n")

    # 2) Confusion Matrix Plot
    plt.figure(figsize = (5, 4))
    sns.heatmap(matrix, annot = True, fmt = "d", cmap = "Blues",
                xticklabels = ["Normal", "Attacker"], yticklabels = ["Normal", "Attacker"])
    plt.title(f"{name} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/{name.lower().replace(' ', '_')}_cm.png")
    plt.close()

    return {
        "Model": name,
        "Class 0 Precision": report_dict["0"]["precision"],
        "Class 0 Recall": report_dict["0"]["recall"],
        "Class 0 F1": report_dict["0"]["f1-score"],
        "Class 1 Precision": report_dict["1"]["precision"],
        "Class 1 Recall": report_dict["1"]["recall"],
        "Class 1 F1": report_dict["1"]["f1-score"],
        "Accuracy": report_dict["accuracy"]
    }

# Usage
if __name__ == "__main__":
    os.makedirs("results/evaluation", exist_ok = True)

    files = {
        "Rule-Based": ("results/rule_based_flags.csv", "true_label", "rule_prediction"),
        "ML-Based": ("results/keystroke_ml_predictions.csv", "true_label", "prediction"),
        "Hybrid (Pipeline)": ("results/pipeline_flags.csv", "true_label", "final_flag")
    }
    
    metrics_summary = []

    for name, (path, y_col, p_col) in files.items():
        if os.path.exists(path):
            df = pd.read_csv(path)
            metrics = evaluate_and_save_metrics(df, y_col, p_col, name)
            metrics_summary.append(metrics)
        else:
            print(f"[WARNING] File not found: {path}")
    
    # 3) Bar Chart Comparing Models
    if metrics_summary:
        summary_df = pd.DataFrame(metrics_summary)
        metric_cols = ["Class 0 Precision", "Class 0 Recall", "Class 0 F1",
                       "Class 1 Precision", "Class 1 Recall", "Class 1 F1", "Accuracy"]
        melted = pd.melt(summary_df, id_vars = "Model", value_vars = metric_cols,
                         var_name = "Metric", value_name = "Score")
        plt.figure(figsize = (14, 6))
        sns.barplot(data = melted, x = "Metric", y = "Score", hue = "Model")
        plt.title("Performance Metrics by Detection Method")
        plt.legend(title = "Model", bbox_to_anchor = (1.01, 1), loc = "upper left", borderaxespad = 0)
        plt.xticks(rotation = 45)
        plt.ylim(0, 1.05)
        plt.tight_layout()
        plt.savefig("results/evaluation/metrics_comparison_barplot.png")
        plt.close()