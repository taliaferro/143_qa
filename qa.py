from qa_engine.base import QABase
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import spacy
import sys
import time
from json import dumps
nlp = spacy.load("en_core_web_lg")

questions = 0

stop = set(stopwords.words('english'))


def token_filter(token, use_spacy_stopwords=False):
    keep_token = True
    if token.pos_ == "PROPN":
        keep_token = False
    elif token.text == "-PRON-":
        keep_token = False
    elif token.text.lower(
    ) in stop if not use_spacy_stopwords else token.is_stop:
        keep_token = False
    elif token.is_punct:
        keep_token = False
    return keep_token


def normalize(text, lemmatize=True, expand_synsets=False, loose_filter=False):
    doc = nlp(text)
    out_set = set([])
    if expand_synsets and not lemmatize:
        print("can't expand synsets without lemmatizing", file=sys.stderr)
        exit()

    for token in doc:
        if token_filter(token):
            if expand_synsets:
                pos_dict = {
                    "NOUN": wn.NOUN,
                    "VERB": wn.VERB,
                    "ADV": wn.ADV,
                    "ADJ": wn.ADJ
                }
                if token.pos_ in pos_dict:
                    synset = wn.synsets(token.lemma_, pos=pos_dict[token.pos_])
                else:
                    synset = wn.synsets(token.lemma_)

                if synset != []:
                    for synonym in synset[0].lemma_names():
                        out_set.add(synonym)
                else:
                    out_set.add(token.lemma_)
            elif (lemmatize):
                out_set.add(token.lemma_)
            else:
                out_set.add(token.text)
    return out_set


def get_answer(question, story):
    """
    :param question: dict
    :param story: dict
    :return: answerid, answer


    question is a dictionary with keys:
        question -- The raw text of question.
        storyid --  The story id.
        questionid  --  The id of the question.


    story is a dictionary with keys:
        storytitle -- the title of the story.
        storyid --  the id of the story.
        setence -- the raw text sentence version.
        sentenceid --  the id of the sentence
    """

    q_lemmas = normalize(question["question"], expand_synsets=True)
    answers = {
        sent["sentenceid"]: normalize(sent["sentence"], expand_synsets=True)
        for sent in story
    }

    score_dict = {}
    for ans in answers.keys():
        ans_lemmas = answers[ans]
        score_dict[ans] = len([lem for lem in q_lemmas if lem in ans_lemmas])
        # score_dict[ans] = score_dict[ans] / len(ans_lemmas) if len(
        #     ans_lemmas) > 0 else score_dict[ans]
    sent_id = max(score_dict, key=score_dict.get)

    answer = [sent for sent in story
              if sent["sentenceid"] == sent_id][0]["sentence"]
    # print(len(q_lemmas))
    # print(score_dict[sent_id])
    # sent_id = "foo"
    # answer = "bar"
    global questions
    questions += 1
    sys.stdout.write("\r" + str(questions) + " questions  answered...")
    # print(question["question"], q_lemmas)

    return sent_id, score_dict[sent_id]
    # return "-", score_dict[sent_id]


#############################################################
###     Dont change the code in this section
#############################################################
class QAEngine(QABase):
    @staticmethod
    def answer_question(question, story):
        sent_id, answer = get_answer(question, story)
        return (sent_id, answer)


def run_qa():
    QA = QAEngine()
    QA.run()
    QA.save_answers()
    for i in range(5):
        print("\a", file=sys.stderr)
        time.sleep(0.2)


#############################################################


def main():
    run_qa()


if __name__ == "__main__":
    main()
