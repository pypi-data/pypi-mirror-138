"""
Snowflake URI utility class that supports extraction of
Snowflake configuration data and method parameters from
Snowflake resource URIs.
"""
from __future__ import annotations
from urllib.parse import urlparse, parse_qs


class sfu:
    def __init__(self, uri: str):
        result = urlparse(uri)

        # Init all possible default values to None
        self.user = None
        self.password = None
        self.account = None
        self.database = None
        self.table = None

        if result.username is not None and result.username != '':
            self.user = result.username

        if result.password is not None and result.password != '':

            if ':' not in result.password:
                self.password = result.password
            else:
                (password, account) = result.password.split(':')
                self.password = password
                self.account = account

        if result.hostname is not None and result.hostname != '':
            self.database = result.hostname

        if result.path is not None and result.path != '':
            self.table = result.path.lstrip('/')

        q_result = parse_qs(urlparse(uri).query)

        # Pull values of q_result out of list structure
        for key in q_result.keys():
            # Only accept if list is of len 1
            if len(q_result[key]) == 1:
                q_result[key] = q_result[key][0]

        # Extract other default properties from q_result
        self.warehouse = q_result.pop('warehouse', None)
        self.schema = q_result.pop('schema', None)
        self.role = q_result.pop('role', None)

        # q_result should now only contain custom values
        self.custom_params = q_result.keys()

        # Extract remaining properties (custom values given by user)
        # so that they can be accessed by foo.<custom_parameter_name>
        self._extract_custom_properties(q_result)

    # Extract all custom values into properties

    def _extract_custom_properties(self, params: dict):
        for key in params.keys():
            setattr(self, key, params[key])

    # Get current values of all originally entered custom values
    def _get_custom_values(self) -> dict:
        custom_dict = {}

        for custom_key in self.custom_params:
            custom_dict[custom_key] = getattr(self, custom_key)

        return custom_dict

    # Given a list of property names, creates a dictionary with structure property_name: value
    # if value is not None. If safe is false, includes all custom values as well
    def _package_properties(self, property_list: list, safe: bool = True) -> dict:
        result = {}

        for key_val in property_list:
            att_val = getattr(self, key_val)
            if att_val is not None:
                result[key_val] = att_val

        if not safe:
            result.update(self._get_custom_values())

        return result

    def credentials(self, safe: bool = True) -> dict:
        """
        Extract configuration data (only credentials) from a URI

        :param safe: If true, only return standard properties that can be passed to snowflake.
            If false, returns custom values as well.

        :return: A dictionary with the following keys (if available):
            user, password, account
        """

        return self._package_properties(['user', 'password', 'account'], safe)

    def configuration(self, safe: bool = True) -> dict:
        """
        Extract configuration data (both credentials and non-credentials) from a URI

        :param safe: If true, only return standard properties that can be passed to snowflake.
            If false, returns custom values as well.

        :return: A dictionary with the following keys (if available):
            user, password, account, database, warehouse, schema, role
        """

        return self._package_properties(
            ['user', 'password', 'database', 'account', 'warehouse', 'schema', 'role'], safe)

    def for_connection(self, safe: bool = True) -> dict:
        """
        Extract all parameters for a connection constructor

        :param safe: If true, only return standard properties that can be passed to snowflake.
            If false, returns custom values as well.

        :return: A dictionary with the following keys (if available):
            user, password, account, database, warehouse, schema, role
        """
        return self.configuration(safe)

    def for_db(self) -> [str, None]:
        """
        Extract database name for a connection.cursor USE DATABASE <DB> command

        :return: Database name
        """

        return self.database

    def for_warehouse(self) -> [str, None]:
        """
        Extract warehouse name for a connection.cursor USE WAREHOUSE <WH> command

        :return: Warehouse name
        """

        return self.warehouse

    def for_table(self) -> [str, None]:
        """
        Extract table name for a connection.cursor SELECT <COLS> FROM <TABLE> command

        :return: Table name
        """

        return self.table

    def to_string(self) -> str:
        """
        Constructs a uri based off of current value of the properties of this object
        """

        new_uri = 'snow://'
        contains_user_info = False

        if self.user is not None:
            contains_user_info = True
            new_uri += self.user

        if self.password is not None:
            contains_user_info = True
            new_uri += ':' + self.password

        if self.account is not None:
            contains_user_info = True
            new_uri += ':' + self.account

        if self.database is not None:
            # Include @ iff there was user info included
            if contains_user_info:
                new_uri += '@'

            new_uri += self.database

            # Can only have a table if a db is specified
            if self.table is not None:
                new_uri += '/' + self.table

        # Add in all parameters and custom values
        parameters = self._package_properties(
            ['warehouse', 'schema', 'role'], False)

        first_param = True
        for key in parameters:
            if first_param:
                new_uri += '?'
                first_param = False
            else:
                new_uri += '&'

            new_uri += key + '=' + parameters[key]

        return new_uri
