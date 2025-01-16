**Sequence of Commands to run:**

**Questions Generation:**

!pip install -U transformers==3.0.0

!python -m nltk.downloader punkt

python Text_paras3.py

python Mcqs_model.py

python Concept_wise_questions.py

python Concept_wise_db_connection.py

**Multiple-choice Answers Generation:**

!pip install --quiet transformers==4.3.0

!pip install pytorch-lightning

!pip install --quiet tokenizers==0.10.3

python Concept_wise_multiple_answers1.py
