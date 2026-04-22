import math
import matplotlib.pyplot as plt
import os

# Configuration système
# On récupère et utilise la valeur de WCET mesurée
if not os.path.exists("wcet.txt"):
    print("ERREUR : Lance d'abord recup_time.py pour générer la valeur de C1 !")
    exit()

with open("wcet.txt", "r") as f:
    C1_VAL = float(f.read())

tasks = [
    ("T1", C1_VAL, 10),
    ("T2", 3, 10),
    ("T3", 2, 20),
    ("T4", 2, 20),
    ("T5", 2, 40),
    ("T6", 2, 40),
    ("T7", 3, 80)
]

HYPERPERIOD = 80 

# Génération de tous les jobs sur l'hyperpériode
jobs_base = []
for name, ci, ti in tasks:
    for arrival in range(0, HYPERPERIOD, ti):
        jobs_base.append({
            'name': name,
            'arrival': arrival,
            'duration': ci,
            'deadline': arrival + ti,
            'id': f"{name}_{arrival}"
        })

# --- 2. MOTEUR DE SIMULATION ---
def simulate(job_list, strategy="SJF", allow_t5_miss=False):
    current_time = 0
    waiting_jobs = [j.copy() for j in job_list]
    executed_jobs = []
    
    while waiting_jobs:
        # On regarde quels jobs sont arrivés
        ready_jobs = [j for j in waiting_jobs if j['arrival'] <= current_time]
        
        if not ready_jobs:
            # Si personne n'est prêt, on avance le temps à la prochaine arrivée
            current_time = min(j['arrival'] for j in waiting_jobs)
            continue
        
        if strategy == "EDF":
            # Question 1 : Le plus urgent d'abord 
            current_job = min(ready_jobs, key=lambda x: x['deadline'])
        else:
            # Question 2 : SJF avec gestion des jobs critiques
            # On vérifie si un job (hors T5) risque de rater sa deadline s'il n'est pas pris
            critical_jobs = [j for j in ready_jobs if j['name'] != "T5" and 
                             (current_time + j['duration'] > j['deadline'] - 3)] 
            
            if critical_jobs:
                current_job = min(critical_jobs, key=lambda x: x['deadline'])
            else:
                # Sinon, on applique SJF (le plus court d'abord) pour réduire l'attente
                current_job = min(ready_jobs, key=lambda x: x['duration'])

        # Exécution
        start_time = current_time
        end_time = start_time + current_job['duration']
        wait_time = start_time - current_job['arrival']
        is_missed = end_time > current_job['deadline']
        
        current_job.update({
            'start': start_time, 
            'end': end_time, 
            'wait': wait_time, 
            'missed': is_missed
        })
        
        # Alerte si tache ratée
        if is_missed and not (current_job['name'] == "T5" and allow_t5_miss):
            print(f"  [!] ALERTE : {current_job['id']} a raté sa deadline ({end_time:.2f} > {current_job['deadline']})")


        executed_jobs.append(current_job)
        waiting_jobs.remove(next(j for j in waiting_jobs if j['id'] == current_job['id']))
        current_time = end_time
        
    return executed_jobs

# tracés en mode gantt
def plot_schedule(executed_jobs, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Couleurs par tâche
    colors = {
        "T1": "tab:red", "T2": "tab:orange", "T3": "tab:blue",
        "T4": "tab:purple", "T5": "tab:green", "T6": "tab:cyan", "T7": "tab:pink"
    }
    
    for j in executed_jobs:
        # On place chaque tâche sur une ligne Y différente
        y_pos = int(j['name'][1:]) 
        ax.broken_barh([(j['start'], j['duration'])], (y_pos - 0.4, 0.8), 
                       facecolors=colors[j['name']], edgecolor='black', alpha=0.8)
        
        # Petit texte pour le nom 
        ax.text(j['start'] + j['duration']/2, y_pos, j['name'], 
                ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        
        # croix rouge si la deadline est loupée
        if j['missed']:
            ax.plot(j['deadline'], y_pos, 'rx', markersize=10, markeredgewidth=2)

    ax.set_ylim(0.5, 7.5)
    ax.set_xlim(0, HYPERPERIOD)
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Tâches")
    ax.set_yticks(range(1, 8))
    ax.set_yticklabels([f"T{i}" for i in range(1, 8)])
    ax.set_title(title)
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# résultats + analyse

# Simulation Q1 (Strict)
res_q1 = simulate(jobs_base, strategy="EDF")
print(f"--- Q1 (EDF Strict) ---")
print(f"Attente totale : {sum(j['wait'] for j in res_q1):.3f} s")
print(f"Succès : {not any(j['missed'] for j in res_q1)}")

# check processor idle time
total_duration = sum(j['duration'] for j in res_q1)
theoretical_idle = 80 - total_duration
actual_idle = 80 - res_q1[-1]['end'] # Temps libre restant à la fin du cycle

print(f"\n --- VÉRIFICATION MAXIMISATION IDLE ---")
print(f"Somme des exécutions (Travail) : {total_duration:.3f} s")
print(f"Idle Time théorique disponible : {theoretical_idle:.3f} s")
print(f"Waiting Time total calculé     : {sum(j['wait'] for j in res_q1):.3f} s")

# La vérification demandée 
if any(j['missed'] for j in res_q1):
    print("Vérification : ÉCHEC (Deadlines manquées)")
else:
    print(f"Vérification : SUCCÈS. L'Idle time est de {theoretical_idle:.3f}s.")
    print("Aucune exécution ne déborde.")

# Simulation Q2 (SJF + T5 flexible)
res_q2 = simulate(jobs_base, strategy="SJF", allow_t5_miss=True)
print(f"\n--- Q2 (SJF Optimisé) ---")
print(f"Attente totale : {sum(j['wait'] for j in res_q2):.3f} s")
t5_miss = len([j for j in res_q2 if j['name'] == "T5" and j['missed']])
print(f"Retards T5 autorisés : {t5_miss}")

# Affichage des graphiques
plot_schedule(res_q1, f"Ordonnancement EDF (Strict) - C1 = {C1_VAL}s")
plot_schedule(res_q2, f"Ordonnancement SJF (Priorité Court) - C1 = {C1_VAL}s")