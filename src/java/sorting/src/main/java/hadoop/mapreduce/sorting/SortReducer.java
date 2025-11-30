package src.main.java.hadoop.mapreduce.sorting;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Reducer pour le tri distribué de nombres
 * 
 * Input:  (nombre, [nombre, nombre, ...]) - triées par clé
 * Output: (nombre, null) - on émet juste le nombre
 * 
 * Les données arrivent déjà triées par clé grâce à Hadoop.
 * Le reducer se contente d'émettre chaque nombre.
 */
public class SortReducer extends Reducer<IntWritable, IntWritable, IntWritable, NullWritable> {
    
    /**
     * Méthode reduce : émet chaque nombre dans l'ordre
     * 
     * @param key     Le nombre (clé triée)
     * @param values  Liste des valeurs pour cette clé
     * @param context Contexte pour émettre les résultats
     */
    @Override
    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) 
            throws IOException, InterruptedException {
        
        // Les données sont déjà triées par clé
        // On émet chaque occurrence du nombre
        for (IntWritable value : values) {
            // Émettre le nombre avec une clé null (on ne garde que la valeur)
            context.write(key, NullWritable.get());
            
            // Log pour debug
            System.out.println("REDUCE: Émission de " + key.get());
        }
    }
}
