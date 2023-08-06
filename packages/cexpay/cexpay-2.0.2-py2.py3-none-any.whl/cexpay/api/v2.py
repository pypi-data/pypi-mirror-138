from datetime import datetime
import json
from typing import Optional
import requests
from urllib.parse import ParseResult, quote, urlencode, urlparse
import urllib3

from cexpay.api.security import SignatureCalculator

class Order:
	def __init__(self,
		order_id: str,
		client_order_id: str,
		status, state,
		from_currency: str, to_currency: str,
		from_amount: str, to_amount: str,
		from_account_id: str, to_account_id: str,
		deposit,
		instrument: str, client_order_tag: str = None
	) -> None:
		self.order_id = order_id
		self.client_order_id = client_order_id
		self.client_order_tag = client_order_tag
		self.status = status
		self.state = state
		self.instrument = instrument
		self.from_currency = from_currency
		self.from_amount = from_amount
		self.from_account_id = from_account_id
		self.to_currency = to_currency
		self.to_amount = to_amount
		self.to_account_id = to_account_id
		self.deposit = deposit

	@staticmethod
	def from_json(json_data):
		return Order(
			order_id = json_data["orderId"],
			client_order_id = json_data["clientOrderId"],
			client_order_tag = json_data["clientOrderTag"],
			status = json_data["status"],
			state = json_data["state"],
			instrument = json_data["instrument"],
			from_currency = json_data["from"]["currency"],
			from_amount = json_data["from"]["amount"],
			from_account_id = json_data["from"]["accountId"],
			to_currency = json_data["to"]["currency"],
			to_amount = json_data["to"]["amount"],
			to_account_id = json_data["to"]["accountId"],
			deposit=json_data["deposit"]
		)


class ApiV2:
	'''
	See https://developers.cexpay.io/processing-api/
	'''

	def __init__(self, key: str, passphrase: str, secret: str, url: str = "https://api.cexpay.io", ssl_ca_cert: str = None) -> None:
		self._key = key
		self._access_passphrase = passphrase
		self._signature_calculator = SignatureCalculator(secret)
		self._url = urlparse(url)
		self._ssl_ca_cert = ssl_ca_cert

	def order_create(self, client_order_id: str,
		from_currency: str, to_currency: str,
		from_amount = None, to_amount = None,
		from_account_id = None, to_account_id = None,
		instrument = None, client_order_tag = None
	) -> Order:
		payload = {
			"clientOrderId": client_order_id,
			"from": {"currency": from_currency},
			"to": {"currency": to_currency}
		}

		if instrument is not None:
			payload["instrument"] = instrument
		if client_order_tag is not None:
			payload["client_order_tag"] = client_order_tag
		if from_amount is not None:
			payload["from"]["amount"] = from_amount
		if to_amount is not None:
			payload["to"]["amount"] = to_amount
		if from_account_id is not None:
			payload["from"]["accountId"] = from_account_id
		if to_account_id is not None:
			payload["to"]["accountId"] = to_account_id

		response_data = self._do_post("/v2/order", payload)

		return Order.from_json(response_data)

	def order_fetch(self, order_id: str) -> Order:
		encoded_order_id = quote(order_id, safe="")

		response_data = self._do_get("/v2/order/" + encoded_order_id)

		return Order.from_json(response_data)

	def _parse_response(self, response: requests.Response, http_method: str, sign_url_part: str) -> dict:
		response_content_type = response.headers.get("Content-Type")

		if response.status_code >= 400:
			error_reason_phrase = response.headers["CP-REASON-PHRASE"]
			raise Exception("Unexpected response status. Reason: %s" % error_reason_phrase)

		if response_content_type != "application/json":
			raise Exception("Unexpected Content-Type: %s" % response_content_type)

		response_access_key = response.headers["CP-ACCESS-KEY"]
		if response_access_key is None:
			raise Exception("Unexpected response. CP-ACCESS-KEY was not provided. Attack?!")
		if self._key != response_access_key:
			raise Exception("Wrong response access key")

		response_timestamp = response.headers["CP-ACCESS-TIMESTAMP"]
		if response_timestamp is None:
			raise Exception("Unexpected response. CP-ACCESS-TIMESTAMP was not provided. Attack?!")

		response_signature = response.headers["CP-ACCESS-SIGN"]
		if response_signature is None:
			raise Exception("Unexpected response. CP-ACCESS-SIGN was not provided. Attack?!")

		response_data_raw = response.content

		response_expected_signature = self._signature_calculator.sing(response_timestamp, http_method, sign_url_part, response_data_raw)
		if response_signature != response_expected_signature:
			raise Exception("Wrong response signature")

		response_data = json.loads(response_data_raw)

		return response_data

	def _do_get(self, url_path: str, query_args: Optional[dict] = None) -> dict:
		query: Optional[str] = None
		if query_args is not None:
			query = urlencode(query_args, doseq=True)
		url: ParseResult = self._url._replace(
			path = url_path,
			query = query
		)
		timestamp: str = str(datetime.utcnow().timestamp()*1000)
		http_method = "GET"
		sign_url_part = url.path
		if url.query is not None and url.query != "":
			sign_url_part = url.path + "?" + url.query

		signature: str = self._signature_calculator.sing(timestamp, http_method, sign_url_part)

		response: requests.Response = requests.get(
			url.geturl(),
			headers = {
				"Content-Type": "application/json",
				"CP-ACCESS-KEY": self._key,
				"CP-ACCESS-TIMESTAMP": timestamp,
				"CP-ACCESS-PASSPHRASE": self._access_passphrase,
				"CP-ACCESS-SIGN": signature
			},
			verify = self._ssl_ca_cert
		)

		response_data: dict = self._parse_response(response, http_method, sign_url_part)
		
		return response_data

	def _do_post(self, url_path: str, payload: dict) -> dict:
		payload_raw: bytes = json.dumps(payload).encode("UTF-8")
		url: ParseResult = self._url._replace(
			path = url_path
		)
		timestamp: str = str(datetime.utcnow().timestamp()*1000)
		http_method = "POST"
		sign_url_part = url.path

		signature: str = self._signature_calculator.sing(timestamp, http_method, sign_url_part, payload_raw)

		response: requests.Response = requests.post(
			url.geturl(),
			headers = {
				"Content-Type": "application/json",
				"CP-ACCESS-KEY": self._key,
				"CP-ACCESS-TIMESTAMP": timestamp,
				"CP-ACCESS-PASSPHRASE": self._access_passphrase,
				"CP-ACCESS-SIGN": signature
			},
			data = payload_raw,
			verify = self._ssl_ca_cert
		)

		response_data: dict = self._parse_response(response, http_method, sign_url_part)
		
		return response_data
