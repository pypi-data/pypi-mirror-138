import asyncio
import inspect
import uuid

from .transceiver import Transceiver, TransceiverManager

async def async_dummy():
	pass

class Pool:
	def __init__(self, name, timeout=30, is_async=False):
		"""
		Create a pool with the given unique name and timeout.
		timeout is the number of seconds after which a pool will
		automatically close without activity (not yet implemented).
		"""
		self._name = name
		self._conns = {}
		self._closed = False
		self._async = is_async

		# TODO: IMPLEMENT!
		self.timeout = timeout

	def get_peer_ids(self):
		"""
		Returns a tuple of the IDs of all connected peers.
		"""
		return tuple(self._conns.keys())

	@property
	def name(self):
		return self._name

	@property
	def closed(self):
		return self._closed

	def allows(self, endpoint):
		"""
		A method which returns a boolean
		value telling whether the given
		endpoint is allowed to join this
		pool. Subclasses may return False
		in some cases, blocking certain
		endpoints from joining.
		"""
		return not self.closed

	def get_connection(self, test):
		"""
		If test is a string, gets a connection by its ID.
		If test is a Transceiver, gets the connection associated with it.
		If no connection is found, None is returned.
		"""
		if isinstance(test, str):
			return self._conns.get(test, None)
		elif isinstance(test, Transceiver):
			for i in self._conns.values():
				if i['socket'] == test:
					return i
			return None
		else:
			raise TypeError("get_connection accepts a UUID string or a Transceiver.")

	def add_endpoint(self, transceiver):
		"""
		Accepts a Transceiver and adds it to the pool
		as an endpoint.
		"""
		if transceiver in self:
			raise ValueError("This endpoint has already been added!")

		if self.allows(transceiver):
			peers = self.get_peer_ids()

			ent = {
				'socket': transceiver,
				'id': str(uuid.uuid4()),
				'description': None
			}

			self._conns[ent['id']] = ent
			transceiver.id = ent['id']

			yield (transceiver, 'rtc:joined', {
				'client_id': ent['id'],
				'peers': peers,
				'descriptions': dict(map(lambda entry: (entry['id'], entry['description']), self._conns.values())),
				'pool': self.name
			})

			yield from map(lambda conn: (conn['socket'], 'rtc:request_offers', {
				'for': transceiver.id
			}), filter(lambda conn: conn['id'] != transceiver.id, self._conns.values()))

		else:
			yield (transceiver, 'rtc:error', {
				'message': 'Could not join pool.'
			})

	def update(self):
		"""
		Prunes closed connections and notifies peers of the closure.
		"""
		if self.closed: return

		# remove closed transceivers,
		# send close notifications to peers
		pre_load = tuple(self._conns.values())
		closed = []
		for conn in pre_load:
			if not conn['socket'].is_open():
				closed.append(conn['id'])
				del self._conns[conn['id']]

		futs = []
		for c in closed:
			futs.append(self.broadcast('rtc:close', { 'uid': c }))

		if self._async:
			return asyncio.gather(*futs)

	def describe(self, id_or_trans, desc):
		"""
		Sets the description of the specified connection.
		"""
		if self.closed:
			raise ValueError("Pool is closed")

		assert desc is None or isinstance(desc, dict)
		conn = self.get_connection(id_or_trans)
		if conn:
			conn['description'] = desc
			return self.broadcast('rtc:describe', {
				'description': desc,
				'uid': conn['id']
			})
		else:
			raise ValueError(f"No connection associated with {id_or_trans}")

	def broadcast(self, evt_type, evt_data, *exclude):
		"""
		Broadcasts the specified event to all connections in the pool,
		except for those whose Transceiver is in ``exclude``.
		"""
		if self.closed:
			raise ValueError("Pool is closed")

		res = []
		for conn in filter(lambda ent: ent['socket'] not in exclude, self._conns.values()):
			res.append(conn['socket'].send(evt_type, evt_data))

		if self._async:
			return asyncio.gather(*res)

	def close(self):
		"""
		Sends a signal to close all connections in the pool,
		and closes the signalling channels.
		"""

		if self.closed:
			raise ValueError("Pool is closed")

		if self._async:
			return self._close_async()
		else:
			self.broadcast('rtc:stop', {})
			for conn in self._conns.values():
				conn['socket'].close()

			self._conns.clear()
			self._closed = True

	async def _close_async(self):
		await self.broadcast('rtc:stop', {})
		await asyncio.gather(*map(lambda conn: conn['socket'].close(), self._conns.values()))

		self._conns.clear()
		self._closed = True

	def __contains__(self, test):
		if isinstance(test, str):
			# check by UID
			return test in self._conns.keys()
		elif isinstance(test, Transceiver):
			return test in map(lambda ent: ent['socket'], self._conns.values())
		else:
			return False

def _flatten(two_deep_gen):
	for gen in two_deep_gen:
		if gen is not None:
			yield from gen

class PoolManager:
	def __init__(self, private=True, is_async=False):
		self._private = private
		self._pools = []
		self._trans = TransceiverManager(is_async=is_async)

		self._async = is_async
		self._closed = False

	def close(self):
		"""
		Closes this pool manager.
		"""
		self._trans.close_all()
		self._closed = True

	def _close_assert(self, msg="PoolManager is closed"):
		assert not self._closed, msg

	def update(self):
		self._close_assert()
		if self._async:
			return self._update_async()
		else:
			for event, source in self._trans.events():
				messages = self.handle_event(event, source)
				self._sendall(messages)

			self.cleanup()

	async def _update_async(self):
		futs = []
		async for event, source in self._trans.events():
			messages = self.handle_event(event, source)
			futs.extend(self._sendall(messages))

		await asyncio.gather(*futs)
		await self.cleanup()

	def _sendall(self, messages):
		futs = []
		for message in messages:
			futs.append(message[0].send(*message[1:]))
		return futs

	def cleanup(self):
		immut = tuple(self._pools)
		futs = []
		for pool in immut:
			if pool.closed:
				self._pools.remove(pool)
			else:
				futs.append(pool.update())

		if self._async:
			return asyncio.gather(*futs)

	def add_endpoint(self, transceiver):
		self._close_assert()

		if transceiver.is_async and not self._async:
			raise ValueError("Cannot add asynchronous transceiver to non-async PoolManager")
		elif not transceiver.is_async and self._async:
			# TODO: 'asyncify'
			raise ValueError("Cannot add non-async transceiver to async PoolManager")

		self._trans.dispatch(transceiver)

	def add_pool(self, pool):
		self._close_assert()
		if pool.name in map(lambda pool: pool.name, self._pools):
			raise ValueError(f"Pool with name '{pool.name}' already exists!")
		else:
			self._pools.append(pool)

	def get_pool(self, name):
		for pool in self._pools:
			if pool.name == name: return pool

		return None

	def remove_pool(self, name):
		self._close_assert()
		pool = self.get_pool(name)
		if pool is not None:
			self._pools.remove(pool)
			return True
		else:
			return False

	def _query(self, test):
		for pool in self._pools:
			conn = pool.get_connection(test)
			if conn:
				return pool, conn

		return None, None

	def get_pool_for(self, test):
		return self._query(test)[0]

	def get_connection_for(self, test):
		return self._query(test)[1]

	def handle_event(self, event, source):
		"""
		:param: event
		:type event: tuple
		:param source:
		:type source: Transceiver
		"""

		self._close_assert()

		messages = ()

		name, data = event
		parts = name.split(':')
		prefix = parts[0]
		if prefix != 'rtc' or len(parts) != 2:
			# Ignore events not intended for the rtc
			# signalling process. This allows a single
			# websocket to be used for RTC signalling
			# as well as other applications.
			return messages

		action = parts[1]
		if action == 'join':
			_pool = data.get('pool', None)
			if not _pool:
				return (source, 'rtc:error', {
					'message': 'Please specify a pool to join.'
				})
			pool = self.get_pool(_pool)

			if pool:
				messages = pool.add_endpoint(source)
			else:
				if self._private:
					# pools cannot be created implicitly,
					# must be explicitly created by server code
					return (source, 'rtc:error', {
						'message': 'No such pool exists.',
						'pool': _pool
					})
				else:
					# auto-add default pool
					pool = Pool(_pool, is_async=self._async)
					self.add_pool(pool)
					messages = pool.add_endpoint(source)

		elif action == 'offers':
			local_offer = []
			for key in data.keys():
				pool, conn = self._query(key)
				if conn:
					local_offer.append((conn['socket'], 'rtc:offer', {
						'for': source.id,
						'offer': data[key]
					}))

			messages = iter(local_offer)
		elif action == 'answer':
			target = data.get('for', None)
			if target:
				conn = self.get_connection_for(target)
				if conn:
					messages = ((conn['socket'], 'rtc:answer', {
						'for': source.id,
						'answer': data.get('answer')
					}),)
			else:
				messages = ((source, 'rtc:error', {
					'message': 'Please specify an answer target.'
				}),)
		elif action == 'candidate':
			target = data.get('for', None)
			if target:
				conn = self.get_connection_for(target)
				if conn:
					messages = ((conn['socket'], 'rtc:candidate', {
						'candidate': data.get('candidate'),
						'from': source.id
					}),)
			else:
				messages = ((source, 'rtc:error', {
					'message': "Please specify a candidate recipient in the 'for' field."
				}),)
		else:
			messages = ((source, 'rtc:error', {
				'message': f"RTC action '{action}' not recognized."
			}),)

		return messages