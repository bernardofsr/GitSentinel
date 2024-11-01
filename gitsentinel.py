import os
import subprocess
import requests
import threading
import argparse
import time

# GitHub token and API URL
GITHUB_TOKEN = "GITHUB_TOKEN"  # Replace with your actual GitHub token
API_URL = "https://api.github.com"

# Create directories for storing repos and reports
os.makedirs("repositories", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# Function to get all repositories for a GitHub user
def get_repos(user):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    repos = []
    page = 1

    while True:
        url = f"{API_URL}/users/{user}/repos?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch repos for user {user}: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1

    return [repo["clone_url"] for repo in repos]

# Function to clone the repository and run Gitleaks
def scan_repository(user, repo_url, wait_time):
    repo_name = repo_url.split('/')[-1].replace(".git", "")
    clone_dir = os.path.join("repositories", f"{user}_{repo_name}")

    # Clone the repository
    try:
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
        print(f"Cloned {repo_name} successfully.")

        # Wait for the specified time after cloning
        if wait_time > 0:
            print(f"Waiting for {wait_time} seconds before proceeding to the next repository...")
            time.sleep(wait_time)

    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository {repo_url}: {e}")

    # Run Gitleaks on the cloned repository and save the report
    report_path = os.path.join("reports", f"{user}_{repo_name}_gitleaks_report.json")
    try:
        result = subprocess.run(
            ["gitleaks", "detect", "--source", clone_dir, "--report-path", report_path, "--report-format", "json"],
            check=True,
            capture_output=True
        )
        print(f"Gitleaks output for {repo_url}: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run Gitleaks on {repo_url}: {e}\nOutput: {e.output.decode()}")
    finally:
        # Clean up the cloned repository
        subprocess.run(["rm", "-rf", clone_dir])
        print(f"Completed scan for {user}/{repo_name} and saved report to {report_path}")

    # Wait for specified time before proceeding to the next repo
    time.sleep(wait_time)

# Function to handle the scanning process for each user
def scan_user_repos(user, wait_time):
    print(f"Scanning repositories for user: {user}")
    repos = get_repos(user)
    threads = []

    for repo_url in repos:
        # Start a new thread for each repository scan
        thread = threading.Thread(target=scan_repository, args=(user, repo_url, wait_time))
        thread.start()
        threads.append(thread)

        # Wait for the specified time before starting the next repository clone
        if wait_time > 0:
            print(f"Waiting {wait_time} seconds before cloning the next repository...")
            time.sleep(wait_time)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Main execution
if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Scan GitHub repositories for secrets using Gitleaks.")
    parser.add_argument('--user-file', type=str, required=True, help='Path to the file containing GitHub usernames.')
    parser.add_argument('--threads', type=int, default=5, help='Number of threads to use for scanning (default: 5).')
    parser.add_argument('--wait-git-clone', type=int, default=5, help='Wait time in seconds between each git clone (default: 5).')

    args = parser.parse_args()

    # Read usernames from the specified file
    with open(args.user_file, "r") as file:
        usernames = [line.strip() for line in file.readlines()]

    # Scan each user's repositories
    for user in usernames:
        scan_user_repos(user, args.wait_git_clone)

    print("All repositories have been scanned.")
