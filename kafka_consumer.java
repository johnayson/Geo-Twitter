import java.util.Properties;
import java.util.Arrays;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.Mongo;
import com.mongodb.MongoException;
import com.mongodb.util.JSON;

//Kafka consumer that listens live to the Stream
public class kafka_consumer {
   
   public static void insert_mongodb ( String database, String col,String record){
	
	Mongo mongo = new Mongo("localhost", 27017);
	//DB db = mongo.getDB("test");
	DB db = mongo.getDB(database);
	DBCollection collection = db.getCollection(col);	

	//DBCollection collection = db.getCollection("tweets_samp");
	//String json = "{'database' : 'mkyongDB','table' : 'hosting'," +
	//  "'detail' : {'records' : 99, 'index' : 'vps_index1', 'active' : 'true'}}}";

	DBObject dbObject = (DBObject)JSON.parse(record);

	collection.insert(dbObject);

	DBCursor cursorDocJSON = collection.find();
	System.out.println("Print values in collection: "); 
	while (cursorDocJSON.hasNext()) {
		System.out.println(cursorDocJSON.next());
	}
	
	System.out.println("End of Collection: ");
       	
   }


   public static void main(String[] args) throws Exception {
      //if(args.length == 0){
      //   System.out.println("Enter topic name");
      //   return;
      //}
      //Kafka consumer configuration settings
      //String topicName = args[0].toString();
      String topicName = "testing3";
      Properties props = new Properties();
      
      props.put("bootstrap.servers", "localhost:9092");
      props.put("group.id", "test");
      props.put("enable.auto.commit", "true");
      props.put("auto.commit.interval.ms", "1000");
      props.put("session.timeout.ms", "30000");
      props.put("key.deserializer", 
         "org.apache.kafka.common.serialization.StringDeserializer");
      props.put("value.deserializer", 
         "org.apache.kafka.common.serialization.StringDeserializer");
      KafkaConsumer<String, String> consumer = new KafkaConsumer
         <String, String>(props);
      
      //Kafka Consumer subscribes list of topics here.
      consumer.subscribe(Arrays.asList(topicName));
      
      //print the topic name
      System.out.println("Subscribed to topic " + topicName);
      int i = 0;
      while (true) {
         ConsumerRecords<String, String> records = consumer.poll(100);
         for (ConsumerRecord<String, String> record : records) {
         // print the offset,key and value for the consumer records.
         	System.out.printf("offset = %d, key = %s, value = %s\n", 
            	record.offset(), record.key(), record.value());
		insert_mongodb("test","tweets_samp",record.value());
	 }
      }
   }
}
