
import pandas as pd
from nltk.parse import DependencyGraph
from nltk.tree import Tree
from collections import defaultdict

# Questionid may also be referred to as qid in variable names
# Storyid may also be referred to as sid in variable names

DATA_DIR = "data/"
QUESTION_FILE = "hw6-questions.tsv"
ANSWER_FILE = "hw6-answers.tsv"
STORIES_FILE = "hw6-stories.tsv"

RESPONSE_FILE = "hw6-responses.tsv"

import math

from collections import defaultdict

## TO BE USED IN HW 7 & 8
#def prepare_deps(raw_deps):
#
#    if isinstance(raw_deps, float) and math.isnan(raw_deps):
#        return []
#    return [DependencyGraph(dep, top_relation_label="root") for dep in raw_deps.split("\n\n")
#            if len(dep) > 2]


## TO BE USED IN HW 7 & 8
#def prepare_pars(raw_pars):
#    if isinstance(raw_pars, float) and math.isnan(raw_pars):
#        return []
#
#    return [Tree.fromstring(line.strip().rstrip(" \n\t"))
#            for line in raw_pars.split("\n") if len(line) > 2]


def prepare_story_data(df):
    stories = defaultdict(list)
    for row in df.itertuples():
        this_story = {
            "storytitle": row.storytitle,
            "sentence": row.sentence,
            "sentenceid": row.sentenceid,
            "storyid": row.storyid,
        }
        stories[row.storyid] += [this_story]
    return stories


def prepare_questions(df):
    questions = {}
    for row in df.itertuples():
        this_qstn = {
            "questionid": row.questionid,
            "storyid": row.storyid,
            "question": row.question
        }
        questions[row.questionid] = this_qstn
    return questions


class QABase(object):

    def __init__(self):

        self._stories = prepare_story_data(pd.read_csv(DATA_DIR + STORIES_FILE, sep="\t"))
        self._questions = prepare_questions(pd.read_csv(DATA_DIR + QUESTION_FILE, sep="\t"))
        self._answers = {q["questionid"]: "" for q in self._questions.values()}


    @staticmethod
    def answer_question(question, story):
        # input: question and story
        # output: sentenceid and answer text
        # HW6 only: answer text can be an empty string ""
        raise NotImplemented


    def get_question(self, qid):
        return self._questions.get(qid)


    def get_story(self, sid):
        return self._stories.get(sid)


    def run(self):
        for qid, q in self._questions.items():
            sent_id, answer = self.answer_question(q, self._stories.get(q["storyid"]))
            self._answers[qid] = {"storyid": q["storyid"], "questionid": qid, \
                                    "answer_sentenceid": sent_id,"answer": answer}


    def save_answers(self, fname=RESPONSE_FILE):
        df = pd.DataFrame([a for a in self._answers.values()])
        df.to_csv(fname, sep="\t", index=False)



