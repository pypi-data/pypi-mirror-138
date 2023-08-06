from akerbp.mlpet import Dataset
from akerbp.mlpet.Datasets import dataloader
from cognite.client import CogniteClient

client = CogniteClient(client_name="test", project="akbp-subsurface")


def test_load_from_cdf():
    dl = dataloader.DataLoader()
    df = dl.load_from_cdf(
        client=client, metadata={"wellbore_name": "25/2-7", "subtype": "BEST"}
    )
    assert df.shape[0] > 0


def test_load_from_las():
    ds = Dataset(
        mappings={"curve_mappings": {}, "groups_map": {}},
        settings={
            "curves": [
                "CALI",
                "BS",
                "DCAL",
                "ROPA",
                "ROP",
                "RDEP",
                "RMED",
                "DTS",
                "DTC",
                "NPHI",
                "PEF",
                "GR",
                "RHOB",
                "DRHO",
            ],
            "label_column": "FORCE_2020_LITHOFACIES_LITHOLOGY",
            "id_column": "well_name",
            "data_path": r"./",
            "depth_column": "DEPTH_MD",
        },
        folder_path=r"./",
    )

    ds.load_from_las(
        [
            "akerbp/mlpet/tests/data/15_9-23.las",
            "akerbp/mlpet/tests/data/25_2-7.las",
            "akerbp/mlpet/tests/data/35_12-1.las",
        ]
    )
