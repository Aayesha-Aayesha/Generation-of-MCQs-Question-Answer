import mysql.connector
import test1
connection = mysql.connector.connect(host='localhost',
                                         database='question_generation',
                                         user='root',
                                         password='')

mycursor = connection.cursor()
video_name, concept_list, text_list, question_list, answer_list = test1.data_going_to_db()

print(concept_list[0])
print(text_list[0][0])
print(question_list[0][0][0])
print(answer_list[0][0][0])

for c in range(len(text_list)):
    for i in range(len(text_list[c])):
        for j in range(len(question_list[c][i])):
            sql = "INSERT INTO concept_wise_rea_advanced_part1_questions1 (Video_Name, Concept, Text_ID, Text_Data, Question, Answer) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (video_name, concept_list[c], i, text_list[c][i], question_list[c][i][j], answer_list[c][i][j])
            mycursor.execute(sql, val)


connection.commit()
print(mycursor.rowcount, "was inserted.")