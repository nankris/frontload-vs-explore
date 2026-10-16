import os
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = "/workspace/work/tig/_harness/fixtures/SUITE14"
SYM = {"N01_median": "the median helper returns the wrong value for even-length arrays",
       "N02_duration": "the duration parser ignores the seconds part (e.g. \"1h2m3s\")",
       "N03_csv": "the CSV reader breaks on quoted fields that contain commas",
       "T05_stale": "clamp() fails its test",
       "T07_multihunk": "prices use the wrong tax rate (it should be 10%)",
       "T10_replace_all": "some URLs still point at the legacy host"}
jobs = []
for pkg, sym in SYM.items():
    bare = (f"This folder holds 14 small JavaScript packages. Bug report: {sym}. Find the package and fix its code "
            f"so that package's test.js passes. Do not edit any test.js or run_all.js, and don't change other packages.")
    src = open(f"{S}/{pkg}/broken.js").read(); tst = open(f"{S}/{pkg}/test.js").read()
    extra = ""
    for f in sorted(os.listdir(f"{S}/{pkg}")):
        if f not in ("broken.js", "test.js"):
            extra += f"\n`{pkg}/{f}`:\n```\n{open(f'{S}/{pkg}/{f}').read()}\n```\n"
    front = (f"Bug report: {sym}. The bug is in `{pkg}/broken.js`. Check with `cd {pkg} && node test.js` (it should print OK / exit 0). "
             f"Do not edit any test.js and don't change other packages.\n\nCurrent `{pkg}/broken.js`:\n```js\n{src}\n```\n"
             f"`{pkg}/test.js`:\n```js\n{tst}\n```\n{extra}")
    for arm, p in (("bare", bare), ("frontload", front)):
        pf = f"{E}/scripts/prompts/{arm}__{pkg}.txt"; open(pf, "w").write(p)
        for r in (1, 2):
            jobs.append(f"--exp {E} --cond {arm} --task {S} --name {pkg} --rep {r} --timeout 600 "
                        f"--check 'cd {pkg} && node test.js' --prompt \"$(cat {pf})\"")
# interleave arms so cache warmth doesn't favour one arm
open(f"{E}/scripts/jobs.txt", "w").write("\n".join(jobs) + "\n")
print(len(jobs))
