# Research Question
Does iterative reasoning improve accuracy compared to
Chain-of-Thought reasoning in large language models?

# Hypothesis 
Iterative reasoning methods will outperform Chain-of-Thought
because they allow correction of earlier reasoning errors.

# Experimental setup
The experiment compares multiple reasoning startegies to the same underlying models, isolating the effect of the reasoning strategy on performance.

To avoid model-specific results, the experiment will test multiple transformer-based language models:
- GPT-4o-mini
- Llama-3-8b-Instruct
- Mistral7B-Instruct

As a dataset, we will use a subset of 100 questions from GSM8K. 
We will evaulte on exact answer accuracy.

Our specific reasoning strategies will include:
- Baseline: direct answer without explicit reasoning instructions.
  - eg. "Solve the following problem: {question}" 
- Chain-of-Thought (CoT): single reasoning trajectory prompt. This represents sequential reasoning. 
  - eg. "Solve the following problem step by step: {question}"
- Iterative reasoning: intial reasoning trace then iteratively improving on it. 
  - eg. Initial reasoning -> critique reasoning -> revise reasoning - > final answer
- Diffusion-style reasoning: simulate diffusion-style reasoning using a transformer model. Repeatedly refine partially corrupted reasoning traces.
  - Process:
      - Initial reasoning
      - Inject noise into reasoning
      - Model denoises / corrects reasoning
      - Repeat N iterations 

Our variables will include:
- Number of refinement steps
- Noise intensity (diffusion method only)

Our evaluation metric will be primarily accuracy, defined as "accuracy = correct answers / total questions." 

# Experimental Procedure:
For each model: 
1. Load the GSM8K dataset subset.
2. For each question:
- run baseline prompting
- run Chain-of-Thought prompting
- run iterative refinement
- run diffusion-style reasoning
3. Record the model's final answer.
4. Compare the answer with the ground truth.
5. Store results in a structured dataset.

# Limitations 
Several limitations to be acknowledged include:
- Only a subset of GSM8K will be evaluated 
- Diffusion reasoning is simulated rather than implemented through a true diffusion model 
- Prompt wording may influence model behavior
