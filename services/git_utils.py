import subprocess as sp


def git_diff():
    process = sp.run(["git", "diff","--staged"], capture_output=True, text=True, encoding="utf-8")
    return process.stdout
