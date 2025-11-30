#!/usr/bin/env python3
"""
Mapper pour le tri MapReduce
Lit les nombres depuis stdin et émet des paires clé-valeur
"""

import sys

def mapper():
    """
    Phase Map : Émet chaque nombre comme paire (clé, valeur)
    
    La clé est le nombre lui-même pour permettre le tri automatique
    par Hadoop lors de la phase shuffle
    """
    for line in sys.stdin:
        # Nettoyer la ligne (enlever espaces et retours à la ligne)
        line = line.strip()
        
        # Ignorer les lignes vides
        if not line:
            continue
        
        try:
            # Convertir en nombre
            number = int(line)
            
            # Émettre la paire clé-valeur
            # Format: clé\tvaleur
            # La clé = la valeur pour permettre le tri
            print(f"{number}\t{number}")
            
        except ValueError:
            # Ignorer les lignes non numériques
            sys.stderr.write(f"Avertissement: ligne ignorée (non numérique): {line}\n")
            continue

if __name__ == '__main__':
    mapper()