from logging import error, raiseExceptions
import pika
from threading import Thread

print("\nTRABALHO DE SDI - CHAT RABBITMQ")
print("Fernanda Maria de Souza")
print("---------------------------------\n")

user = raw_input("Nome do usuario: ")

connection = pika.BlockingConnection (pika.ConnectionParameters(host = 'localhost'))
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#        host='sdi-1',
#        credentials=pika.PlainCredentials(username="sdi", password="sdi")))

# CANAL DE SAIDA
channelSaida = connection.channel()
channelSaida.exchange_declare(exchange = 'fila_saida', exchange_type = 'fanout')

# CANAL DE ENTRADA
channelEntrada = connection.channel()
channelEntrada.exchange_declare(exchange = 'fila_entrada', exchange_type = 'fanout')

result = channelEntrada.queue_declare('', exclusive=True)
queue_name = result.method.queue
channelEntrada.queue_bind(exchange = 'fila_entrada', queue = queue_name)

 
def respostaCallback(ch, method, properties, body):

	mensagem = body.decode().split(">>", 2)

	if(str(mensagem[2]) != str(user)):
		nomeArquivo = str(user) + "-" + str(mensagem[2]) + ".client" + "-0" + str(mensagem[1])
		arquivo = open(nomeArquivo, "w")
		arquivo.write(mensagem[0])
		print("\nMensagem recebida de " + mensagem[2] + "!")
		print("\nQual arquivo voce deseja enviar mesmo?")


channelEntrada.basic_consume(respostaCallback, queue=queue_name, no_ack=True)


class ThreadOne(Thread):

	def __init__ (self, user_, channelSaida_):
		Thread.__init__(self)
		self.contMensagensEnviadas = 0
		self.user = user_
		self.channelSaida = channelSaida_

	def run(self):

		while(True):
			try:
				nomeArquivo = raw_input("\nNome do Arquivo a ser enviado como mensagem: ")
				arquivo = open(nomeArquivo, "r")
				mensagem = arquivo.read()
				self.contMensagensEnviadas += 1
				mensagem = str(mensagem) + ">>" + str(self.contMensagensEnviadas) + ">>" + str(self.user)
				self.channelSaida.basic_publish(exchange = 'fila_saida', routing_key = '', body = mensagem)
				print("Mensagem enviada!")
			except:
				raiseExceptions(error)


thingOne = ThreadOne(user, channelSaida)
thingOne.start()

channelEntrada.start_consuming()