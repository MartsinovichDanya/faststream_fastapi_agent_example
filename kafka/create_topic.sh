#!/bin/bash

# Скрипт для создания топика в Kafka
# Использование: ./create_topic.sh <topic_name>

# Проверяем, передан ли аргумент
if [ $# -eq 0 ]; then
    echo "Ошибка: Не указано имя топика"
    echo "Использование: $0 <topic_name>"
    exit 1
fi

# Получаем имя топика из первого аргумента
TOPIC_NAME="$1"

# Создаем топик с помощью docker-compose exec
echo "Создание топика '$TOPIC_NAME'..."
docker exec kafka_kafka-1_1 /opt/kafka/bin/kafka-topics.sh --create --topic "$TOPIC_NAME" --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# Проверяем результат выполнения команды
if [ $? -eq 0 ]; then
    echo "Топик '$TOPIC_NAME' успешно создан"
else
    echo "Ошибка при создании топика '$TOPIC_NAME'"
    exit 1
fi
