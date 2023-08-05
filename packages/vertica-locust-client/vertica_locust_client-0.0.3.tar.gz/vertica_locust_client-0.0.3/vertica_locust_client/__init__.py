from .client import VerticaClient
from .user import VerticaUser
from locust import events


@events.init_command_line_parser.add_listener
def _(parser):
    """Add command line arguments to locust that are Verica specific"""
    parser.add_argument("--user",
                        type=str,
                        env_var="VERTICA_USER",
                        default="dbadmin",
                        help="ID of user to connect to Vertica with")
    parser.add_argument("--password",
                        type=str,
                        env_var="VERTICA_PASSWORD",
                        default="",
                        help="Password of the Vertica user ID")
    parser.add_argument("--carbon-endpoint",
                        type=str,
                        env_var="CARBON_ENDPOINT",
                        default="",
                        help="Server location of the carbon stats collector.  "
                            "This is a plaintext endpoint.  Location can include "
                            "the port number if something other than 2003 is used.")
    parser.add_argument("--carbon-namespace",
                        type=str,
                        env_var="CARBON_NAMESPACE",
                        default="locust",
                        help="The namespace for the carbon metric.  This is treated as "
                             "the prefix when constructing the full metric name")