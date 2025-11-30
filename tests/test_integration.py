#!/usr/bin/env python3
"""
Tests d'intégration pour le projet MapReduce Sorting
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'python'))

def test_local_pipeline():
    """Test du pipeline MapReduce complet en local"""
    print("═" * 60)
    print("  Test du Pipeline Local MapReduce")
    print("═" * 60)
    print()
    
    # Créer un répertoire temporaire
    with tempfile.TemporaryDirectory() as tmpdir:
        # Données de test
        test_numbers = [42, 7, 99, 15, 3, 88, 21, 56, 34, 67, 
                       100, 1, 89, 45, 23, 78, 12, 55, 90, 11]
        
        input_file = os.path.join(tmpdir, 'input.txt')
        output_file = os.path.join(tmpdir, 'output.txt')
        
        # Créer le fichier d'entrée
        with open(input_file, 'w') as f:
            for num in test_numbers:
                f.write(f"{num}\n")
        
        print(f"📂 Fichier de test créé: {len(test_numbers)} nombres")
        print(f"   Min: {min(test_numbers)}, Max: {max(test_numbers)}")
        print()
        
        # Exécuter le pipeline
        print("🔄 Exécution du pipeline MapReduce...")
        
        mapper_path = Path(__file__).parent.parent / 'src' / 'python' / 'mapper.py'
        reducer_path = Path(__file__).parent.parent / 'src' / 'python' / 'reducer.py'
        
        # Pipeline : cat -> mapper -> sort -> reducer
        cmd = f"cat {input_file} | python {mapper_path} | sort -n -k1 | python {reducer_path} > {output_file}"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Erreur lors de l'exécution du pipeline")
            print(result.stderr)
            return False
        
        print("✓ Pipeline exécuté")
        print()
        
        # Lire les résultats
        with open(output_file, 'r') as f:
            output_numbers = [int(line.strip()) for line in f if line.strip()]
        
        # Vérifier le tri
        expected = sorted(test_numbers)
        
        print("📊 Vérification des résultats:")
        print(f"   Entrée:  {test_numbers[:5]}...{test_numbers[-3:]}")
        print(f"   Sortie:  {output_numbers[:5]}...{output_numbers[-3:]}")
        print(f"   Attendu: {expected[:5]}...{expected[-3:]}")
        print()
        
        if output_numbers == expected:
            print("✅ TEST RÉUSSI: Le tri est correct !")
            return True
        else:
            print("❌ TEST ÉCHOUÉ: Le tri est incorrect")
            print(f"   Différences trouvées")
            return False

def test_mapper_output_format():
    """Test du format de sortie du mapper"""
    print("═" * 60)
    print("  Test du Format de Sortie du Mapper")
    print("═" * 60)
    print()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, 'input.txt')
        
        # Créer un fichier de test
        with open(input_file, 'w') as f:
            f.write("42\n7\n99\n")
        
        mapper_path = Path(__file__).parent.parent / 'src' / 'python' / 'mapper.py'
        
        # Exécuter le mapper
        result = subprocess.run(
            f"cat {input_file} | python {mapper_path}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        lines = result.stdout.strip().split('\n')
        
        print(f"📤 Sortie du mapper ({len(lines)} lignes):")
        for line in lines:
            print(f"   {line}")
        print()
        
        # Vérifier le format
        success = True
        for line in lines:
            parts = line.split('\t')
            if len(parts) != 2:
                print(f"❌ Format incorrect: '{line}'")
                success = False
                continue
            
            try:
                key = int(parts[0])
                value = int(parts[1])
                if key != value:
                    print(f"❌ Clé != Valeur: {key} != {value}")
                    success = False
            except ValueError:
                print(f"❌ Valeurs non numériques: '{line}'")
                success = False
        
        if success:
            print("✅ TEST RÉUSSI: Format correct (clé\\tvaleur)")
        else:
            print("❌ TEST ÉCHOUÉ: Format incorrect")
        
        return success

def test_reducer_with_sorted_input():
    """Test du reducer avec des données triées"""
    print("═" * 60)
    print("  Test du Reducer avec Données Triées")
    print("═" * 60)
    print()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, 'sorted_input.txt')
        output_file = os.path.join(tmpdir, 'output.txt')
        
        # Créer un fichier avec des paires clé-valeur triées
        sorted_pairs = [(3, 3), (7, 7), (15, 15), (42, 42), (99, 99)]
        
        with open(input_file, 'w') as f:
            for key, value in sorted_pairs:
                f.write(f"{key}\t{value}\n")
        
        print("📥 Entrée du reducer:")
        with open(input_file, 'r') as f:
            print(f.read())
        
        reducer_path = Path(__file__).parent.parent / 'src' / 'python' / 'reducer.py'
        
        # Exécuter le reducer
        result = subprocess.run(
            f"cat {input_file} | python {reducer_path}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        output_numbers = [int(line.strip()) for line in result.stdout.strip().split('\n') if line.strip()]
        expected = [pair[1] for pair in sorted_pairs]
        
        print("📤 Sortie du reducer:")
        for num in output_numbers:
            print(f"   {num}")
        print()
        
        if output_numbers == expected:
            print("✅ TEST RÉUSSI: Reducer fonctionne correctement")
            return True
        else:
            print("❌ TEST ÉCHOUÉ: Sortie incorrecte")
            print(f"   Attendu: {expected}")
            print(f"   Obtenu:  {output_numbers}")
            return False

def test_large_dataset():
    """Test avec un grand dataset"""
    print("═" * 60)
    print("  Test avec Grand Dataset (1000 nombres)")
    print("═" * 60)
    print()
    
    # Générer 1000 nombres aléatoires
    import random
    test_numbers = [random.randint(1, 10000) for _ in range(1000)]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, 'large_input.txt')
        output_file = os.path.join(tmpdir, 'large_output.txt')
        
        with open(input_file, 'w') as f:
            for num in test_numbers:
                f.write(f"{num}\n")
        
        print(f"📂 Dataset généré: {len(test_numbers)} nombres")
        print()
        
        mapper_path = Path(__file__).parent.parent / 'src' / 'python' / 'mapper.py'
        reducer_path = Path(__file__).parent.parent / 'src' / 'python' / 'reducer.py'
        
        # Mesurer le temps
        import time
        start = time.time()
        
        cmd = f"cat {input_file} | python {mapper_path} | sort -n -k1 | python {reducer_path} > {output_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        duration = time.time() - start
        
        if result.returncode != 0:
            print("❌ Erreur lors de l'exécution")
            return False
        
        # Vérifier le résultat
        with open(output_file, 'r') as f:
            output_numbers = [int(line.strip()) for line in f if line.strip()]
        
        expected = sorted(test_numbers)
        
        print(f"⏱️  Temps d'exécution: {duration:.3f}s")
        print(f"📊 Résultats:")
        print(f"   Nombres traités: {len(output_numbers)}")
        print(f"   Min: {output_numbers[0]}, Max: {output_numbers[-1]}")
        print()
        
        if output_numbers == expected:
            print("✅ TEST RÉUSSI: Grand dataset trié correctement")
            return True
        else:
            print("❌ TEST ÉCHOUÉ: Tri incorrect")
            return False

def run_all_tests():
    """Exécuter tous les tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "TESTS D'INTÉGRATION MAPREDUCE SORTING" + " " * 10 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    tests = [
        ("Format du Mapper", test_mapper_output_format),
        ("Reducer avec données triées", test_reducer_with_sorted_input),
        ("Pipeline local complet", test_local_pipeline),
        ("Grand dataset (1000 nombres)", test_large_dataset),
    ]
    
    results = []
    
    for i, (name, test_func) in enumerate(tests, 1):
        print(f"\n[Test {i}/{len(tests)}] {name}\n")
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ Exception: {e}")
            results.append((name, False))
        print()
    
    # Résumé
    print("═" * 60)
    print("  RÉSUMÉ DES TESTS")
    print("═" * 60)
    print()
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}  {name}")
    
    print()
    print("═" * 60)
    print(f"  Résultat: {passed}/{total} tests réussis")
    print("═" * 60)
    
    return passed == total

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)