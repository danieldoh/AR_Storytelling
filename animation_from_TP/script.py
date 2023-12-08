import subprocess

texts = []
with open("./input_prompt.txt", 'r') as f:
    texts = f.readlines()
texts = [t.replace("\n", "") for t in texts]
if '' in texts:
    texts.remove('')

print(texts, len(texts))

if len(texts) == 0:
    print("No Prompts")
elif len(texts) == 1:
    subprocess.run(["./run_one.sh"], shell=True)
elif len(texts) > 1:
    print("multiple")
    subprocess.run(["./run_multiple.sh"], shell=True)
