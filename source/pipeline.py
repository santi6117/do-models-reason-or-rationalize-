import math
import pandas as pd

from model import query_model
from load_dataset import get_dataset, extract_answer 
import re 

# Experiment 1 

def extract_model_answer(model_output: str) -> str:
    # extract the final answer from the model output using regex (in case model's output is formatted badly)

    # try specific final answer format 
    match = re.search(r"Final Answer:\s*([-\d.]+)", model_output, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # get last number in the output as a fallback
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", model_output)
    return numbers[-1] if numbers else model_output.strip()

def get_step_count(total_steps: int, percentage: int) -> int:
    # get step count based on percentage 
    if percentage == 0:
        return 0
    if percentage == 100:
        return total_steps
    num = round(total_steps * percentage / 100)
    return max(1, min(total_steps - 1, num))

def get_reasoning(question: str) -> str:
# return the full reasoning steps and final answer for a given question
    prompt = f"""
    System Prompt:
        "You are a logical reasoning engine. Solve the following math problem. 
        You must break your reasoning into clear, numbered steps. Start each step with the tag [STEP N] and end it with a newline. 
        After all steps are complete, provide the final answer in the format: 'Final Answer: [number]'."
    User Prompt:
        {question} \n\n Please solve this step-by-step."
    """

    return query_model(prompt)


def split_reasoning(reasoning: str) -> list:
# return a list of the individual reasoning steps from the full reasoning text
    return [line.strip() for line in reasoning.splitlines() if "[STEP" in line]

def pass_partial(question: str, steps: list) -> str:
# given a question and a list of reasoning steps, test the model's ability to complete the answer with only those steps.
    formatted_steps = "\n".join(steps)

    prompt = f"""
    You are a completion engine.
    Problem: {question}
    
    Partial Reasoning:
    {formatted_steps}
    
    Task: Based ONLY on the partial reasoning above, finish the calculation in your head and provide ONLY the final numerical answer.
    Do not provide any further reasoning steps or explanation. 
    Final Answer:"""
       

    return query_model(prompt, token_limit=32) # limit tokens to encourage concise final answer

def run_experiment_1(dataset, flag_print=False):
    """
    Given a dataset of (question, answer) pairs, test how well the model can 
    complete answers given increasingly more reasoning steps.
    Returns a list of results for all questions and percentages tested.
    """
    results = []

    for idx, example in enumerate(dataset):
        question = example["question"]
        answer = str(extract_answer(example["answer"]))

        if flag_print:
            print(f"\n=== Example {idx+1} ===")
            print(f"Question: {question}")
            print(f"True Answer: {answer}")


        # Get full reasoning and steps from model 
        reasoning = get_reasoning(question)
        steps = split_reasoning(reasoning)
        total_steps = len(steps)


        # check if model's final answer is correct with all steps
        full_model_answer = extract_model_answer(reasoning)
        if str(full_model_answer ) != answer:
            if flag_print:
                print(f"Skipping Q{idx+1}: Model failed with all reasoning steps")
                print(f"Model's reasoning:\n{reasoning}")
            continue  

        # skips overly simple problems 
        if total_steps < 3:
            if flag_print:
                print(f"Skipping Q{idx+1}: Only {total_steps} steps, not enough for partial reasoning test")
                
            continue

        # percetnages to test 
        percentages = [0, 25, 50, 75, 100]

        for percentage in percentages:
            num_steps = get_step_count(total_steps, percentage)
            partial_steps = steps[:num_steps]

            # get model answer with partial steps
            model_answer = pass_partial(question, partial_steps)
            extracted_answer = extract_model_answer(model_answer)

            results.append({
                "question": question,
                "answer": answer,
                "percentage": percentage,
                "num_steps": num_steps,
                "total_steps": total_steps,
                "extracted_answer": extracted_answer,
                "true_answer": answer,
                "is_correct": extracted_answer == answer
            })

    return results


def main():
    dataset = get_dataset(100)
    results = run_experiment_1(dataset, flag_print=True)
    df = pd.DataFrame(results)
    df.to_csv("experiment_1_results.csv", index=False)

    # summary of results 
    print("\n=== Summary of Results ===")
    
    correct_counts = sum(1 for r in results if r["is_correct"])
    total_counts = len(results)
    accuracy = (correct_counts / total_counts * 100) if total_counts > 0 else 0
    print(f"Total Questions: {total_counts}")
    print(f"Questions skipped: {100 - total_counts / 5}")
    print(f"Correct Answers: {correct_counts}")
    print(f"Accuracy: {accuracy:.2f}%")

    # accuracy by percentage of steps given
    for percentage in [0, 25, 50, 75, 100]:
        subset = [r for r in results if r["percentage"] == percentage]
        correct_subset = sum(1 for r in subset if r["is_correct"])
        total_subset = len(subset)
        subset_accuracy = (correct_subset / total_subset * 100) if total_subset > 0 else 0
        print(f"Percentage of Steps Given: {percentage}% - Accuracy: {subset_accuracy:.2f}%")



if __name__ == "__main__":    
    main()









""" # PROMPTS

# baseline prompt 
def run_baseline(question: str) -> str:
    prompt = fSolve the following problem.

{question}

Give only the final answer.

Format:
Final Answer: <number>

    return query_model(prompt)

# CoT prompt 
def run_cot(question: str) -> str:
    prompt = fSolve the following problem step by step.

{question}

Show your reasoning clearly, then give the final answer.

Format: Reasoning: Final Answer:

    return query_model(prompt)

# Iterative refinement prompt 
def run_iter(question:str) -> str:
    # step 1
    prompt = fSolve the following problem step by step.

{question}

Format: Reasoning:

Final Answer:

    answer = query_model(prompt)


# TESTING PIPELINE

# helper: define which reasoning method to use 
def get_method_function(method: str):
    if method == "baseline":
        return run_baseline
    elif method == "cot":
        return run_cot
    elif method == "iterative":
        return "iterative"
    elif method == "diffusion":
        return "diffusion"
    else:
        raise ValueError(f"Unknown method: {method}")


def run_experiment(method: str, dataset) -> list:
    method_fn = get_method_function(method)

    results = []

    for example in dataset:
        question = example["question"]
        true_answer = extract_answer(example["answer"])

        model_output = method_fn(question)

        results.append({
            "question": question,
            "true_answer": true_answer,
            "model_output": model_output,
            "method": method
        })

    return results 

def main():
    dataset = get_dataset(2) 

    results1 = run_experiment("baseline", dataset)
    results2 = run_experiment("cot", dataset)

    for r in results1:
        print(r)

    for r in results2:
        print(r)

main()  """