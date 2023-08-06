# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Utility functions to load the final model and vectorizer during inferencing"""

import logging
import numpy as np
import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from typing import Optional, Union

from azureml.automl.dnn.nlp.common.constants import OutputLiterals
from azureml.automl.dnn.nlp.classification.multilabel.model_wrapper import ModelWrapper
from azureml.core.run import Run


_logger = logging.getLogger(__name__)


def load_model_wrapper(run_object: Run, artifacts_dir: Optional[str] = None) -> ModelWrapper:
    """Function to load model (in form of model wrapper) from the training run

    :param run_object: Run object
    :param artifacts_dir: artifacts directory
    :return: model wrapper containing pytorch mode, tokenizer, vectorizer
    """
    _logger.info("Loading model from artifacts")

    if artifacts_dir is None:
        artifacts_dir = OutputLiterals.OUTPUT_DIR

    run_object.download_file(os.path.join(artifacts_dir, OutputLiterals.MODEL_FILE_NAME),
                             output_file_path=OutputLiterals.MODEL_FILE_NAME)

    _logger.info("Finished loading model from training output")

    with open(OutputLiterals.MODEL_FILE_NAME, "rb") as f:
        model = pickle.load(f)
    return model


def get_vectorizer(train_df: pd.DataFrame, val_df: Union[pd.DataFrame, None],
                   label_column_name: str) -> CountVectorizer:
    """Obtain labels vectorizer

    :param train_df: Training DataFrame
    :param val_df: Validation DataFrame
    :param label_column_name: Name/title of the label column
    :return: vectorizer
    """
    # Combine both dataframes if val_df exists
    if val_df is not None:
        combined_df = pd.concat([train_df, val_df])
    else:
        combined_df = train_df

    # Get combined label column
    combined_label_col = np.array(combined_df[label_column_name].astype(str))

    # TODO: CountVectorizer could run into memory issues for large datasets
    vectorizer = CountVectorizer(token_pattern=r"(?u)\b\w+\b", lowercase=False)
    vectorizer.fit(combined_label_col)

    return vectorizer
