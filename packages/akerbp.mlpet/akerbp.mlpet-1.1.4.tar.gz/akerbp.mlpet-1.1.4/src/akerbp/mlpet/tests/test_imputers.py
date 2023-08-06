from akerbp.mlpet.tests.data.data import TEST_DF
from akerbp.mlpet.Datasets.imputers import (
    simple_impute,
    iterative_impute,
    generate_imputation_models,
    impute_depth_trend,
)


def test_simple_impute():
    df = simple_impute(TEST_DF[["AC", "BS"]])
    assert not df.isnull().any().any()


def test_iterative_impute():
    df = iterative_impute(TEST_DF[["AC", "BS"]])
    assert not df.isnull().any().any()


def test_impute_depth_trend():
    df = impute_depth_trend(
        TEST_DF[["DEPTH", "AC", "BS"]],
        curves_to_impute=["BS"],
        depth_column="DEPTH",
        save_imputation_models=True,
        folder_path="./",
    )
    assert not df.isnull().any().any()


def test_impute_depth_trend_with_provided_models():
    models = generate_imputation_models(
        TEST_DF[["DEPTH", "AC", "BS"]], curves=["BS"], depth_column="DEPTH"
    )
    df = impute_depth_trend(
        TEST_DF[["DEPTH", "AC", "BS"]],
        curves_to_impute=["BS"],
        imputation_models=models,
        depth_column="DEPTH",
        save_imputation_models=True,
        folder_path="./",
    )
    assert not df.isnull().any().any()
