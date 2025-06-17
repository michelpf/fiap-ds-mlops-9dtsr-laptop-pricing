import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("https://dagshub.com/michelpf/fiap-ds-mlops-9dtsr-laptop-pricing.mlflow")
client = MlflowClient()
model_name = "laptop-pricing-model-brl"

# Última versão registrada (modelo em produção)
registered_versions = sorted(
    client.search_model_versions(f"name='{model_name}'"),
    key=lambda v: int(v.version),
    reverse=True
)

if not registered_versions:
    raise ValueError(f"No registered versions found for model '{model_name}'")

prod_version = registered_versions[0]
prod_metrics = client.get_run(prod_version.run_id).data.metrics

# Último run em qualquer experimento
all_runs = mlflow.search_runs(search_all_experiments=True, 
                              order_by=["start_time DESC"], 
                              filter_string="metrics.MAPE > 0",
                              max_results=5)
if all_runs.empty:
    raise ValueError("No experimental runs found.")

latest_exp_run_id = all_runs.iloc[0]["run_id"]
latest_exp_run = client.get_run(latest_exp_run_id)
exp_metrics = latest_exp_run.data.metrics

# Geração de relatório
def format_metrics(metrics: dict):
    return "\n".join([f"- `{k}`: {v:.4f}" for k, v in metrics.items()])

report = f"""
## 📊 MLflow Report: `{model_name}`

### 🏁 Production Model (Last registered version)
- **Run ID**: `{prod_version.run_id}`
- **Model Version**: `{prod_version.version}`

#### 🔢 Metrics
{format_metrics(prod_metrics)}

---

### 🧪 Latest Experimental Run
- **Run ID**: `{latest_exp_run_id}`

#### 🔢 Metrics
{format_metrics(exp_metrics)}

---

### 📈 Metric Comparison
"""

for metric in prod_metrics:
    if metric in exp_metrics:
        delta = exp_metrics[metric] - prod_metrics[metric]
        report += f"- `{metric}`: Experiment = {exp_metrics[metric]:.4f}, Production = {prod_metrics[metric]:.4f}, Δ = {delta:+.4f}\n"

with open("mlflow_report.md", "w") as f:
    f.write(report)

print("MLflow report comparing latest experiment with production model generated.")