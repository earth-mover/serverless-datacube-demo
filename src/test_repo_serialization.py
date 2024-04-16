import logging
import pickle
import sys

import arraylake
import cloudpickle
from lithops.job.serialize import SerializeIndependent

logger = logging.getLogger("arraylake")
logger.setLevel(logging.DEBUG)
stderr_handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stderr_handler.setFormatter(formatter)
logger.addHandler(stderr_handler)


class CustomSerializingThing:
    def __init__(self):
        print("called init")

    def __getstate__(self):
        print("called getstate")
        return {}

    def __setstate__(self, state):
        print("called setstate")


if __name__ == "__main__":
    client = arraylake.Client()
    print("first open")
    repo = client.get_repo("earthmover-demos/sentinel-mosaic-South-America-v1")
    # repo = CustomSerializingThing()
    print("pickling")
    p = pickle.dumps(repo)
    print("unpickling")
    repo2 = pickle.loads(p)

    print("cloudpickling")
    p = cloudpickle.dumps(repo)
    print("uncloudpickling")
    repo2 = cloudpickle.loads(p)

    serialize = SerializeIndependent([])

    # print("getmembers")
    # list(inspect.getmembers_static(repo))
    # for k, v in inspect.getmembers_static(repo):
    # print(k)
    # inspect.isfunction(v) or (inspect.ismethod(v) and inspect.isfunction(v.__func__))
    print("serialize")
    serialize._module_inspect(repo)

    # class Dummy:
    #     def __call__(self, *arg, **kwargs):
    #         pass
    # print("serializing")
    # p = serialize([Dummy, repo], [], [])
