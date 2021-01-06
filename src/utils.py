"""Utils module for shared functions across Jupyter notebooks."""

import os
from pathlib import Path
from typing import Iterator, Tuple

import boto3
import pandas as pd


def upload_files(files: Iterator[Tuple[str, str]]) -> None:
    """Upload files to S3/Ceph.

    Takes a list of local paths and associated/desired S3 keys and
    uploads the files to given location.

    Args:
        files (Iterator[Tuple[str, str]]): List of pairs of local path and S3 key
    """
    s3_endpoint_url = os.getenv("S3_ENDPOINT_URL")
    s3_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    s3_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_bucket_name = os.getenv("S3_BUCKET", "DH-PLAYPEN")
    s3_path = os.getenv("S3_PROJECT_KEY", "mcliffor/fedora_devel_mail")

    s3 = boto3.client(
        "s3",
        endpoint_url=s3_endpoint_url,
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
    )

    for path, key in files:
        print(f"Uploading file: {path} to {s3_path}/{key}", end="...\t")
        s3.upload_file(Filename=path, Bucket=s3_bucket_name, Key=f"{s3_path}/{key}")
        print("Done")


def load_dataset(path: str) -> pd.DataFrame:
    """Load all dataset chunks in a folder.

    Get all dataset chunks in a folder and concat them into a single DataFrame.

    Args:
        path (str): Dataset folder location.

    Returns:
        pd.DataFrame: Concatenated DataFrame containing all chunks.
    """
    dataset_chunks_df = (
        pd.read_csv(f, index_col="Unnamed: 0") for f in Path(path).glob("*.csv")
    )
    return pd.concat(dataset_chunks_df, ignore_index=True)
