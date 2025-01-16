import re
from sunau import Au_write
from typing import List, Dict
import tqdm.notebook as tq
from tqdm.notebook import tqdm
import json
import pandas as pd
import numpy as np

import torch
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from transformers import (
    AdamW,
    T5ForConditionalGeneration,
    T5TokenizerFast as T5Tokenizer
    )
SEP_TOKEN = '<sep>'
MODEL_NAME = 't5-small'
SOURCE_MAX_TOKEN_LEN = 512
TARGET_MAX_TOKEN_LEN = 64
N_EPOCHS = 20
BATCH_SIZE = 24
LEARNING_RATE = 0.0001
MODEL_SAVE_NAME = '100200'

model_name = 't5-small'
tokenizer = T5Tokenizer.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
tokenizer.add_tokens(SEP_TOKEN)
TOKENIZER_LEN = len(tokenizer)

class QGModel(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME, return_dict=True)
        self.model.resize_token_embeddings(TOKENIZER_LEN) #resizing after adding new tokens to the tokenizer

    def forward(self, input_ids, attention_mask, labels=None):
        output = self.model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        return output.loss, output.logits

    def training_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['labels']
        loss, output = self(input_ids, attention_mask, labels)
        self.log('train_loss', loss, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['labels']
        loss, output = self(input_ids, attention_mask, labels)
        self.log('val_loss', loss, prog_bar=True, logger=True)
        return loss

    def test_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['labels']
        loss, output = self(input_ids, attention_mask, labels)
        self.log('test_loss', loss, prog_bar=True, logger=True)
        return loss
  
    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=LEARNING_RATE)


checkpoint_path = 'race-distractors.ckpt'
best_model = QGModel.load_from_checkpoint(checkpoint_path)
best_model.freeze()
best_model.eval()


def generate(qgmodel: QGModel, answer: str, context: str, generate_count: int) -> str:
    source_encoding = tokenizer(
        '{} {} {}'.format(answer, SEP_TOKEN, context),
        max_length=SOURCE_MAX_TOKEN_LEN,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        add_special_tokens=True,
        return_tensors='pt'
    )

    generated_ids = qgmodel.model.generate(
        input_ids=source_encoding['input_ids'],
        attention_mask=source_encoding['attention_mask'],
        num_beams=generate_count,
        num_return_sequences=generate_count,
        max_length=TARGET_MAX_TOKEN_LEN,
        repetition_penalty=2.5,
        length_penalty=1.0,
        early_stopping=True,
        use_cache=True
    )

    preds = {
        tokenizer.decode(generated_id, skip_special_tokens=False, clean_up_tokenization_spaces=True)
        for generated_id in generated_ids
    }

    return ''.join(preds)


print("hi ash")

var_context = "Goal is a desired state something that the organization only partially can influence. Means is a course of action, an instrument or method something that the organization essentially can control."
var_correct = "Means"
var_question = "What is a course of action?"
all_options = []
for beam in generate(best_model, var_correct, var_context, 4).split('</s>'):
    print(beam)
    if "<pad> " in beam:
        req_word= beam.replace("<pad> ", "")
        req_word = req_word.replace("<sep>", ",")
        req_word = req_word.split(", ")
        for j in range(len(req_word)):
            print(req_word[j])
            if "<pad>" in req_word[j]:
                req_word[j]= req_word[j].replace("<pad>", "")
            all_options.append(req_word[j])
given_options = set(all_options)
print(given_options)


