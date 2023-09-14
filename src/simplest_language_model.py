"""Demonstrate the "simplest" language model."""
import math

# generate English document
text = "Four score and seven years ago, our fathers brought forth, upon this continent, a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal."

# tokenize - split the document into a list of little strings
tokens = [char for char in text]

# encode as {0, 1}
encodings = [0 if token == " " else 1 for token in tokens]

# define model - it's a simple model
p_space = 0.5

# compute probability
p = math.prod(p_space if encoding == 0 else (1 - p_space) for encoding in encodings)

# print
print(p)

"""
## NOTES

* What happens as the text gets very long?
* Spoiler alert: text gets very long. How can we avoid underflow?
"""
