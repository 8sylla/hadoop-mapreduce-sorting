#!/usr/bin/env python3
"""
Reducer pour le tri MapReduce
Reçoit les paires clé-valeur triées et émet les valeurs finales
"""

import sys

def reducer():
    """
    Phase Reduce : Émet les valeurs dans l'ordre
    
    Les données arrivent déjà triées par clé grâce à Hadoop
    Le reducer se contente d'émettre les valeurs
    """
    for line in sys.stdin:
        # Nettoyer la ligne
        line = line.strip()
        
        # Ignorer les lignes vides
        if not line:
            continue
        
        try:
            # Parser la paire clé-valeur (format: clé\tvaleur)
            key, value = line.split('\t')
            
            # Émettre uniquement la valeur (déjà triée)
            print(value)
            
        except ValueError:
            # Gérer les erreurs de format
            sys.stderr.write(f"Avertissement: format incorrect: {line}\n")
            continue

if __name__ == '__main__':
    reducer()