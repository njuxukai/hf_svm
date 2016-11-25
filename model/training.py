# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.svm import SVC, LinearSVC
from sklearn import preprocessing
import random
from util.af_logger import *

def select_economic_feature_set(feature_df):
    """
    TODO
    根据文献方法，实现寻找最小经济特征集算法
    """
    return []
 
def train_multi_class_svm(feature_df, input_features):
    """
    朴素的svm算法 简单验证模型的有效性
    feature_df DataFrame 最后一列是class label (int)
    """
    train_set_size = 500
    test_set_size = 100
    pool_size = len(feature_df)
    labels = np.unique(feature_df['label'])
    label_ix_dict = {}
    for label in labels:
        label_ix_dict[label] = list(feature_df['label'][feature_df['label'] == label].index)

    train_set_index_list = []
    test_set_index_list = []
    for label in labels:
        label_density = len(label_ix_dict[label]) / pool_size
        train_set_target_size = int(train_set_size * label_density)
        test_set_target_size = int(test_set_size * label_density)
        #从label类中先取train_set_target_size作为训练集的一部分
        #再取test_set_target_size作为测试集
        train_set = random.sample(label_ix_dict[label], train_set_target_size)
        candidate_set = [i for i in label_ix_dict[label] if i not in train_set]
        test_set = random.sample(candidate_set, test_set_target_size)
        train_set_index_list.extend(train_set)
        test_set_index_list.extend(test_set)

    #train & test
    train_df = feature_df.ix[train_set_index_list]
    test_df = feature_df.ix[test_set_index_list]
    samples_features = np.array(train_df[input_features])
    class_labels = np.array(train_df.label)
    min_max_scaler = preprocessing.MinMaxScaler()
    sample_features_minmax = min_max_scaler.fit_transform(samples_features)
    svm_model = LinearSVC(C=2.0)
    svm_model.fit(sample_features_minmax, class_labels)
    test_features_minmax = min_max_scaler.transform(np.array(test_df[input_features]))
    result = svm_model.predict(test_features_minmax)
    test_class_labels = np.array(test_df.label)
    diff = result - test_class_labels
    #correct_count  = len(diff[diff == 0])
    correct_count = 0
    for d in diff:
        if abs(d) < 1:
            correct_count += 1
    logger.info("correct ratio={0}/{1}".format(correct_count, len(diff)))



