# ESC180
Projects from ESC180

# Gomoku.py
Implementation of an AI engine for the game Gomoku, played on a 8 × 8 board. In Gomoku, there are two players. One player plays with black stones and the other player plays with white stones. A player moves by placing a stone on an empty square on the board. The player who plays with black stones always moves first. After the first move, the players alternate. A player wins if she has placed five of her stones in a sequence, either horizontally, or vertically, or diagonally.

# Synonym.py
One type of question encountered in the Test of English as a Foreign Language (TOEFL) is the “Synonym Question”, where students are asked to pick a synonym of a word out of a list of alternatives. For example:

1. vexed (Answer: (a) annoyed)
(a) annoyed

(b) amused

(c) frightened

(d) excited

This assignment is an intelligent system that can learn to answer questions like this one. In order to do that, the system will approximate the semantic similarity of any pair of words. The semantic similarity between two words is the measure of the closeness of their meanings. For example, the semantic similarity between “car” and “vehicle” is high, while that between “car” and “flower” is low. In order to answer the TOEFL question, you will compute the semantic similarity between the word you are given and all the possible answers, and pick the answer with the highest semantic similarity to the given word. More precisely, given a word w and a list of potential synonyms s1, s2, s3, s4, we compute the similarities of (w, s1), (w, s2), (w, s3), (w, s4) and choose the word whose similarity to w is the highest. We will measure the semantic similarity of pairs of words by first computing a semantic descriptor vector of each of the words, and then taking the similarity measure to be the cosine similarity between the two vectors. Given a text with n words denoted by (w1, w2, ..., wn) and a word w, let descw be the semantic descriptor vector of w computed using the text. descw is an n-dimensional vector. The i-th coordinate of descw is the number of sentences in which both w and wi occur.
