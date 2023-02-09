'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2022.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    mult_sum = 0 # sum of the product of u_i and v_i
    u2_sum = 0 # sum of the square of the u terms
    v2_sum = 0 # sum of the square of the v terms
    for term1 in vec1:
        #print(term1)
        if term1 in vec2:
            mult = vec1[term1] * vec2[term1]
            mult_sum += mult
        u2_sum += (vec1[term1]) ** 2
    for term2 in vec2:
        # don't need to add the mult_sum because already done in last loop
        v2_sum += (vec2[term2]) ** 2
    root = math.sqrt(u2_sum*v2_sum)
    if root == 0: return -1 # math error
    return mult_sum / root


def build_semantic_descriptors(sentences):
    master_dict = {} # big dictionary with all the words
    for s in sentences:
        s = list(set(s))
        ''' ^this affects how words that are 2-on-1 are counted. For example, if one word appears twice in the sentence we still increase the counts of all the other words by 1 with this line. Remove this line and those words are increased by 2 instead.'''
        #print(s)
        for word in s:
            #print(word)
            if word not in master_dict:
                master_dict[word] = {} # sub-dictionary for each word
            for otherword in s:
                if word != otherword:
                    if otherword not in master_dict[word]:
                        master_dict[word][otherword] = 1
                    else:
                        master_dict[word][otherword] += 1
    return master_dict


def split_text_to_sentences(text):
    text = text.replace("!", ".").replace("?", ".") # change sentence-ending punctuation to periods
    text = text.replace(",", " ").replace("--", " ").replace("-", " ").replace(":", " ").replace(";", " ") # disregard other punctuation
    text = text.replace("\n", " ") # disregard new lines
    text = text.lower() # disregard capital letters
    sentences = text.split(".") # split everything at the period
    return sentences


def split_sentence_to_words(sentences):
    words = []
    for i in range(len(sentences)):
        #print(sentences[i])
        words.append(sentences[i].split())
    return words


def split_text_to_words(text):
    s = split_text_to_sentences(text)
    w = split_sentence_to_words(s)
    return w


def build_semantic_descriptors_from_files(filenames):
    text = ""
    for cur_file in filenames:
        #print(cur_file)
        openfile = open(cur_file, "r", encoding="latin1")
        text += openfile.read()
        #print(text[0:10])
    words = split_text_to_words(text) # use helper functions to encode the text
    d = build_semantic_descriptors(words) # now in proper format to make the dictionary
    return d


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    best_choice = choices[0]
    best_similarity = -1 # the current best cosine similarity found
    if word not in semantic_descriptors:
        return best_choice # we have no data, have to return the first one
    the_word = semantic_descriptors[word]
    for choice in choices:
        cur_similarity = -1
        if choice in semantic_descriptors:
            the_choice = semantic_descriptors[choice] # grab the similarity for the current word
            cur_similarity = similarity_fn(the_word, the_choice)
            #print("word: ", word, " - choice: ", choice, " - similarity: ", cur_similarity)
            if (cur_similarity > best_similarity):
                best_choice = choice
                best_similarity = cur_similarity
    return best_choice


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    openfile = open(filename, "r", encoding="latin1")
    text = openfile.read()
    tests = text.split("\n")
    #print(tests)
    total_tests_run = 0
    total_tests_correct = 0
    for t in tests:
        test = t.split()
        if len(test) >= 3:
            #print(test)
            word = test[0]
            answer = test[1]
            choices = []
            for i in range(2, len(test)):
                choices.append(test[i])
            our_answer = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
            #print("our answer: ", our_answer, " - correct: ", answer)
            # print(our_answer)
            if (our_answer == answer):
                total_tests_correct += 1
            total_tests_run += 1
    return 100 * total_tests_correct / total_tests_run


if __name__=="__main__":
    # text = ""
    # openfile = open("thetest.txt", "r", encoding="latin1")
    # text1 = openfile.read()
    # openfile = open("thetest.txt", "r", encoding="latin1")
    # text2 = openfile.read()
    # text += text1
    # text += text2
    # print(text)

    sem_descriptors_new = build_semantic_descriptors_from_files(["warandpeace.txt", "swann.txt"])
    res = run_similarity_test("test.txt", sem_descriptors_new, cosine_similarity)
    print(res, "of the guesses were correct")
