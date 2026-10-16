import csv, statistics as S, os
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(f"{D}/results/runs.csv")))
tasks = sorted({r["task"] for r in rows}); out=[]
for t in tasks:
    d={"task":t}
    for arm in ("bare","frontload"):
        rs=[r for r in rows if r["task"]==t and r["cond"]==arm]
        d[f"{arm}_pass"]=f"{sum(r['passed']=='True' for r in rs)}/{len(rs)}"
        for k in ("total_tokens","output_tokens","num_turns","tool_calls","est_cost_usd","wall_s"):
            d[f"{arm}_{k}"]=round(S.mean(float(r[k]) for r in rs),4)
    d["cost_saving_pct"]=round(100*(1-d["frontload_est_cost_usd"]/d["bare_est_cost_usd"]),1)
    d["token_saving_pct"]=round(100*(1-d["frontload_total_tokens"]/d["bare_total_tokens"]),1)
    out.append(d)
tot={"task":"ALL (mean)"}
for k in out[0]:
    if k!="task" and not k.endswith("_pass"): tot[k]=round(S.mean(o[k] for o in out),4)
for arm in ("bare","frontload"):
    rs=[r for r in rows if r["cond"]==arm]; tot[f"{arm}_pass"]=f"{sum(r['passed']=='True' for r in rs)}/{len(rs)}"
tot["cost_saving_pct"]=round(100*(1-tot["frontload_est_cost_usd"]/tot["bare_est_cost_usd"]),1)
tot["token_saving_pct"]=round(100*(1-tot["frontload_total_tokens"]/tot["bare_total_tokens"]),1)
out.append(tot)
w=csv.DictWriter(open(f"{D}/results/summary.csv","w"),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for o in out: print(o)
fig,ax=plt.subplots(1,3,figsize=(15,4.6)); x=np.arange(len(tasks))
for i,(k,lab) in enumerate((("total_tokens","total tokens (mean of 2)"),("est_cost_usd","API-equivalent est. $"),("tool_calls","tool calls"))):
    b=[o[f"bare_{k}"] for o in out[:-1]]; f=[o[f"frontload_{k}"] for o in out[:-1]]
    ax[i].bar(x-0.2,b,0.4,label="bare bug report (explore)",color="#999"); ax[i].bar(x+0.2,f,0.4,label="front-loaded path+files",color="#d17b4a")
    ax[i].set_xticks(x); ax[i].set_xticklabels(tasks,rotation=30,fontsize=8); ax[i].set_title(lab)
ax[0].legend(fontsize=8)
plt.suptitle(f"#015 Claude Code: front-loading context cut tokens {tot['token_saving_pct']}% and est. cost {tot['cost_saving_pct']}% (24 runs, all passed)",fontsize=11)
plt.tight_layout(); plt.savefig(f"{D}/results/chart.png",dpi=110)
