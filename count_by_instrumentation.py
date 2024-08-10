from datetime import datetime
from typing import List
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import argparse

from data_filter import DataFilter
from utilities import count_by_language_and_file_extension

from github_client import GithubClient


class App:
    def __init__(self, languages: List[str], path_prefix: str, keyword: str):
        self.client = GithubClient()
        self.data_filter = DataFilter(languages=languages,
                                      path_prefix=path_prefix, keyword=keyword)

    def get_commit_by_date(self, repository, date):
        return self.client.get_most_recent_commit(repository, date, "main")

    def get_repository_by_commit(self, repository, commit):
        repo_data = self.client.get_repository_at_commit(repository, commit)
        repo_data = self.data_filter.parse_data(repo_data)

        return repo_data


def main(args):
    app = App(
        languages=[args.language],
        path_prefix="instrumentation/",
        keyword="test"
    )

    today = datetime.now().date().strftime("%Y-%m-%dT%H:%M:%SZ")

    commit = app.get_commit_by_date(date=today, repository=args.repo)
    repo_files = app.get_repository_by_commit(
        repository=args.repo,
        commit=commit
    )
    count = count_by_language_and_file_extension(files=repo_files["files"],
                                                 languages=[args.language])

    df = pd.DataFrame(list(count.items()), columns=['Key', 'Value'])
    df = df.sort_values(by='Value', key=lambda col: col.astype(int), ascending=False)

    sns.set_theme()
    colors = sns.color_palette('pastel')[0:len(df)]

    # Create a pie chart
    explode = [0.05] * len(df)  # this will "explode" each slice from the pie
    df.set_index('Key')['Value'].plot.pie(autopct='%1.0f%%', colors=colors,
                                          explode=explode)

    plt.title(f'Remaining {args.language} files by Instrumentation')
    plt.ylabel('')

    print(df.to_markdown(index=False))
    print(f"| Total | {df['Value'].sum()} |")

    if args.output is not None:
        plt.savefig(args.output)
    else:
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Show Pie chart of file count in test folders')
    parser.add_argument("-r", "--repo",
                        help="Repository name. "
                             "ex: open-telemetry/opentelemetry-java-instrumentation",
                        required=True)
    parser.add_argument("-l", "--language",
                        help="Language to analyze"
                             "ex: groovy",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="File name to output graph to (leave blank and no file is generated)."
                             "ex: pie-chart-counts.png")
    arguments = parser.parse_args()
    main(arguments)