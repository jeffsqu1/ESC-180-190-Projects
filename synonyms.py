'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
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
    same_word = 0
    mag1 = 0
    mag2 = 0
    for i in vec1:
        if i in vec2:
            same_word += vec1[i] * vec2[i]
        mag1 += vec1[i]**2
    for i in vec2:
        mag2 += vec2[i]**2
    if same_word == 0:
        return -1
    similarity = same_word/math.sqrt(mag1*mag2)
    return similarity



def build_semantic_descriptors(sentences):
    d = {}
    for sent in sentences: #each sentence
        for w in sent: #each word
            if w not in d: #for new word
                d[w] = {}#new entry for word, a dictionary for other words in sentence
            for i in sent: #check words in sentence
                if i != w:
                    if i not in d[w]:
                        d[w][i] = 1 #new entry
                    else:
                        d[w][i] += 1 #add to existing entry
    return d


def build_semantic_descriptors_from_files(filenames):
    #file = ""
    sentences = []
    for i in range(len(filenames)):
        file = open(filenames[i], "r", encoding="latin1").read() #if /n/ becomes a problem, replace latin1 with utf-8

        f1 = file.replace("!",".") #All punctuation for sentences becomes uniform "."
        f2 = f1.replace("?",".")

        f3 = f2.replace(","," ") #All word separators replaced by space
        f4 = f3.replace("--"," ") #first double, then single dash
        f5 = f4.replace("-"," ")
        f6 = f5.replace(":"," ")
        f7 = f6.replace(";"," ")

        
        for i in f7.split("."): #sentence1, sentence2
            phrase = []
            for word in i.split():
                phrase.append(word)
            #phrase = [i] #[phrase1], [phrase2]
            sentences.append(phrase) #each sentence, list of sentence
    
    return build_semantic_descriptors(sentences)



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    #semantic_descriptors is dictionary for build semantic descriptors
    #similarity_fn = cosine_similarity
    most = -1 #highest similarity
    best = "" #closest word
    for i in range(len(choices)-1, 0, -1): #reverse indices
        cosi = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]])
        if cosi >= most: #vector(word) and vector(choice) cosine
            most = cosi
            best = choices[i]
    return best
    



def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    # file = open(filename, "r", encoding="latin1").read() #one string
    case = open(filename, "r", encoding="latin1").readlines()
    correct = 0

    #case.append(file.readlines())
    for i in range(len(case)):
        case[i] = case[i].strip().split()
    # for i in file.split("\n"): #each sentence
    #     case.append(i.split())
    
    for i in range(len(case)): #each line
        word = case[i][0]
        answer = case[i][1]
        compare = case[i][2:]
        
        if most_similar_word(word, compare, semantic_descriptors, similarity_fn) == answer:
            correct += 1
    return correct*100/len(case)

    # for i in range(len(case)):
    #     for j in range(case[i].split()):
    #         if j == 0:
    #             word = j
    #         elif j == 1:
    #             answer = j
    #         else:



# if __name__ == "__main__":
# # # #     # text = [["i", "am", "a", "sick", "man"],
# # # #     # ["i", "am", "a", "spiteful", "man"],
# # # #     # ["i", "am", "an", "unattractive", "man"],
# # # #     # ["i", "believe", "my", "liver", "is", "diseased"],
# # # #     # ["however", "i", "know", "nothing", "at", "all", "about", "my",
# # # #     # "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
# #     #print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))
# #     ##print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"e": 4, "f": 5, "d": 6}))


#      filenames = ["war_and_peace.txt", "swann.txt"]
# # # #     #print(build_semantic_descriptors(text))
# # # #     print(build_semantic_descriptors_from_files(filenames))
# # #     print(most_similar_word("woman", ["abandon", "myself", "people", "happen"],build_semantic_descriptors_from_files(filenames),cosine_similarity))
#      sem_descriptors = build_semantic_descriptors_from_files(filenames)
#      print(run_similarity_test("test2.txt", sem_descriptors, cosine_similarity))