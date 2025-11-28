import subprocess


def run_step(name, command):
    print("\n======================================")
    print(f"🚀 Running step: {name}")
    print("======================================")

    result = subprocess.run(command, shell=True)

    if result.returncode == 0:
        print(f"✅ {name} Completed!\n")
    else:
        print(f"❌ {name} Failed! (exit code = {result.returncode})")
        raise SystemExit(result.returncode)


def main():
    print("======================================")
    print("      🟦 E-COMMERCE ETL PIPELINE")
    print("======================================")

    # 1) INGEST → raw_data.kaggle_raw
    run_step("Ingest Step", "python ingest.py")

    # 2) TRANSFORM → production.fact_sales
    run_step("Transform Step", "python transform.py")

    # 3) PUBLISH → Google Sheets
    run_step("Publish Step", "python publish.py")

    print("======================================")
    print("🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
    print("======================================")


if __name__ == "__main__":
    main()