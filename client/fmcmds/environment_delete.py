from cliff.command import Command

import call_server as server


class EnvironmentDelete(Command):
    
    def get_parser(self, prog_name):
        parser = super(EnvironmentDelete, self).get_parser(prog_name)

        parser.add_argument(dest='env_name',
                            help="Environment name")

        # parser.add_argument('--force',
        #                    help="Force delete of the environment.")

        return parser

    def take_action(self, parsed_args):
        env_name = parsed_args.env_name

        force_flag = ''
        # if parsed_args.force:
        #    force_flag = 'true'
        server.TakeAction().delete_environment(env_name, force_flag=force_flag)
