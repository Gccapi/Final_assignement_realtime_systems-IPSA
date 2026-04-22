import subprocess # plutot que os (plus rapide)
import time
import numpy as np

# code à lancer depuis ubuntu direct (python3 recup_time.py) après compilation du code C
# gcc product.c -o task1_linux -O0

executable = "./task1_linux"
iterations = 100 
durations = []

print(f"Lancement de {iterations} itérations (~60secondes en test)...")

for i in range(iterations):
    print(f"\rProgression : {i+1}/{iterations}", end="")
    start = time.perf_counter()
    # os.system est beaucoup plus rapide sous Linux, mieux qu'avec windows mais tjrs lourd donc remplacé
    subprocess.run([executable], capture_output=True) 
    end = time.perf_counter()
    
    # On stocke en secondes 
    durations.append(end - start)

# ANALYSE DES RÉSULTATS 
if durations:
    c1_wcet_mesure = np.max(durations)
    c1_wcet_securite = c1_wcet_mesure * 1.2 # Marge de 20% pour le WCET réel
    
    print("\n\n--- STATISTIQUES TÂCHE T1 (WSL) ---")
    print(f"Min: {np.min(durations):.6f} s")
    print(f"Q1 (25%): {np.percentile(durations, 25):.6f} s")
    print(f"Q2 (Médiane): {np.median(durations):.6f} s")
    print(f"Q3 (75%): {np.percentile(durations, 75):.6f} s")
    print(f"Max (WCET mesuré): {c1_wcet_mesure:.6f} s")
    print(f"WCET retenu (+20%): {c1_wcet_securite:.6f} s")
    
    # Calcul de l'utilisation réelle (U = Ci / Ti)
    # T2=3s, T3=2s, T4=2s, T5=2s, T6=2s, T7=3s
    # Périodes : 10, 20, 20, 40, 40, 80
    u_others = (3/10) + (2/20) + (2/20) + (2/40) + (2/40) + (3/80)
    u_total = (c1_wcet_securite / 10) + u_others

    print("\n--- ANALYSE DU SYSTÈME ---")
    print(f"Utilisation totale (U): {u_total:.4f}")
    
    if u_total <= 1:
        print("Résultat: Le système est SCHEDULABLE")
    else:
        print("Résultat: SURCHARGE (Trop de calcul pour les périodes imparties).")


    # sauvegarde de la valeur pour scheduler après 
    with open("wcet.txt", "w") as f:
        f.write(str(c1_wcet_securite))