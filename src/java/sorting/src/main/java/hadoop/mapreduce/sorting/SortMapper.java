package src.main.java.hadoop.mapreduce.sorting;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * Mapper pour le tri distribué de nombres
 * 
 * Input:  (offset, "nombre")
 * Output: (nombre, nombre)
 * 
 * La clé et la valeur sont identiques pour permettre le tri automatique
 * par Hadoop lors de la phase Shuffle & Sort
 */
public class SortMapper extends Mapper<LongWritable, Text, IntWritable, IntWritable> {
    
    private IntWritable number = new IntWritable();

    /**
     * Méthode map : transforme chaque ligne en paire (nombre, nombre)
     * 
     * @param key     Offset de la ligne dans le fichier (ignoré)
     * @param value   Ligne contenant un nombre
     * @param context Contexte pour émettre les paires clé-valeur
     */
    @Override
    public void map(LongWritable key, Text value, Context context) 
            throws IOException, InterruptedException {
        
        String line = value.toString().trim();
        
        // Ignorer les lignes vides
        if (line.isEmpty()) {
            return;
        }
        
        try {
            // Parser le nombre
            int num = Integer.parseInt(line);
            
            // Émettre la paire (nombre, nombre)
            number.set(num);
            context.write(number, number);
            
            // Log pour debug (visible dans les logs YARN)
            System.out.println("MAP: " + num + " -> (" + num + ", " + num + ")");
            
        } catch (NumberFormatException e) {
            // Ignorer les lignes non numériques
            System.err.println("AVERTISSEMENT: Ligne ignorée (non numérique): " + line);
            context.getCounter("SortingJob", "INVALID_LINES").increment(1);
        }
    }
}
