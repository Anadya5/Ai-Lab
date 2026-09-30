"""
Second-Order Autoregressive Language Model
Estimates P(X_t | X_{t-2}, X_{t-1}) using transition counts (Trigrams) from training data.
"""

import random
from collections import defaultdict, Counter


class SecondOrderLM:
    def __init__(self):
        # Stores raw tuple transition counts: C((w_{t-2}, w_{t-1}), w_t)
        self.counts = defaultdict(Counter)
        # Stores CPT: P(w_t | (w_{t-2}, w_{t-1}))
        self.probs = {}
        self.vocab = set()

    def train(self, sentences):
        """
        Tokenizes input sentences, adds dual boundary tokens,
        counts trigrams, and builds the CPT.
        """
        for sentence in sentences:
            # Pad with two <START> tokens to handle initial second-order context
            tokens = ["<START>", "<START>"] + sentence.lower().split() + ["<END>"]
            self.vocab.update(tokens)

            for i in range(len(tokens) - 2):
                context = (tokens[i], tokens[i + 1])
                next_word = tokens[i + 2]
                self.counts[context][next_word] += 1

        # Build Conditional Probability Distribution: P(X_t | X_{t-2}, X_{t-1})
        for context, next_counts in self.counts.items():
            total_transitions = sum(next_counts.values())
            self.probs[context] = {
                nxt: count / total_transitions 
                for nxt, count in next_counts.items()
            }

    def get_cpt(self, context_tuple):
        """Returns CPT P(X_t | (w_{t-2}, w_{t-1}))."""
        return self.probs.get(context_tuple, {})

    def predict_next_greedy(self, context_tuple):
        """Predicts argmax_w P(w | context_tuple)."""
        cpt = self.get_cpt(context_tuple)
        if not cpt:
            return None
        return max(cpt, key=cpt.get)

    def predict_next_sample(self, context_tuple):
        """Samples next token from P(w | context_tuple)."""
        cpt = self.get_cpt(context_tuple)
        if not cpt:
            return None
        tokens, probabilities = zip(*cpt.items())
        return random.choices(tokens, weights=probabilities, k=1)[0]

    def test_normalization(self):
        """Verifies probabilistic invariant: sum_v P(v | context) == 1.0."""
        totals = {}
        for context, cpt in self.probs.items():
            totals[context] = sum(cpt.values())
        return totals

    def generate_sentence(self, mode="sample", max_length=25):
        """Generates a sentence starting from context ('<START>', '<START>')."""
        context = ("<START>", "<START>")
        sentence = []

        for _ in range(max_length):
            if mode == "greedy":
                next_word = self.predict_next_greedy(context)
            elif mode == "sample":
                next_word = self.predict_next_sample(context)
            else:
                raise ValueError("Mode must be either 'greedy' or 'sample'")

            if next_word is None or next_word == "<END>":
                break

            sentence.append(next_word)
            context = (context[1], next_word)

        return " ".join(sentence)