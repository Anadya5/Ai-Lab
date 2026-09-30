"""
Main Runner & Validation Script
Trains 1st and 2nd Order Models, validates CPTs, tests normalization invariants,
generates sample text, and compares model performance metrics.
"""

import random
from first_order_lm import FirstOrderLM
from second_order_lm import SecondOrderLM

# Dataset provided in Part III of BN_lab.pdf
DATASET = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug"
]


def print_section_header(title):
    print("\n" + "=" * 65)
    print(f" {title}")
    print("=" * 65)


def run_experiments():
    random.seed(42)  # For reproducible sampling

    # -------------------------------------------------------------
    # 1. Train First-Order Model
    # -------------------------------------------------------------
    print_section_header("PART 1: FIRST-ORDER AUTOREGRESSIVE MODEL")
    lm1 = FirstOrderLM()
    lm1.train(DATASET)

    # Display selected CPTs (Question 3)
    target_words = ['the', 'cat', 'dog', 'sat', 'ran']
    print("\n[Conditional Probability Distributions P(X_t | X_{t-1})]:")
    for word in target_words:
        cpt = lm1.get_cpt(word)
        cpt_str = ", ".join([f"{w}: {p:.2f}" for w, p in cpt.items()])
        print(f"  P(next | '{word}') = {{ {cpt_str} }}")

    # Probability Normalization Test (Part VII)
    print("\n[Probability Normalization Test (sum_v P(v|w) == 1.0)]:")
    norm_results_1 = lm1.test_normalization()
    all_passed_1 = all(abs(total - 1.0) < 1e-6 for total in norm_results_1.values())
    print(f"  All context distributions sum to 1.0: {all_passed_1}")

    # Text Generation: Greedy vs Sampling (Part X)
    print("\n[First-Order Text Generation - Mode A: Greedy]:")
    for i in range(3):
        print(f"  Sentence {i+1}: {lm1.generate_sentence(mode='greedy')}")

    print("\n[First-Order Text Generation - Mode B: Sampling (5 Examples)]:")
    for i in range(5):
        print(f"  Sentence {i+1}: {lm1.generate_sentence(mode='sample')}")

    # -------------------------------------------------------------
    # 2. Train Second-Order Model
    # -------------------------------------------------------------
    print_section_header("PART 2: SECOND-ORDER AUTOREGRESSIVE MODEL")
    lm2 = SecondOrderLM()
    lm2.train(DATASET)

    # Display selected CPTs
    sample_contexts = [
        ("<START>", "<START>"),
        ("the", "cat"),
        ("sat", "on"),
        ("ran", "to")
    ]
    print("\n[Conditional Probability Distributions P(X_t | X_{t-2}, X_{t-1})]:")
    for ctx in sample_contexts:
        cpt = lm2.get_cpt(ctx)
        cpt_str = ", ".join([f"{w}: {p:.2f}" for w, p in cpt.items()])
        print(f"  P(next | {ctx}) = {{ {cpt_str} }}")

    # Probability Normalization Test
    norm_results_2 = lm2.test_normalization()
    all_passed_2 = all(abs(total - 1.0) < 1e-6 for total in norm_results_2.values())
    print(f"\n[Probability Normalization Test]:")
    print(f"  All context distributions sum to 1.0: {all_passed_2}")

    # Text Generation: Greedy vs Sampling
    print("\n[Second-Order Text Generation - Mode A: Greedy]:")
    for i in range(3):
        print(f"  Sentence {i+1}: {lm2.generate_sentence(mode='greedy')}")

    print("\n[Second-Order Text Generation - Mode B: Sampling (5 Examples)]:")
    for i in range(5):
        print(f"  Sentence {i+1}: {lm2.generate_sentence(mode='sample')}")

    # -------------------------------------------------------------
    # 3. Quantitative Model Comparison (Part XIII)
    # -------------------------------------------------------------
    print_section_header("PART 3: MODEL COMPARISON SUMMARY")
    
    # Generate 20 sampled sentences per model
    gen_sentences_1 = [lm1.generate_sentence(mode='sample') for _ in range(20)]
    gen_sentences_2 = [lm2.generate_sentence(mode='sample') for _ in range(20)]
    
    distinct_params_1 = sum(len(cpt) for cpt in lm1.probs.values())
    distinct_params_2 = sum(len(cpt) for cpt in lm2.probs.values())

    print(f"1. Parameters (Non-zero probabilities stored):")
    print(f"   - First-Order Model : {distinct_params_1} transitions")
    print(f"   - Second-Order Model: {distinct_params_2} transitions")

    print(f"\n2. Unique Contexts Tracked:")
    print(f"   - First-Order Model : {len(lm1.probs)} contexts")
    print(f"   - Second-Order Model: {len(lm2.probs)} contexts")

    print(f"\n3. Diversity of Generated Output (Unique sentences out of 20 samples):")
    print(f"   - First-Order Model : {len(set(gen_sentences_1))} unique sentences")
    print(f"   - Second-Order Model: {len(set(gen_sentences_2))} unique sentences")


if __name__ == "__main__":
    run_experiments()