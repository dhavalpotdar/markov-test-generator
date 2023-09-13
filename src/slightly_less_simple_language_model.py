"""Demonstrate the "simplest" language model."""
import math
from typing import Optional

# generate English document
text = "Four score and seven years ago, our fathers brought forth, upon this continent, a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal."
text = (text + " ") * 100  # make the document very long

# tokenize - split the document into a list of little strings
tokens = [char for char in text]

# encode as {0, 1}
encodings = [0 if token == " " else 1 for token in tokens]


# define model
class SimplestModel:
    """The simplest language model."""

    def __init__(self) -> None:
        """Initialize."""
        self.p_space: Optional[float] = None

    def train(self, encodings: list[int]) -> "SimplestModel":
        """Train the model on data."""
        self.p_space = encodings.count(0) / len(encodings)
        return self

    def apply(self, encodings: list[int]) -> float:
        """Compute the probability of a document."""
        if self.p_space is None:
            raise ValueError("This model is untrained")
        return sum(
            math.log(self.p_space) if encoding == 0 else math.log(1 - self.p_space)
            for encoding in encodings
        )


# train model
model = SimplestModel()
model.train(encodings)

# compute probability
log_p = model.apply(encodings)

# print
print(f"learned p_space value: {model.p_space}")
print(f"log probability of document: {log_p}")
print(f"probability of document: {math.exp(log_p)} (this is due to underflow)")