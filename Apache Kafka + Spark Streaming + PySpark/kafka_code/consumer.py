from kafka import KafkaConsumer

consumer = KafkaConsumer('test_step_1', bootstrap_servers=['localhost:9092'])
for msg in consumer:
    print(msg.value)