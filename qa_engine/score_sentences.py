import pandas as pd
import argparse

question_dict = {}
for line in open("data/hw6-questions.tsv", "r").readlines()[1:]:
    line = line.split("\t")
    question_dict[line[1]] = line[2]

ans_dict = {"-": "-"}
for line in open("data/hw6-stories.tsv", "r").readlines()[1:]:
    line = line.split("\t")
    ans_dict[line[2]] = line[3]


def score_all_answers(gold, pred, incorrect_only=True):
    all_scores = []
    if len(gold) != len(pred):
        print("WARNING: you are missing questions in your response file.")
        exit(1)
    for row in gold.itertuples():
        gold_answer = str(row.answer_sentenceid.strip())
        pred_answer = str(pred.loc[row.Index].answer_sentenceid).strip()
        correct = gold_answer == pred_answer

        if incorrect_only and not correct:
            print()
            print('OHHHH, that\'s too bad!')
            print('To the question, "' + question_dict[row.Index].strip() +
                  '"')
            print(
                'You answered "' +
                ans_dict[str(pred.loc[row.Index].answer_sentenceid).strip()] +
                '"')
            print('but the answer was "' +
                  ans_dict[row.answer_sentenceid if "," not in
                           row.answer_sentenceid else row.
                           answer_sentenceid[:row.answer_sentenceid.
                                             index(",")]].strip() + '"')
            print()

        all_scores.append(int(correct))

    # print("-" * 40)
    return sum(all_scores) / len(gold)


def run_scoring(gold, pred):
    accuracy = score_all_answers(gold, pred)

    print("FINAL RESULTS\n\n")

    print("AVERAGE ACCURACY =     {:.4f}".format(accuracy))
    print(
        "\n*************************************************************************\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assignment 6')
    parser.add_argument('-answer',
                        dest='answer_fname',
                        help='The path to answer key file')
    parser.add_argument('-response',
                        dest='response_fname',
                        help='The path to your response file')
    args = parser.parse_args()

    gold = pd.read_csv(args.answer_fname, index_col="questionid", sep="\t")
    pred = pd.read_csv(args.response_fname, index_col="questionid", sep="\t")
    run_scoring(gold, pred)
