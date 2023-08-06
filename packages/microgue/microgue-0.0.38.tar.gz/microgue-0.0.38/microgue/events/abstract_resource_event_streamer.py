import boto3
import json
import logging
import uuid

logger = logging.getLogger('microgue')


class StreamFailed(Exception):
    pass


class AbstractResourceEventStreamer:
    stream = None
    stream_name = ''
    resource_id_field = 'id'

    def __init__(self):
        logger.debug(f"########## {self.__class__.__name__} __init__ ##########")
        logger.debug(f"AbstractResourceEventStreamer.stream: {AbstractResourceEventStreamer.stream}")
        if AbstractResourceEventStreamer.stream is None:
            logger.debug("connecting to kinesis")
            AbstractResourceEventStreamer.stream = boto3.client('kinesis')
        else:
            logger.debug("using existing connection to kinesis")

    def stream_create(self, resource_after):
        return self._stream('create', {}, resource_after)

    def stream_update(self, resource_before, resource_after):
        return self._stream('update', resource_before, resource_after)

    def stream_delete(self, resource_before):
        return self._stream('delete', resource_before, {})

    def _stream(self, event_type, resource_before={}, resource_after={}):
        logger.debug("########## {} Stream ##########".format(self.__class__.__name__))
        logger.debug("event_type: {}".format(event_type))
        logger.debug("before: {}".format(resource_before))
        logger.debug("after: {}".format(resource_after))
        partition_key = resource_after.get(self.resource_id_field) if resource_after.get(self.resource_id_field, None) is not None else resource_before.get(self.resource_id_field)
        data = {
            'id': str(uuid.uuid4()),
            'event_type': '{}.{}'.format(self.stream_name, event_type),
            'before': resource_before,
            'after': resource_after
        }

        try:
            self.stream.put_record(
                StreamName=self.stream_name,
                PartitionKey=partition_key,
                Data=json.dumps(data)
            )
        except Exception as e:
            logger.error("########## {} Error".format(self.__class__.__name__))
            logger.error("{}: {}".format(e.__class__.__name__, str(e)))
            raise StreamFailed(str(e))

        return True
