import mcqs_model
import mysql.connector
best_model = mcqs_model.best_model
connection = mysql.connector.connect(host='localhost',
                                         database='question_generation',
                                         user='root',
                                         password='')

mycursor = connection.cursor()

mycursor.execute("SELECT Video_Name, Concept, Text_Data, Question, Answer FROM concept_wise_rea_advanced_part1_questions1")
myresult = mycursor.fetchall()

empty_val = ""
for each in myresult:
    var_video = each[0]
    var_concept = each[1]
    var_context = each[2]
    var_question = each[3]
    var_answer = each[4]
    all_options = []
    for beam in mcqs_model.generate(best_model, var_answer, var_context, 5).split('</s>'):
        print(beam)
        req_word= beam.replace("<pad> ", "")
        req_word1= req_word.replace("<sep>", ",")
        req_word2 = req_word1.split(", ")
        for j in range(len(req_word2)):
            if "<pad>" in req_word2[j]:
                req_word2[j]= req_word2[j].replace("<pad>", "")
            all_options.append(req_word2[j])
    given_options = set(all_options)
    given_options = list(given_options)

    if  len(given_options) == 3:
        abc = ""
        sql = "INSERT INTO concept_wise_rea_advanced_part1_options1 (Video_Name, Concept, Text_Data, Question, Answer, Option1, Option2, Option3, Option4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (var_video, var_concept, var_context, var_question, var_answer, given_options[0], given_options[1], given_options[2], abc)
        mycursor.execute(sql, val)
    else:
        sql = "INSERT INTO concept_wise_rea_advanced_part1_options1 (Video_Name, Concept, Text_Data, Question, Answer, Option1, Option2, Option3, Option4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (var_video, var_concept, var_context, var_question, var_answer, given_options[0], given_options[1], given_options[2], given_options[3])
        mycursor.execute(sql, val)

connection.commit()
print(mycursor.rowcount, "was inserted.")

