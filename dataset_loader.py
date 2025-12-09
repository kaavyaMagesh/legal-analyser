import os

# Change this to your actual dataset location
DATASET_ROOT = "/home/yourusername/datasets/kageneko/legal-case-document-summarization/versions/1/dataset"


def load_dataset_texts():
    """
    Loads all .txt files from:
        IN-Abs/test-data/judgement/*.txt
    """

    judgement_dir = os.path.join(DATASET_ROOT, "IN-Abs", "test-data", "judgement")

    samples = []

    for fname in os.listdir(judgement_dir):
        if fname.endswith(".txt"):
            path = os.path.join(judgement_dir, fname)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                samples.append({
                    "id": fname.replace(".txt", ""),
                    "content": f.read()
                })

    return samples
