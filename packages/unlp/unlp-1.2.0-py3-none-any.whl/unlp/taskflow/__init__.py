#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2021/2/26 12:10 下午
@Author  : hcai
@Email   : hua.cai@unidt.com
"""

import unlp.taskflow.word_embedding
import unlp.taskflow.sentence_embedding
import unlp.taskflow.similarity

def get_word_embedding(model,word,min=1,max=3):
    word_vector = unlp.taskflow.word_embedding.word_vector(model, word, min, max)
    return word_vector

def get_sentence_embedding(model,sentence, add_pos_weight=['n','nr','ng','ns','nt','nz'],stop_words_path=None):
    sentence_vector = unlp.taskflow.sentence_embedding.sentence_vector(model, sentence, add_pos_weight, stop_words_path)
    return sentence_vector

def get_similarity(query_vec, vec_list, metric_type='cos'):
    vector_similarity = unlp.taskflow.similarity.get_similarity(query_vec, vec_list, metric_type)
    return vector_similarity

def get_tfidf_similarity(sentence1, sentence2):
    vector_similarity = unlp.taskflow.similarity.tfidf_similarity(sentence1, sentence2)
    return vector_similarity
