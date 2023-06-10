import java.io.*;
import java.util.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.Reducer.Context;
import org.apache.hadoop.util.*;

public class partial {
    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {

        public void map(LongWritable key, Text value, OutputCollector<Text, Text> output, Reporter reporter) throws IOException {
            FileSplit fileSplit=(FileSplit) reporter.getInputSplit();
            String fileName = fileSplit.getPath().getName();

            String lastDigits = "";

            for (int i = fileName.length() - 1; i >= 0; i--) {
                char c = fileName.charAt(i);
                if (Character.isDigit(c)) {
                    lastDigits = c + lastDigits;
                } else {
                    break;
                }
            }

            String line = value.toString();
            StringTokenizer tokenizer = new StringTokenizer(line.toLowerCase());

            while (tokenizer.hasMoreTokens()) {

                String token = tokenizer.nextToken();
                output.collect(new Text(token), new Text(lastDigits));
            }
        }
    }
    public static class Reduce extends MapReduceBase implements
            Reducer<Text, Text, Text, Text> {
        public void reduce(Text key, Iterator<Text> value, OutputCollector<Text, Text> output,Reporter reporter)throws IOException{
            Set<String> uniqueFiles = new HashSet<String>();
            while(value.hasNext()){
                uniqueFiles.add(value.next().toString());
            }
            StringBuilder fileList = new StringBuilder();
            for (String file : uniqueFiles) {
                fileList.append(file).append(",");
            }
            fileList.deleteCharAt(fileList.length() - 1);
            output.collect(key, new Text(fileList.toString()));
        }
    }
    public static void main(String[] args) throws Exception {
        JobConf conf = new JobConf(partial.class);
        conf.setJobName("Partial");

        conf.setMapOutputKeyClass(Text.class);
        conf.setMapOutputValueClass(Text.class);

        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Text.class);

        conf.setMapperClass(Map.class);
        conf.setReducerClass(Reduce.class);

        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);
        FileInputFormat.setInputPaths(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));
        JobClient.runJob(conf);
    }
}
