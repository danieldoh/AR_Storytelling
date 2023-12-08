import spacy

nlp = spacy.load("en_core_web_sm")

def split_sentence(sentence):
    doc = nlp(sentence)

    # Initialize variables for subject and background
    subject = None
    background = None

    subject_span = []
    background_span = []

    # Find the main verb (main action) in the sentence
    main_action = None
    for token in doc:
        if token.pos_ == "VERB":
            main_action = token
            break

    # Find the subjects and objects of the main verb
    if main_action:
        for child in main_action.children:
            if child.dep_ == "nsubj" and child.ent_type_ == 0:
                subject = child.text
            elif child.dep_ == "prep" and child.ent_type_ == "LOC":
                background = child.text

    # Handle multi-word subjects and objects
    if subject:
        subject_span = [subject]
        for token in main_action.lefts:
            if token.dep_ == "compound":
                subject_span.insert(0, token.text)

    # Handle multi-word objects (background in this case)
    if background:
        background_span = [background]
        for token in main_action.rights:
            if token.dep_ == "pobj" and token.ent_type_ == "LOC":
                background_span.append(token.text)

    return subject_span, background_span, main_action.text

# Test sentences
sentence1 = "Obama punches in a manner consistent with martial arts on the street."
sentence2 = "Astronaut is jumping rope on the moon."

# Split the sentences
subject1, background1, action1 = split_sentence(sentence1)
subject2, background2, action2 = split_sentence(sentence2)

# Print the results
print("Example 1:")
print("1. " + ', '.join(subject1) + (", " + ' '.join(background1) if background1 else ""))
print("2. " + action1)

print("\nExample 2:")
print("1. " + ', '.join(subject2) + (", " + ' '.join(background2) if background2 else ""))
print("2. " + action2)

