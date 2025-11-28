import subprocess

def run_step(name, command):
    print(f"\n🚀 Running step: {name} ...")
    result = subprocess.run(command, shell=True)

    if result.returncode == 0:
        print(f"✅ {name} Completed!\n")
    else:
        print(f"❌ {name} Failed!")
        exit(1)

def main():
    print("======================================")
    print("      🟦 E-COMMERCE ETL PIPELINE")
    print("======================================")

    # 1) INGEST RAW DATA → PostgreSQL
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
