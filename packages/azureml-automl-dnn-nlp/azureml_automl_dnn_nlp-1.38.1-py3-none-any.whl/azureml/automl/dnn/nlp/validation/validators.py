# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""
This file contains abstract classes for dnn nlp data validation
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from azureml.automl.core.shared._diagnostics.contract import Contract
import pandas as pd


class AbstractDataValidator(ABC):
    """Common interface for all dnn nlp data validation."""

    @abstractmethod
    def validate(
            self,
            label_col_name: str,
            train_data: pd.DataFrame,
            valid_data: Optional[pd.DataFrame] = None
    ) -> None:
        """
        Run validations on the user provided data inputs
        Raise error and stop the training if any validation fails

        :param label_col_name: Column name of label column.
        :param train_data: The training set data to validate.
        :param valid_data: The validation set data to validate
        :return: None
        """
        raise NotImplementedError


class AbstractNLPClassificationDataValidator(AbstractDataValidator):
    """
    Common interface for dnn nlp multiclass and multilabel classification scenarios
    """

    def validate(
            self,
            label_col_name: Optional[Any],
            train_data: Any,
            valid_data: Optional[Any] = None
    ) -> None:
        """
        Run validations on the user provided data inputs
        Raise error and stop the training if any validation fails

        :param label_col_name: Column name of label column.
        :param train_data: The training set data to validate.
        :param valid_data: The validation set data to validate
        :return None
        """
        self.check_shared_validation(label_col_name, train_data, valid_data)
        self.check_custom_validation(label_col_name, train_data, valid_data)

    def check_shared_validation(
            self,
            label_col_name: str,
            train_data: pd.DataFrame,
            valid_data: Optional[pd.DataFrame] = None
    ) -> None:
        """
        shared validation steps for multiclass and multilabel scenarios
        Raise error and stop the training if any validation fails

        :param label_col_name: Column name of label column.
        :param train_data: The training set data to validate.
        :param valid_data: The validation set data to validate
        :return None
        """
        self.check_feature_columns(label_col_name, train_data, valid_data)
        self.check_label_column(label_col_name, train_data, valid_data)

    @abstractmethod
    def check_custom_validation(
            self,
            label_col_name: str,
            train_data: pd.DataFrame,
            valid_data: Optional[pd.DataFrame] = None
    ) -> None:
        """
        validation steps only for multiclass or multilabel scenarios
        Raise error and stop the training if any validation fails

        :param label_col_name: Column name of label column.
        :param train_data: The training set data to validate.
        :param valid_data: The validation set data to validate
        :return None
        """
        raise NotImplementedError

    def check_feature_columns(
            self,
            label_col_name: str,
            train_data: pd.DataFrame,
            valid_data: Optional[pd.DataFrame] = None
    ) -> None:
        """
        Run validation on feature columns.
        Validations included:
            check if training set or validation set have duplicated column names
            check if feature columns in training set and validation set are the same
            check if feature columns in training set and validation set have the same order
            check if columns have the same name also have the same data type
        Raise error and stop the training if any validation fails

        :param label_col_name: Column name of label column.
        :param train_data: The training set data to validate.
        :param valid_data: The validation set data to validate
        :return None
        """
        Contract.assert_true(
            len(set(train_data.columns)) == train_data.shape[1],
            "Training set should not have duplicated column names",
            log_safe=True,
        )
        if valid_data:
            Contract.assert_true(
                len(set(valid_data.columns)) == valid_data.shape[1],
                "Validation set should not have duplicated column names",
                log_safe=True,
            )
        train_data = train_data[train_data.columns.diff([label_col_name])]
        if valid_data:
            valid_data = valid_data[valid_data.columns.diff([label_col_name])]
        self._check_same_column_set(train_data, valid_data)
        self._check_column_order(train_data, valid_data)
        self._check_column_type(train_data, valid_data)

    @abstractmethod
    def check_label_column(
            self,
            label_col_name: str,
            train_data: pd.DataFrame,
            valid_data: Optional[pd.DataFrame] = None
    ) -> None:
        """
        Run validation on label column.
        Validations included:
            check if at least one label in validation set is in training set
            check if other conditions are met for the specific task
        Raise error and stop the training if any validation fails

        :param label_col_name: Column name of label column.
        :param train_data: The training set data to validate.
        :param valid_data: The validation set data to validate
        :return None
        """
        raise NotImplementedError

    def _check_same_column_set(
            self,
            train_data: pd.DataFrame,
            valid_data: Optional[pd.DataFrame] = None
    ) -> None:
        """
        Check if training set and validation set have the same set of columns
        Raise error and stop the training if any validation fails

        :param train_data: The training set data to validate.
        :param valid_data: The validation set data to validate
        :return None
        """

        if valid_data is not None:
            Contract.assert_true(
                set(train_data.columns) == set(valid_data.columns),
                "training set and validation set should have same set of columns",
                log_safe=True,
            )

    def _check_column_order(
            self,
            train_data: pd.DataFrame,
            valid_data: Optional[pd.DataFrame] = None
    ) -> None:
        """
        Check if training set and validation set's columns have the same order
        Raise error and stop the training if any validation fails

        :param label_col_name: Column name of label column.
        :param train_data: The training set data to validate.
        :param valid_data: The validation set data to validate
        :return None
        """
        if valid_data:
            for train_col, valid_col in zip(train_data.columns, valid_data.columns):
                Contract.assert_true(
                    train_col == valid_col,
                    "columns in training set and validation set should follow the same order",
                    log_safe=True,
                )

    def _check_column_type(
            self,
            train_data: pd.DataFrame,
            valid_data: Optional[pd.DataFrame] = None
    ) -> None:
        """
        Check if training set and validation set's columns have the same data type
        Raise error and stop the training if any validation fails

        :param train_data: The training set data to validate.
        :param valid_data: The validation set data to validate
        :return None
        """
        if valid_data:
            for col in train_data.columns:
                Contract.assert_true(
                    train_data[col].dtype == valid_data[col].dtype,
                    "Columns that share same column name should have the same data type",
                    log_safe=True,
                )


class AbstractNERDataValidator(AbstractDataValidator):
    """Interface for dnn nlp NER sceanrio"""

    def validate(self, data: Any) -> bool:
        """
        Run validations on the user provided data inputs
        Raise error and stop the training if any validation fails

        :return: None
        """
        raise NotImplementedError
