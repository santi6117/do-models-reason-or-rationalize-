from datasets import load_dataset

def get_dataset(n=100):
    dataset = load_dataset("gsm8k", "main")
    return dataset["train"].select(range(n))

def extract_answer(answer_text):
    return answer_text.split("#### ")[-1].strip()

