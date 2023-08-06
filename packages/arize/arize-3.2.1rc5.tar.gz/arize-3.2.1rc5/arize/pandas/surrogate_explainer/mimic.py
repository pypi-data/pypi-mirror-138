import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder

from interpret_community.mimic.mimic_explainer import (
    MimicExplainer,
    LGBMExplainableModel,
)

from arize.utils.types import ModelTypes


class Mimic:
    def __init__(self, X, y, model_type):
        self.feature_names = X.columns

        if model_type == ModelTypes.SCORE_CATEGORICAL:

            def model_func(_):
                return np.array(list(map(lambda p: [1 - p, p], y)))

        elif model_type == ModelTypes.NUMERIC:

            def model_func(_):
                return np.array(y)

        else:
            raise "unrecognized model_type"

        # apply integer encoding to non-numeric columns
        int_enc_X = self._integer_encode_non_numeric_features(X)

        self.explainer = MimicExplainer(
            model_func,
            int_enc_X,
            LGBMExplainableModel,
            augment_data=False,
            is_function=True,
        )

    def explain(self, X, y):

        # apply integer encoding to non-numeric columns
        int_enc_X = self._integer_encode_non_numeric_features(X)

        return pd.DataFrame(
            self.explainer.explain_local(int_enc_X).local_importance_values,
            columns=int_enc_X.columns,
            index=X.index,
        )

    def _integer_encode_non_numeric_features(self, X):
        text_feat, num_feat = X.select_dtypes(object), X.select_dtypes(exclude=object)
        int_enc_feat = pd.DataFrame(
            {
                name: LabelEncoder().fit(data).transform(data)
                for name, data in text_feat.iteritems()
            },
            index=text_feat.index,
        )
        return pd.concat([num_feat, int_enc_feat], axis=1)

    @staticmethod
    def augment(df, prediction_score_column_name, feature_column_names, model_type):
        col_map = {f"{ft}": f"{ft} (feature importance)" for ft in feature_column_names}

        # limit the total number of "cells" to 5M, unless too few rows remain
        samp_df = df.sample(min(len(df), max(1_000, 5_000_000 // df.shape[1])))

        X, y = samp_df[feature_column_names], samp_df[prediction_score_column_name]

        aug_df = pd.concat(
            [
                df,
                Mimic(X, y, model_type).explain(X, y).rename(col_map, axis=1),
            ],
            axis=1,
        )

        # fill null with zero for now, pending update on server side
        aug_df.fillna({c: 0 for c in col_map.values()}, inplace=True)

        return (
            aug_df,
            col_map,
        )
