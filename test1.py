import text_paras_advanced_rea
from pipelines import pipeline

video_name, quiz_concepts, concept_list = text_paras_advanced_rea.data_from_paras()
nlp = pipeline("multitask-qa-qg", model="valhalla/t5-base-qa-qg-hl")


all_concept_question_list = []
all_concept_answer_list = []
for c in range(len(quiz_concepts)):
    concept_question_list = []
    concept_answer_list = []
    for p in range(len(quiz_concepts[c])):
        data_list = nlp(quiz_concepts[c][p])
        if (len(data_list) > 0):
            question_list = []
            answer_list = []
            for i in range(len(data_list)):
                question_list.append(data_list[i]["question"])
                answer_list.append(data_list[i]["answer"])
            concept_question_list.append(question_list)
            concept_answer_list.append(answer_list)
    all_concept_question_list.append(concept_question_list) 
    all_concept_answer_list.append(concept_answer_list)
def data_going_to_db():
    return video_name, concept_list, quiz_concepts, all_concept_question_list, all_concept_answer_list