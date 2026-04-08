# Research Question
Do strucutred iterative reasoning strategies improve accuracy compared to standard Chain-of-Thought reasoning in large language models?

# Hypothesis 
Iterative reasoning methods will outperform Chain-of-Thought
because they allow correction of earlier reasoning errors.

# Experimental setup
The experiment compares multiple reasoning startegies to the same underlying models, isolating the effect of the reasoning strategy on performance.

## Models evaluated:
One transformer-based language model will be evaluated:
- GPT-4o-mini
(If extra time: Llama-3-8b-Instruct, Mistral7B-Instruct)
All models will use identical generation settings:

> temperature = 0, max_tokens = 512

## Dataset
This experiment will use a subset of 100 questions from GSM8K. 

## Reasoning methods
We evaluate 4 specific reasoning strategies. 
 ### 1. Baseline: direct answer without explicit reasoning instructions.
  - eg. "Solve the following problem: {question}" 
 ### 2. Chain-of-Thought (CoT): single reasoning trajectory prompt. This represents sequential reasoning. 
  - eg. "Solve the following problem step by step: {question}"
 ### 3. Iterative reasoning: multi-step reasoning with explicity critique and revision stages
  - eg. Initial reasoning -> critique reasoning -> revise reasoning - > final answer
 ### 4. Diffusion-style reasoning: simulate diffusion-style reasoning using a transformer model. Repeatedly refine partially corrupted reasoning traces.

## Experimental Variables 
The primary independet variable is: 
- Reasoning method

All other variables will remain constant. 

## Evaluation Metric
We undergo two forms of evalution: qualitative and quantative 
### Quantative: 
Our quantative metric will be accuracy which is defined as "accuracy = correct answers / total questions."
### Qualatative:
We analyze selected examples to understand how reasoning strategies differ. This might included cases where one reasoning method fails and the other succeeds or where models might introduce or correct errors during refinement.

Our evaluation metric will be primarily accuracy, defined as "accuracy = correct answers / total questions." 

## Prompt templates:
These prompt templates will be used exactly for all 4 reasoning methods. 

### 1. Baseline (1 call)
Prompt: 
> Solve the following problem.
>
> {question}
> 
> Give only the final answer.
> 
> Format:
> Final Answer: <number>

### 2. CoT (1 call):
Prompt:
> Solve the following problem step by step.
>
> {question}
>
> Show your reasoning clearly, then give the final answer.
> 
> Format:
> Reasoning:
> <your steps>
> Final Answer: <number>

### 3. Iterative Refinement (3 calls):
Prompt:

Step 1:
> Solve the following problem step by step.
>
>{question}
>
> Format:
> Reasoning:
> <your steps>
>
> Final Answer: <number>

Step 2:
> You are a careful reviewer.
> Here is a solution to a problem:
>
> {solution_from_step_1}
>
> Identify any errors in the reasoning. 
> If the solution is correct, say "No errors found."
>
> Be precise.

Step 3:
> You are improving a solution based on feedback.
>
> Problem:
>{question}
>
> Original solution:
> {solution_from_step_1}
>
> Critique:
> {critique_from_step_2}
>
> Provide a corrected and improved solution.
>
> Format:
> Reasoning:
> <your steps>
>
> Final Answer: <number>
### 4. Diffusion-inspired Refinement (3 iterations = 4 calls total)
For this prompting technique, we specifically add noise in at the start of steps 2, 3, and 4. For each of these steps respectively, we add the following noise:
  - Step 2: Step deletion - remove one reasoning step
  - Step 3: Numerical corruption - slightly modify a singular number
  - Step 4: Step shuffling - swap the order of two steps

Step 1:
> Solve the following problem step by step.
> 
> {question}
> 
> Format:
> Reasoning:
> <your steps>
> 
> Final Answer: <number>

Step 2-4:
> You are given a partially incorrect or unclear solution.
> 
> {noisy_solution}
> 
> Rewrite the solution completely so that it is correct, clear, and logically consistent.
> 
> Format:
> Reasoning:
> <your steps>
> 
> Final Answer: <number>


## Experimental Procedure:
For each model: 
1. Load the same GSM8K dataset subset of 100 questions.
2. For each question: (using defined prompting templates)
- run baseline prompting
- run Chain-of-Thought prompting
- run iterative refinement
- run diffusion-style reasoning
3. Record the model's final answer.
4. Compare the answer with the ground truth.
5. Store results in a structured dataset.
Our results will be stored in CSV format. 

## Limitations 
Several limitations to be acknowledged include:
- Only a subset of GSM8K will be evaluated 
- Diffusion reasoning is simulated rather than implemented through a true diffusion model. This has the potneital to cause the model to either rewrite the answer from scratch or ignore the input depending on the level of noise.
- Prompt wording may influence model behavior
