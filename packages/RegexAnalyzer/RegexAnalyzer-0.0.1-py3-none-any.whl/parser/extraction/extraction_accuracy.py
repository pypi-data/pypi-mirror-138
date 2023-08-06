# Builtin imports
import sqlite3
import os
import logging

# Internal imports
from extraction import extract
from FoundExpression import FoundExpression

_REPO_PATH = "/mnt/volume_nyc1_01/repos/"
_DB_PATH = "/root/repo-scraper/projects.db"


def main():
    assert os.path.isdir(_REPO_PATH)
    assert os.path.isfile(_DB_PATH)
    db = sqlite3.connect(_DB_PATH)
    conn = db.cursor()
    conn.execute("SELECT * FROM repositories;")
    repos = conn.fetchall()
    total_true = 0
    total_found = 0
    for repo in repos:
        id, name, url, stars = repo
        extracted = extract(os.path.join(_REPO_PATH, url.split("https://github.com/")[1]))
        found_expressions = len(set([f.file for f in filter(lambda x: isinstance(x, FoundExpression),
                                                            extracted)]))
        conn.execute("SELECT COUNT(*) FROM languages WHERE repository=?",
                     (id, ))
        true_expressions = conn.fetchone()[0]
        print(f"{url} - found {found_expressions}/{true_expressions} ({(round(found_expressions/true_expressions, 2))*100}%)")
        total_true += true_expressions
        total_found += found_expressions
    conn.close()
    print(f"In {len(repos)} repositories, picked up expressions in {total_found}/{total_true} files ({round((total_found/total_true), 2)*100}%)")

if __name__ == "__main__":
    main()