"""
First-Order Autoregressive Language Model
Estimates P(X_t | X_{t-1}) using transition counts (Bigrams) from training data.
"""

import random
from collections import defaultdict, Counter


class FirstOrderLM:
    def __init__(self):
        # Stores raw transition counts: C(w_{t-1}, w_t)
        self.counts = defaultdict(Counter)
        # Stores CPT: P(w_t | w_{t-1})
        self.probs = {}
        self.vocab = set()

    def train(self, sentences):
        """
        Tokenizes input sentences, adds boundary tokens, counts transitions,
        and builds the Conditional Probability Table (CPT).
        """
        for sentence in sentences:
            tokens = ["<START>"] + sentence.lower().split() + ["<END>"]
            self.vocab.update(tokens)
            
            # Count consecutive bigram transitions
            for w1, w2 in zip(tokens[:-1], tokens[1:]):
                self.counts[w1][w2] += 1

        # Build Conditional Probability Distribution: P(X_t = w_j | X_{t-1} = w_i)
        for w1, next_counts in self.counts.items():
            total_transitions = sum(next_counts.values())
            self.probs[w1] = {
                w2: count / total_transitions 
                for w2, count in next_counts.items()
            }

    def get_cpt(self, current_word):
        """Returns the CPT P(X_t | current_word)."""
        return self.probs.get(current_word.lower(), {})

    def predict_next_greedy(self, current_word):
        """Predicts the most probable next token: argmax_w P(w | current_word)."""
        cpt = self.get_cpt(current_word)
        if not cpt:
            return None  # Unobserved context / zero transition
        return max(cpt, key=cpt.get)

    def predict_next_sample(self, current_word):
        """Samples the next token according to P(w | current_word)."""
        cpt = self.get_cpt(current_word)
        if not cpt:
            return None  # Unobserved context
        tokens, probabilities = zip(*cpt.items())
        return random.choices(tokens, weights=probabilities, k=1)[0]

    def test_normalization(self):
        """Verifies the probabilistic invariant: sum_v P(v | w) == 1.0 for all w."""
        totals = {}
        for word, cpt in self.probs.items():
            totals[word] = sum(cpt.values())
        return totals

    def generate_sentence(self, mode="sample", max_length=25):
        """Generates a sentence token by token starting from <START>."""
        current = "<START>"
        sentence = []
        
        for _ in range(max_length):
            if mode == "greedy":
                next_word = self.predict_next_greedy(current)
            elif mode == "sample":
                next_word = self.predict_next_sample(current)
            else:
                raise ValueError("Mode must be either 'greedy' or 'sample'")

            if next_word is None or next_word == "<END>":
                break
                
            sentence.append(next_word)
            current = next_word

        return " ".join(sentence)