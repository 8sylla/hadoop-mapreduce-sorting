package src.main.java.hadoop.mapreduce.sorting;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/**
 * Job MapReduce pour trier un tableau de nombres
 * 
 * Utilisation:
 *   hadoop jar sorting.jar <input> <output>
 * 
 * Exemple:
 *   hadoop jar sorting.jar /user/root/input/numbers.txt /user/root/output
 */
public class SortingJob extends Configured implements Tool {
    
    @Override
    public int run(String[] args) throws Exception {
        
        // Vérifier les arguments
        if (args.length != 2) {
            System.err.println("Usage: SortingJob <input_path> <output_path>");
            System.err.println("Exemple: hadoop jar sorting.jar input/numbers.txt output");
            return -1;
        }
        
        // Configuration du job
        Configuration conf = getConf();
        Job job = Job.getInstance(conf, "MapReduce Sorting");
        
        // Classe principale
        job.setJarByClass(SortingJob.class);
        
        // Classes Mapper et Reducer
        job.setMapperClass(SortMapper.class);
        job.setReducerClass(SortReducer.class);
        
        // Types de sortie du Mapper
        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(IntWritable.class);
        
        // Types de sortie du Reducer
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(NullWritable.class);
        
        // Chemins d'entrée et de sortie
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
        // Nombre de reducers (1 pour un tri global)
        job.setNumReduceTasks(1);
        
        // Informations sur le job
        System.out.println("═══════════════════════════════════════════════════════");
        System.out.println("  Job MapReduce Sorting - Configuration");
        System.out.println("═══════════════════════════════════════════════════════");
        System.out.println("  Input  : " + args[0]);
        System.out.println("  Output : " + args[1]);
        System.out.println("  Mapper : SortMapper");
        System.out.println("  Reducer: SortReducer");
        System.out.println("  Reducers: 1 (tri global)");
        System.out.println("═══════════════════════════════════════════════════════");
        
        // Lancer le job et attendre la fin
        long startTime = System.currentTimeMillis();
        boolean success = job.waitForCompletion(true);
        long endTime = System.currentTimeMillis();
        
        // Afficher les statistiques
        if (success) {
            System.out.println("\n═══════════════════════════════════════════════════════");
            System.out.println("  ✅ Job terminé avec succès !");
            System.out.println("═══════════════════════════════════════════════════════");
            System.out.println("  Temps d'exécution: " + (endTime - startTime) / 1000.0 + " secondes");
            System.out.println("  Lignes invalides : " + job.getCounters()
                .findCounter("SortingJob", "INVALID_LINES").getValue());
            System.out.println("═══════════════════════════════════════════════════════");
        } else {
            System.err.println("\n❌ Job échoué !");
        }
        
        return success ? 0 : 1;
    }
    
    /**
     * Point d'entrée principal
     */
    public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new Configuration(), new SortingJob(), args);
        System.exit(exitCode);
    }
}
