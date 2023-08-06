# from kfputils.run import Runner, _display_run
from kfp import Client

# from os import environ, name
from os import environ


def get_kfp_client(namespace="kubeflow"):
    token = get_access_token()
    # inside cluster
    if token is not None:
        return Client(
            existing_token=token,
            namespace=namespace,
            host="http://ml-pipeline.kubeflow.svc.cluster.local:8888",
        )
    # outside cluster
    return Client(namespace=namespace)
    # return Client()


# def get_kfp_client_inside_cluster():
#     return Client(
#         existing_token=get_access_token(),
#         host="http://ml-pipeline.kubeflow.svc.cluster.local:8888",
#     )


def get_access_token():
    token = environ.get("KF_PIPELINES_SA_TOKEN_HARDCODED")
    if token is not None and token != "":
        print("hardcoded token used")
        return token

    token_path = environ.get("KF_PIPELINES_SA_TOKEN_PATH")
    if token_path is not None:
        with open(token_path) as f:
            return f.read()
