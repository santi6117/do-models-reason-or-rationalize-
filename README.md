# diffusion-reasoning-models
Investigating iterative reasoning with diffusion–transformer hybrid models

# Motivation
Large language models typically generate reasoning sequences autoregressively, committing to each token as it is produced. This sequential generation can lead to exposure bias and error propagation when early reasoning steps are incorrect.

Diffusion-based language models offer an alternative generation paradigm in which sequences are produced through iterative denoising. This process allows intermediate reasoning steps to be revised, potentially improving reasoning robustness and accuracy.

# Research Question

Can diffusion-based language models improve reasoning performance by enabling iterative refinement compared to autoregressive chain-of-thought reasoning?

# Approach

This project compares three reasoning paradigms:

Autoregressive Chain-of-Thought (CoT) - Standard transformer reasoning using step-by-step prompts.

Iterative Prompting - Autoregressive reasoning with additional self-reflection and revision steps.

Diffusion-Based Reasoning - Reasoning generated through a diffusion–transformer hybrid model using iterative denoising.

# Dataset

Experiments will use a subset of the GSM8K dataset, a widely used benchmark for mathematical reasoning in language models.

# Evaluation

Models will be evaluated based on:
- reasoning accuracy on GSM8K questions
- robustness to reasoning errors
- - qualitative analysis of reasoning chains

# Expected Outcomes

This project aims to explore whether iterative refinement mechanisms improve reasoning reliability compared to sequential chain-of-thought reasoning.

# Additional Experiments (time permitting)

Beyond the core comparison between autoregressive and diffusion-based reasoning, this project may explore how different diffusion parameters influence reasoning performance. These experiments aim to better understand how iterative refinement dynamics influence reasoning behavior.

Potential experiments include:
- Varying the number of diffusion denoising steps
- Exploring different noise schedules
- Testing partial refinement of reasoning sequences
- Evaluating whether additional refinement iterations improve reasoning accuracy
