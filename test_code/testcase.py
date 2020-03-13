import logging
import json
import time
from util import run_cmd, configure_log

LOG = configure_log(logging.DEBUG, __name__, "console.log")

class TestRemoveSubstrate:
	def test_create_substrate_container_destroy(self, image):
		"""
		This test method does the following things
			- Remove the docker container if it already exists
			- Create a docker container based on the image
			- Keep checking for block number for the substrate
			- Destroy the container if block number exceeds 10
		:return:
		"""
		# All the commands needed to be run
		docker_create = "docker run -itd --name parity --net host %s --dev" % image
		rm = "docker rm -f parity"
		check_block_num = 'curl  -H "Content-Type: application/json" -d \'{"id":1, "jsonrpc":"2.0", "method": "chain_getBlock"}\' localhost:9933'

		# Create the docker container
		LOG.info("-We are creating substrate docker container from parity ")
		LOG.info("Remove if container already exists")
		out, rc = run_cmd(rm)
		LOG.info("Create substrate container")
		out, rc = run_cmd(docker_create)
		assert rc == 0, "creating docker substrate container failed"

		# Check the block number periodically, if it exceeds 10 then remove docker container
		time.sleep(5) # calibration time
		LOG.info("Checking for block number and deleting container if it exceeds 10")
		out, rc = run_cmd(check_block_num)
		assert rc == 0, "getting block number failed %s" % out
		block_num = int(json.loads(out)['result']['block']['header']['number'], 16)
		while block_num <= 10:
			out, rc = run_cmd(check_block_num)
			assert rc == 0, "getting block number failed"
			block_num = int(json.loads(out)['result']['block']['header']['number'], 16)
			LOG.info("Block Number: %d" % block_num)
			time.sleep(2)
		LOG.info("Removing substrate docker container as now block_num exceeds 10")
		out, rc = run_cmd(rm)
		assert rc == 0, "Removal of docker container failed after exceeding 10 blocks"
