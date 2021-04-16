import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#        host='sdi-1',
#        credentials=pika.PlainCredentials(username="sdi", password="sdi")))

channelEnvioMensagens = connection.channel()
channelEnvioMensagens.exchange_declare(exchange = 'fila_entrada', exchange_type = 'fanout')

channelRecebimentoMensagens = connection.channel()
channelRecebimentoMensagens.exchange_declare(exchange = 'fila_saida', exchange_type = 'fanout')

result = channelRecebimentoMensagens.queue_declare('', exclusive=True)
queue_name = result.method.queue
channelRecebimentoMensagens.queue_bind(exchange='fila_saida', queue=queue_name)

def callback(ch, method, properties, body):
	texto 		= body.decode().split(">>", 2)
	nomeArquivo = str(texto[2]) + "-0" + str(texto[1]) + ".serv"
	arquivo 	= open(nomeArquivo, 'w')
	arquivo.write(texto[0])
	
	print("O usuario " + texto[2] + " enviou um arquivo!")
	channelEnvioMensagens.basic_publish(exchange = 'fila_entrada', routing_key = '', body = body)

channelRecebimentoMensagens.basic_consume(callback, queue = queue_name, no_ack = True)

channelRecebimentoMensagens.start_consuming()