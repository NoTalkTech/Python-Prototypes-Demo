#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Kafka Consumer
import json
import sys
import time

from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import OffsetAndMetadata
from kafka import TopicPartition
from kafka.errors import KafkaError

reload(sys)
sys.setdefaultencoding("utf-8")

msg_offsets = {}


class UdfProducer:
    """Producer Module"""

    def __init__(self, kafkahost, kafkaport, kafkatopic, msgkey):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkaTopic = kafkatopic
        self.key = msgkey
        print("producer:h,p,t,k", kafkahost, kafkaport, kafkatopic, msgkey)
        bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort
        )
        print("boot svr:", bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params, ensure_ascii=False)
            producer = self.producer
            print(parmas_message)
            v = parmas_message.encode('utf-8')
            k = key.encode('utf-8')
            print("send msg:(k,v)", k, v)
            producer.send(self.kafkaTopic, key=k, value=v)
            producer.flush()
        except KafkaError as e:
            print (e)


class UdfConsumer:
    """Consumer Module"""

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkaTopic = kafkatopic
        self.groupId = groupid
        self.key = key
        self.consumer = KafkaConsumer(self.kafkaTopic, group_id=self.groupId,
                                      bootstrap_servers='{kafka_host}:{kafka_port}'.format(
                                          kafka_host=self.kafkaHost,
                                          kafka_port=self.kafkaPort)
                                      )

    def consume_message(self):
        try:
            for p in self.consumer.partitions_for_topic(self.kafkaTopic):
                print ("[Topic %s, Partition %s] Offset = %s" % (self.kafkaTopic,
                                                                 p,
                                                                 self.consumer.committed(
                                                                     TopicPartition(self.kafkaTopic, p))))
            for msg in self.consumer:
                yield msg
        except KeyboardInterrupt as e:
            print e
        finally:
            print "Finally close consumer and autocommit offsets."
            self.consumer.commit_async(msg_offsets)


KAFKA_HOST = "localhost"
KAFKA_PORT = 9092
KAFKA_TOPIC = "test_hby"


def main(x_type, group, key=None):
    """Producer test"""
    if x_type == 'p':
        producer = UdfProducer(KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC, key)
        print ("===========> producer:", producer)
        for _id in range(100):
            params = '{"消息" : "%s"}' % str(_id)
            # 这种方式会将引号都打上\,可以直接用python对象
            # params = [{"消息0": _id}, {"消息1": _id}]
            producer.sendjsondata(params)
            time.sleep(1)

    """Consumer Test"""
    if x_type == 'c':
        msg_offsets = {}
        consumer_client = UdfConsumer(KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC, group)
        print ("========> consumer: ", consumer_client)
        messages = consumer_client.consume_message()
        for msg in messages:
            print ("msg-------->k,v", msg.key, msg.value)
            # print("offset------>p,o", msg.partition, msg.offset)
            if TopicPartition(KAFKA_TOPIC, msg.partition) in msg_offsets:
                msg_offsets[TopicPartition(KAFKA_TOPIC, msg.partition)] = OffsetAndMetadata(msg.offset, None)
            else:
                msg_offsets[TopicPartition(KAFKA_TOPIC, msg.partition)] = OffsetAndMetadata(msg.offset, None)

            for k in msg_offsets:
                print 'Partition: %s, Offset: %s' % (k, msg_offsets[k])

                # res = consumer_client.consumer.commit_async(msg_offsets)
                # print ("commit offset async: %s, %s" % (res.is_done, res.value))


if __name__ == '__main__':
    x_type = sys.argv[1]
    group = sys.argv[2]
    key = sys.argv[3]
    # print x_type, group, key
    # main('p', group, key)
    main(x_type, group, key)
