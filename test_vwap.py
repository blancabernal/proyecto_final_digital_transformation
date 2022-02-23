import pandas as pd
from vwap import vwap


def test_vwap():
    data = {
        "volume": [913, 90, 9, 4003],
        "price": [1, 10, 512, 6626],
    }
    expected = [1.000000, 1.807577, 6.344862, 5290.189232]
    df_data = pd.DataFrame(data, columns=["volume", "price"])
    df_data["expected"] = expected

    df_data = vwap(df_data)
    df_data.vwap = pd.Series(round(x, 6) for x in df_data.vwap)

    compared = df_data.expected == df_data.vwap

    assert compared[0] and compared[1] and compared[2] and compared[3]