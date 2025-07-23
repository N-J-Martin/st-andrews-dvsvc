import pandas as pd

# link to llm output DB at some point
IN_FILE = "../resource/extracted_data_service_context(in).csv"
OUT_FILE = "../resource/output.csv"

def merge(file: str):
    df = pd.read_csv(IN_FILE, usecols=["url", "charity_numbers", "summary", "charity_name", "services", "charity_numbers_corrected","summary_corrected","services_corrected", "charity_name_corrected", "url_corrected"] )
    df["url_corrected"] = df["url_corrected"].fillna(df["url"])
    df["charity_numbers_corrected"] = df["charity_numbers_corrected"].fillna(df["charity_numbers"])
    df["summary_corrected"] = df["summary_corrected"].fillna(df["summary"])
    df["services_corrected"] = df["services_corrected"].fillna(df["services"])
    df["charity_name_corrected"] = df["charity_name_corrected"].fillna(df["charity_name"])
    df = df[["charity_numbers_corrected","summary_corrected","services_corrected", "charity_name_corrected", "url_corrected"]]

    return df



def main():
    df = merge(IN_FILE)
    df.to_csv(OUT_FILE, index=False)
    print("Corrections written to" + OUT_FILE)


if __name__ == "__main__":
    main()