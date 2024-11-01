import json
import argparse
import os

# Set up argument parsing
parser = argparse.ArgumentParser(description="Analyze all Gitleaks JSON reports.")
parser.add_argument('--report-dir', type=str, required=True, help='Path to the directory containing Gitleaks report files.')

args = parser.parse_args()

# Check if the provided report directory exists
if not os.path.exists(args.report_dir):
    print(f"❌ The specified directory '{args.report_dir}' does not exist.")
    exit(1)

# List all JSON files in the report directory
report_files = [f for f in os.listdir(args.report_dir) if f.endswith('.json')]

# Check if there are any JSON report files
if not report_files:
    print("⚠️ No JSON report files found in the specified directory.")
    exit(0)

# Variables for overall summary
total_files = 0
total_secrets_found = 0

# Analyze each report file
for report_file in report_files:
    report_path = os.path.join(args.report_dir, report_file)
    total_files += 1

    with open(report_path, 'r') as file:
        try:
            # Load JSON data
            data = json.load(file)
        except json.JSONDecodeError:
            print(f"⚠️ Failed to decode JSON from '{report_path}'. Skipping this file.")
            continue

        # Check if the data is a list and process each secret
        if isinstance(data, list) and data:
            total_secrets = len(data)
            total_secrets_found += total_secrets
            print(f"\n📄 **Report for '{report_file}': {total_secrets} secrets found**\n")

            for i, secret in enumerate(data, 1):
                repo = report_file.replace("_gitleaks_report.json", "")
                file_path = secret.get('File', 'N/A')
                commit = secret.get('Commit', 'N/A')
                line = secret.get('StartLine', 'N/A')
                match = secret.get('Match', 'N/A')
                secret_value = secret.get('Secret', 'N/A')
                rule = secret.get('Description', 'N/A')

                print("------------------------------------------------")
                print(f"🔍 Secret #{i}")
                print(f"Repository  : {repo}")
                print(f"File        : {file_path}")
                print(f"Commit      : {commit}")
                print(f"Line        : {line}")
                print(f"Match       : {match}")
                print(f"Secret      : {secret_value}")
                print(f"Rule        : {rule}")
                print("------------------------------------------------\n")
        else:
            print(f"⚠️ No valid secret entries found in '{report_file}'.")

# Overall Summary
print("\n=== 📝 Overall Summary ===")
print(f"Total files processed     : {total_files}")
print(f"Total secrets found       : {total_secrets_found}")
