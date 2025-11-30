#!/usr/bin/env python3
"""
Générateur de données pour l'exercice MapReduce
Crée un fichier avec 100 nombres aléatoires
"""

import random
import os

def generate_random_numbers(count=100, min_val=1, max_val=1000, output_file='data/input/numbers.txt'):
    """
    Génère un fichier contenant des nombres aléatoires
    
    Args:
        count: Nombre de valeurs à générer
        min_val: Valeur minimale
        max_val: Valeur maximale
        output_file: Chemin du fichier de sortie
    """
    # Créer le répertoire data s'il n'existe pas
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Générer les nombres aléatoires
    numbers = [random.randint(min_val, max_val) for _ in range(count)]
    
    # Écrire dans le fichier (un nombre par ligne)
    with open(output_file, 'w') as f:
        for number in numbers:
            f.write(f"{number}\n")
    
    print(f"✓ {count} nombres générés dans {output_file}")
    print(f"  Plage: [{min_val}, {max_val}]")
    print(f"  Premiers nombres: {numbers[:5]}")
    print(f"  Derniers nombres: {numbers[-5:]}")
    
    # Statistiques
    print(f"\nStatistiques:")
    print(f"  Min: {min(numbers)}")
    print(f"  Max: {max(numbers)}")
    print(f"  Moyenne: {sum(numbers) / len(numbers):.2f}")

if __name__ == '__main__':
    generate_random_numbers()