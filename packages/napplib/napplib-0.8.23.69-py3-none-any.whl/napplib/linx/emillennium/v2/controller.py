import re
import requests
from requests.auth import HTTPBasicAuth
from dataclasses import dataclass
from datetime import datetime
from typing import Union, Tuple

from loguru import logger

from napplib.utils import AttemptRequests
from napplib.utils	import LoggerSettings

@logger.catch()
@dataclass
class EmillenniumController():
	endpoint_base: str
	username: str
	password: str
	debug: bool = False
	
	def __post_init__(self):
		level = 'INFO' if not self.debug else 'DEBUG'
		LoggerSettings(level=level)

		if not isinstance(self.username, str) or not self.username:
			raise TypeError(f'please enter a valid username. username: {self.username}')
		
		if not isinstance(self.password, str) or not self.password:
			raise TypeError(f'please enter a valid password. password: {self.password}')

		self.params = dict()
		
		self.headers = {
			'Content-Type'   : 'application/json',
			'Accept-Charset' : 'utf-8'
		}

		self.authentication = HTTPBasicAuth(self.username,self.password)

	@AttemptRequests(success_codes=[200], waiting_time=10)
	def get_products(self, showcase: str, change_date: Union[str, datetime] = None, trans_id: int = None) -> requests.Response:

		request_params = self.params.copy()
		if trans_id:
			request_params['trans_id'] = trans_id
		request_params['Vitrine'] = showcase
		request_params['Data_Atualizacao'] = change_date
		request_params['$top'] = 500
		request_params['$format'] = 'json'

		return requests.get(f'{self.endpoint_base}/api/millenium_eco/Produtos/ListaVitrine', params=request_params, headers=self.headers, auth=self.authentication)

	@AttemptRequests(success_codes=[200], waiting_time=10)
	def get_stocks(self, showcase: str, change_date: Union[str, datetime] = None, trans_id: int = None) -> requests.Response:

		request_params = self.params.copy()
		if trans_id:
			request_params['trans_id'] = trans_id
		request_params['Vitrine'] = showcase
		request_params['data_atualizacao_inicial'] = change_date
		request_params['$top'] = 500
		request_params['$format'] = 'json'
		
		return requests.get(f'{self.endpoint_base}/api/millenium_eco/Produtos/SaldoDeEstoque', params=request_params, headers=self.headers, auth=self.authentication)

	@AttemptRequests(success_codes=[200], waiting_time=10)
	def get_prices(self, showcase: str, change_date: Union[str, datetime] = None, trans_id: int = None) -> requests.Response:

		request_params = self.params.copy()
		if trans_id:
			request_params['trans_id'] = trans_id
		request_params['Vitrine'] = showcase
		request_params['data_atualizacao_inicial'] = change_date
		request_params['$top'] = 500
		request_params['$format'] = 'json'
		
		return requests.get(f'{self.endpoint_base}/api/millenium_eco/Produtos/PrecoDeTabela', params=request_params, headers=self.headers, auth=self.authentication)