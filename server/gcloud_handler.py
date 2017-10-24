import ast
from os.path import expanduser

from stevedore import extension

from common import fm_logger
from dbmodule.objects import environment as env_db

home_dir = expanduser("~")

APP_AND_ENV_STORE_PATH = ("{home_dir}/.cld/data/deployments/").format(home_dir=home_dir)

fmlogger = fm_logger.Logging()


class GCloudHandler(object):

    res_mgr = extension.ExtensionManager(
        namespace='server.server_plugins.gcloud.resource',
        invoke_on_load=True,
    )

    coe_mgr = extension.ExtensionManager(
        namespace='server.server_plugins.gcloud.coe',
        invoke_on_load=True,
    )

    def _get_coe_type(self, env_id):
        coe_type = ''
        env_obj = env_db.Environment().get(env_id)
        env_definition = ast.literal_eval(env_obj.env_definition)
        env_details = env_definition['environment']
        coe_type = env_details['app_deployment']['type']
        return coe_type

    def create_resources(self, env_id, resource_list):
        fmlogger.debug("GCloudHandler create_resources")
        resource_details = ''
        ret_status_list = []

        for resource_defs in resource_list:
            resource_details = resource_defs['resource']
            type = resource_details['type']
            env_db.Environment().update(env_id, {'status': 'creating_' + type})

            for name, ext in GCloudHandler.res_mgr.items():
                if name == type:
                    status = ext.obj.create(env_id, resource_details)
                    if status: ret_status_list.append(status)

        return ret_status_list

    def delete_resource(self, env_id, resource):
        fmlogger.debug("GCloudHandler delete_resource")
        type = resource.type
        env_db.Environment().update(env_id, {'status': 'deleting_' + type})
        for name, ext in GCloudHandler.res_mgr.items():
            if name == type:
                ext.obj.delete(resource)

    def create_cluster(self, env_id, env_info):
        coe_type = self._get_coe_type(env_id)
        for name, ext in GCloudHandler.coe_mgr.items():
            if name == coe_type:
                status = ext.obj.create_cluster(env_id, env_info)
                return status