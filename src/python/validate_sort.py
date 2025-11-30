#!/usr/bin/env python3
"""
Script de validation du tri MapReduce
Vérifie que le résultat est correctement trié
"""

import sys
import os
from typing import List, Tuple

def load_numbers(filepath: str) -> List[int]:
    """Charge les nombres depuis un fichier"""
    numbers = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    numbers.append(int(line))
    except FileNotFoundError:
        print(f"❌ Erreur: Fichier '{filepath}' introuvable")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Erreur: Ligne non numérique trouvée - {e}")
        sys.exit(1)
    
    return numbers

def validate_sorted(numbers: List[int]) -> Tuple[bool, str]:
    """
    Valide que les nombres sont triés en ordre croissant
    
    Returns:
        (is_sorted, message)
    """
    if not numbers:
        return False, "Liste vide"
    
    for i in range(len(numbers) - 1):
        if numbers[i] > numbers[i + 1]:
            return False, f"Erreur à l'index {i}: {numbers[i]} > {numbers[i + 1]}"
    
    return True, "Tri correct ✓"

def get_statistics(numbers: List[int]) -> dict:
    """Calcule des statistiques sur les nombres"""
    return {
        'count': len(numbers),
        'min': min(numbers) if numbers else None,
        'max': max(numbers) if numbers else None,
        'mean': sum(numbers) / len(numbers) if numbers else None,
        'range': max(numbers) - min(numbers) if numbers else None
    }

def compare_files(input_file: str, output_file: str):
    """Compare les fichiers input et output"""
    print("═" * 60)
    print("  Validation du Tri MapReduce")
    print("═" * 60)
    print()
    
    # Charger les fichiers
    print("📂 Chargement des fichiers...")
    input_numbers = load_numbers(input_file)
    output_numbers = load_numbers(output_file)
    
    print(f"   Input:  {len(input_numbers)} nombres")
    print(f"   Output: {len(output_numbers)} nombres")
    print()
    
    # Vérifier le nombre d'éléments
    if len(input_numbers) != len(output_numbers):
        print("❌ ERREUR: Le nombre d'éléments ne correspond pas !")
        print(f"   Entrée: {len(input_numbers)}")
        print(f"   Sortie: {len(output_numbers)}")
        return False
    
    # Vérifier que c'est trié
    print("🔍 Vérification du tri...")
    is_sorted, message = validate_sorted(output_numbers)
    
    if is_sorted:
        print(f"   ✅ {message}")
    else:
        print(f"   ❌ {message}")
        return False
    
    print()
    
    # Vérifier que ce sont les mêmes éléments
    print("🔍 Vérification de la préservation des données...")
    input_sorted = sorted(input_numbers)
    if input_sorted == output_numbers:
        print("   ✅ Toutes les valeurs sont préservées")
    else:
        print("   ❌ Les valeurs ne correspondent pas !")
        # Trouver les différences
        input_set = set(input_numbers)
        output_set = set(output_numbers)
        missing = input_set - output_set
        extra = output_set - input_set
        if missing:
            print(f"   Valeurs manquantes: {missing}")
        if extra:
            print(f"   Valeurs en trop: {extra}")
        return False
    
    print()
    
    # Statistiques
    print("📊 Statistiques:")
    stats = get_statistics(output_numbers)
    print(f"   Nombre d'éléments: {stats['count']}")
    print(f"   Minimum: {stats['min']}")
    print(f"   Maximum: {stats['max']}")
    print(f"   Moyenne: {stats['mean']:.2f}")
    print(f"   Plage: {stats['range']}")
    
    print()
    
    # Aperçu
    print("👀 Aperçu des résultats:")
    print(f"   Premiers 5: {output_numbers[:5]}")
    print(f"   Derniers 5: {output_numbers[-5:]}")
    
    print()
    print("═" * 60)
    print("  ✅ VALIDATION RÉUSSIE : Le tri est correct !")
    print("═" * 60)
    
    return True

def main():
    """Point d'entrée principal"""
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} <output_file>")
        print(f"  {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    
    if len(sys.argv) == 2:
        # Mode simple : vérifier juste le tri
        output_file = sys.argv[1]
        numbers = load_numbers(output_file)
        is_sorted, message = validate_sorted(numbers)
        
        if is_sorted:
            print(f"✅ {message}")
            stats = get_statistics(numbers)
            print(f"   Éléments: {stats['count']}, Min: {stats['min']}, Max: {stats['max']}")
            sys.exit(0)
        else:
            print(f"❌ {message}")
            sys.exit(1)
    
    elif len(sys.argv) == 3:
        # Mode complet : comparer input et output
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        success = compare_files(input_file, output_file)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()