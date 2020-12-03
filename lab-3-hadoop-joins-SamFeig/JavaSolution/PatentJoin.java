import java.io.IOException;
import java.util.*;

import java.lang.Integer;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import org.apache.hadoop.mapreduce.lib.chain.ChainMapper;
import org.apache.hadoop.mapreduce.lib.chain.ChainReducer;

public class PatentJoin {

    static public class Mapper1
            extends Mapper<Object, Text, LongWritable, Text> {
		
        private LongWritable mykey = new LongWritable();
        private Text myvalue = new Text();

        // "map" is called for each record (line)
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString();
            String[] words = line.split(",");

			//It is intermediate text data from Reducer1 run 1 
           if (words.length == 1) {
			   try {
				   //Split on whitespace as data has already been processed once
				   words = line.split("\\s");
				   mykey.set(Long.parseLong(words[0]));

				   String allButFirst = String.join(" ",
								Arrays.copyOfRange(words, 1, words.length)
						);
				   myvalue.set(allButFirst);
				   context.write(mykey, myvalue);
				} catch (java.lang.NumberFormatException e) {
                    // ignore this - bogus data
                    System.out.println("ERROR-3");
                }
		   } else if (words.length == 2) { //It is Citation data
                try {
                    mykey.set(Long.parseLong(words[0]));
                    myvalue.set(words[1]);
                    context.write(mykey, myvalue);
                } catch (java.lang.NumberFormatException e) {
                    // ignore this - bogus data
                    System.out.println("ERROR-1");
                }
            } else { //It is Patent data
                try {
                    mykey.set(Long.parseLong(words[0]));
                    String allButFirst = String.join(",",
                            Arrays.copyOfRange(words, 1, words.length)
                    );
                    myvalue.set(allButFirst);
                    context.write(mykey, myvalue);
                } catch (java.lang.NumberFormatException e) {
                    // ignore this - bogus data
                    System.out.println("ERROR-2");
                }
            }
        }
    };
    
    static public class Mapper2
            extends Mapper<Object, Text, LongWritable, Text> {
		
        private LongWritable mykey = new LongWritable();
        private Text myvalue = new Text();

        // "map" is called for each record (line)
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString();
            String[] words = line.split(",");
			
			//It is intermediate text data from Reducer1 run 2
            if (words.length == 1) {
				try {
				    words = line.split("\\s");
				    mykey.set(Long.parseLong(words[0]));
					//Check if patent states are equal and not empty
				    if(words[1].equals(words[3]) && !words[1].equals("\"\"")) {
					   myvalue.set("1");
					   context.write(mykey, myvalue);
				    }
			   } catch (java.lang.NumberFormatException e) {
				// ignore this - bogus data
				System.out.println("ERROR-3");
			   }
		   } else if (words.length == 2) { //It is Citation data
                try {
                    mykey.set(Long.parseLong(words[0]));
                    myvalue.set(words[1]);
                    context.write(mykey, myvalue);
                } catch (java.lang.NumberFormatException e) {
                    // ignore this - bogus data
                    System.out.println("ERROR-1");
                }
            } else { //It is Patent data
                try {
                    mykey.set(Long.parseLong(words[0]));
					String allButFirst = line.substring(line.indexOf(',')+1);					
                    myvalue.set(allButFirst);
                    context.write(mykey, myvalue);
                } catch (java.lang.NumberFormatException e) {
                    // ignore this - bogus data
                    System.out.println("ERROR-2");
                }
            }
        }
    };

    static public class Reducer1
            extends Reducer<LongWritable, Text, Text, Text> {
		
        private Text outkey = new Text();
        private Text outvalue = new Text();

        public void reduce(LongWritable key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
			
            String patentInfo = null;
            String patentState = "";

            ArrayList<String> citations = new ArrayList<String>();

            for (Text value : values) {
                String[] fields = value.toString().split(",");

				//If patent info, just store in variable and get patent state value
                if (fields.length > 2) {
                    patentInfo = value.toString();
                    try {
                        // The 4th field is 5th in the original data -- state of patent
                        patentState = fields[4];
                    } catch (java.lang.NumberFormatException e) {
                        // leave as -1 -- bogus data
                    }
                } else { //If Citation add to list
                    citations.add(value.toString());
                }
            }

            outkey.set(key.toString());
			
			//We might have citations for which we have no patent info...
            if (patentInfo != null) {
                for(String citation: citations) {
					outkey.set(citation);
					//System.out.println(outkey + " " + key + " " + patentState);
                    
					//flip key/value pair and add state to end
                    outvalue.set(key + " " + patentState); 
					context.write(outkey, outvalue);
                }
            }    
        }
    };
    
    static public class Reducer2
            extends Reducer<LongWritable, Text, Text, Text> {
		private Text outkey = new Text();
        private Text outvalue = new Text();
		
		public void reduce(LongWritable key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {
			
            String patentInfo = null;
            String patentState = "";

            ArrayList<String> citations = new ArrayList<String>();

			int sum = 0;
            for (Text value : values) {
                String[] fields = value.toString().split(",");
				
				//If patent info, just store in variable
                if (fields.length > 2) {
                    patentInfo = value.toString();
                } else { //If individual counts, sum them up
					sum += Long.parseLong(value.toString());
				}
				//If patent info exists, write out patent info with count appended to the end
				if (patentInfo != null) {
					outkey.set(key.toString() + "," + patentInfo + "," + sum);
				}	
			}
			context.write(outkey, outvalue);
		}
	};


    public static void main(String[] args) throws Exception {
		//Job 1 - Initial pass through citation & patent data
		//Return Cited Citing CitingState
        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf, "patent join");

        job.setJarByClass(PatentJoin.class);

        job.setMapperClass(Mapper1.class);
        job.setMapOutputKeyClass(LongWritable.class);
        job.setMapOutputValueClass(Text.class);

        //
        // We can not set a Combiner because we rely on having all
        // the information for the join
        //
        job.setReducerClass(Reducer1.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path("output-part-1"));
		
        job.waitForCompletion(true);
        
        
        //Job 2 - Second pass through Job1 output & patent data
		//Return Citing CitingState Cited CitedState
        Configuration conf2 = new Configuration();

        Job job2 = Job.getInstance(conf2, "patent join 2");

        job2.setJarByClass(PatentJoin.class);

        job2.setMapperClass(Mapper1.class);
        job2.setMapOutputKeyClass(LongWritable.class);
        job2.setMapOutputValueClass(Text.class);

        //
        // We can not set a Combiner because we rely on having all
        // the information for the join
        //
        job2.setReducerClass(Reducer1.class);
        job2.setOutputKeyClass(Text.class);
        job2.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job2, new Path(args[0] + "/apat63_99.txt"));
        FileInputFormat.addInputPath(job2, new Path("output-part-1/part-r-*"));
        FileOutputFormat.setOutputPath(job2, new Path("output-part-2"));
        
        job2.waitForCompletion(true);
        
		
        //Job 3 - Final pass through Job2 output & patent data
		//Return original patent info with count of same state cited patents appended to end
        Configuration conf3 = new Configuration();

        Job job3 = Job.getInstance(conf3, "patent join final");

        job3.setJarByClass(PatentJoin.class);

        job3.setMapperClass(Mapper2.class);
        job3.setMapOutputKeyClass(LongWritable.class);
        job3.setMapOutputValueClass(Text.class);

        //
        // We can not set a Combiner because we rely on having all
        // the information for the join
        //
        job3.setReducerClass(Reducer2.class);
        job3.setOutputKeyClass(Text.class);
        job3.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job3, new Path(args[0] + "/apat63_99.txt"));
		FileInputFormat.addInputPath(job3, new Path("output-part-2/part-r-*"));
        FileOutputFormat.setOutputPath(job3, new Path(args[1]));
		
        System.exit(job3.waitForCompletion(true) ? 0 : 1);
           
    }
}
