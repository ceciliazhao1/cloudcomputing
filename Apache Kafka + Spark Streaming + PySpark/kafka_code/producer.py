from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

producer.send('test_step_1', b'(1, Main Menu), (2, Phone) , (3, Smart Phone), (4, iPhone)')