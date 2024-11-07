
![GitSentinel](logo.png)

GitSentinel is a Python-based tool for scanning multiple users GitHub repositories for sensitive information using [Gitleaks](https://github.com/gitleaks/gitleaks). This tool automates cloning and scanning multiple repositories with configurable wait times, leveraging multithreading to process several repositories concurrently.

## Features

- **Automated Repo Cloning**: Fetches and clones all repositories of specified GitHub users.
- **Sensitive Data Scanning**: Runs Gitleaks on each repository to detect secrets and sensitive information.
- **Configurable Threading**: Supports multiple threads for faster processing of large repositories.
- **Adjustable Wait Time**: Customizable wait period between cloning operations to manage API rate limits and avoid overloads.
- **Report Generation**: Outputs JSON reports with detailed information about any findings from Gitleaks.
- **Analyzer Tool**: Analyzes JSON reports to summarize and display findings for easy review.

## Requirements & API Token

- **Python 3.x**
- **Gitleaks**: Ensure that [Gitleaks](https://github.com/gitleaks/gitleaks) is installed and accessible in your system’s PATH.
- **GitHub Token**: A GitHub token with access to the repositories you intend to scan. Replace `GITHUB_TOKEN` in the script with your token. Get yours here [GitHub Tokens](https://github.com/settings/tokens)

## Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/gitsentinel.git
cd gitsentinel
```

Ensure **Gitleaks** is installed and accessible:

```bash
gitleaks version
```

If Gitleaks is not installed, follow the instructions [here](https://github.com/gitleaks/gitleaks?tab=readme-ov-file#installing) to install it.

## Usage

### Command-Line Arguments

- **`--user-file`**: Path to a text file containing GitHub usernames to scan (one username per line).
- **`--threads`**: Number of threads to use for scanning (default is 5).
- **`--wait-git-clone`**: Wait time in seconds between each repository clone (default is 5).

### Example Usage

```bash
python gitsentinel.py --user-file users.txt --threads 10 --wait-git-clone 10
```

### Sample `users.txt` Format

Each line in `users.txt` should contain one GitHub username:

```
user1
user2
user3
```
#

## Analyzer Tool

The analyzer tool provides a summarized and structured output for Gitleaks JSON reports.

### Running the Analyzer

Use the following command to analyze JSON report files:

```bash
python analyzer_gitsentinel.py --report-dir reports
```

### Output Format

- **Summary**: Shows the total number of secrets found in each report file.
- **Detailed Secrets**: Displays each secret with information such as the repository name, file path, commit ID, line number, the secret found, and the rule matched.
- **Overall Summary**: After processing all files, an overview of total files scanned and secrets found is displayed.

Example Output:

```
📄 **Report for 'user_repo_gitleaks_report.json': 1 secret found**

------------------------------------------------
🔍 Secret #1
Repository  : user/repo
File        : path/to/file.txt
Commit      : abc123
Line        : 42
Secret      : 'example_secret_value'
Rule        : 'Generic Credential'
Author      : 'Author Name'
Email       : 'Author Email'
------------------------------------------------

=== 📝 Overall Summary ===
Total files processed     : 3
Total secrets found       : 1
```

## Output

GitSentinel generates two types of outputs:

- **Cloned Repositories**: Stored in the `repositories` folder, these are cleaned up after each scan.
- **Gitleaks Reports**: JSON reports for each repository are saved in the `reports` folder with the format `<username>_<repo_name>_gitleaks_report.json`.

## Notes

- **API Rate Limits**: Using a GitHub token helps avoid rate limits. Set the token in the `GITHUB_TOKEN` variable in `gitsentinel.py`.
- **Threading**: Increasing the number of threads may speed up processing but could also increase the load on your network or risk hitting GitHub’s API limits.
- **Wait Time**: Adjust `--wait-git-clone` to control the delay between each clone, useful for avoiding GitHub’s rate limits.

## Disclaimer

This tool is intended for authorized use only. Ensure you have permission to scan any repositories that you do not own. Misuse of GitSentinel may violate GitHub’s terms of service and/or applicable laws.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request to propose improvements.

## Acknowledgments

- **[Gitleaks](https://github.com/gitleaks/gitleaks)** for providing a robust open-source tool for scanning repositories.
