import configparser as ini

cfg = ini.ConfigParser()
cfg.read('C:\\QueroDelivery\\Config.ini')
SERVIDOR_DELIVERY = cfg.get('CONEXAO','Servidor')
SERVIDOR_CAMINHO  = cfg.get('CONEXAO','Caminho')
SERVIDOR_HOST  = cfg.get('CONEXAO','Host')
PLACE_ID       = cfg.get('QUERO DELIVERY','placeId')
HEAD           = cfg.get('QUERO DELIVERY','Head')
URL_SITE       = cfg.get('QUERO DELIVERY','url')
CATEGORIA      = cfg.get('QUERO DELIVERY','categoria')

