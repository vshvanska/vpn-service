import matplotlib
import base64
import matplotlib.pyplot as plt
from io import BytesIO

matplotlib.use("agg")


def generate_bar_chart(labels, values, title, xlabel, ylabel):
    plt.bar(labels, values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    chart_data = base64.b64encode(buffer.read()).decode("utf-8")
    return chart_data


def generate_line_chart(labels, values, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(labels, values, marker="o", linestyle="-", color="b")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    chart_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return chart_data
