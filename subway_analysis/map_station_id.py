import pandas as pd


def map_station_id(line, index):
    return 100 * line + index

if __name__ == "__main__":

    for line in [1, 2, 4]:
        df = pd.read_csv(f"data/line_{line}_ridership.csv")
        df["index"] = df.index
        df["stationID"] = df.apply(lambda x: map_station_id(line, x["index"]), axis=1)
        df.drop(columns=["index"], inplace=True)
        df.to_csv(f"data/line{line}_stationID.csv", index=False)