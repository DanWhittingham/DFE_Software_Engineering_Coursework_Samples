#==== Imports
import spacy

#==== load language module
nlp = spacy.load('en_core_web_md')

#==== single-world similarities
word1 = nlp("cat")
word2 = nlp("monkey")
word3 = nlp("banana")
print(word1.similarity(word2))
print(word3.similarity(word2))
print(word3.similarity(word1))

##=== additional example
print("Compare 'tabby'")
word4 = nlp("tabby")
print(word1.similarity(word4))
print(word2.similarity(word4))
print(word3.similarity(word4))


#==== loop over set of tokens
tokens = nlp('cat apple monkey banana')
for token1 in tokens:
    for token2 in tokens:
        print(token1.text, token2.text, token1.similarity(token2))


#==== Sentence comparisons
sentence_to_compare = "Why is my cat on the car"
sentences = ["where did my dog go",
"Hello, there is my car",
"I\'ve lost my car in my car",
"I\'d like my boat back",
"I will name my dog Diana"]
model_sentence = nlp(sentence_to_compare)
for sentence in sentences:
    similarity = nlp(sentence).similarity(model_sentence)
    print(sentence + " - ", similarity)


#==== Notes for task
'''
Cat & monkey have stronger similarity as both are animals.
Banana rates more closely to monkey than to cat, which suggests
the model is aware of the association between monkeys and bananas.

Adding in the word "tabby", this associates very strongly with cat.
The association with monkey is weak, and even weaker with banana.
This is as one would expect.

Running with 'en_core_web_sm' (instead of _md) yields less meaningful judgements.
For example, cat associates more strongly with apply than monkey does with banana!
The smaller module does produce warnings that judgements may not be as useful
and recommends using one of the larger modules for better judgements.
'''
