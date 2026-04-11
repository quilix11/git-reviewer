import subprocess as sp

def git_diff():
    process = sp.run(["git", "diff","--staged"], capture_output=True, text=True)
    return process.stdout

result = git_diff()
print(result)