# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_container.configuration import Configuration


class ContainerContainerDistribution(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'pulp_labels': 'object',
        'name': 'str',
        'content_guard': 'str',
        'base_path': 'str',
        'repository': 'str',
        'repository_version': 'str',
        'private': 'bool',
        'description': 'str'
    }

    attribute_map = {
        'pulp_labels': 'pulp_labels',
        'name': 'name',
        'content_guard': 'content_guard',
        'base_path': 'base_path',
        'repository': 'repository',
        'repository_version': 'repository_version',
        'private': 'private',
        'description': 'description'
    }

    def __init__(self, pulp_labels=None, name=None, content_guard=None, base_path=None, repository=None, repository_version=None, private=None, description=None, local_vars_configuration=None):  # noqa: E501
        """ContainerContainerDistribution - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_labels = None
        self._name = None
        self._content_guard = None
        self._base_path = None
        self._repository = None
        self._repository_version = None
        self._private = None
        self._description = None
        self.discriminator = None

        if pulp_labels is not None:
            self.pulp_labels = pulp_labels
        self.name = name
        if content_guard is not None:
            self.content_guard = content_guard
        self.base_path = base_path
        self.repository = repository
        self.repository_version = repository_version
        if private is not None:
            self.private = private
        self.description = description

    @property
    def pulp_labels(self):
        """Gets the pulp_labels of this ContainerContainerDistribution.  # noqa: E501


        :return: The pulp_labels of this ContainerContainerDistribution.  # noqa: E501
        :rtype: object
        """
        return self._pulp_labels

    @pulp_labels.setter
    def pulp_labels(self, pulp_labels):
        """Sets the pulp_labels of this ContainerContainerDistribution.


        :param pulp_labels: The pulp_labels of this ContainerContainerDistribution.  # noqa: E501
        :type: object
        """

        self._pulp_labels = pulp_labels

    @property
    def name(self):
        """Gets the name of this ContainerContainerDistribution.  # noqa: E501

        A unique name. Ex, `rawhide` and `stable`.  # noqa: E501

        :return: The name of this ContainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ContainerContainerDistribution.

        A unique name. Ex, `rawhide` and `stable`.  # noqa: E501

        :param name: The name of this ContainerContainerDistribution.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def content_guard(self):
        """Gets the content_guard of this ContainerContainerDistribution.  # noqa: E501

        An optional content-guard. If none is specified, a default one will be used.  # noqa: E501

        :return: The content_guard of this ContainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._content_guard

    @content_guard.setter
    def content_guard(self, content_guard):
        """Sets the content_guard of this ContainerContainerDistribution.

        An optional content-guard. If none is specified, a default one will be used.  # noqa: E501

        :param content_guard: The content_guard of this ContainerContainerDistribution.  # noqa: E501
        :type: str
        """

        self._content_guard = content_guard

    @property
    def base_path(self):
        """Gets the base_path of this ContainerContainerDistribution.  # noqa: E501

        The base (relative) path component of the published url. Avoid paths that                     overlap with other distribution base paths (e.g. \"foo\" and \"foo/bar\")  # noqa: E501

        :return: The base_path of this ContainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._base_path

    @base_path.setter
    def base_path(self, base_path):
        """Sets the base_path of this ContainerContainerDistribution.

        The base (relative) path component of the published url. Avoid paths that                     overlap with other distribution base paths (e.g. \"foo\" and \"foo/bar\")  # noqa: E501

        :param base_path: The base_path of this ContainerContainerDistribution.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and base_path is None:  # noqa: E501
            raise ValueError("Invalid value for `base_path`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                base_path is not None and len(base_path) < 1):
            raise ValueError("Invalid value for `base_path`, length must be greater than or equal to `1`")  # noqa: E501

        self._base_path = base_path

    @property
    def repository(self):
        """Gets the repository of this ContainerContainerDistribution.  # noqa: E501

        The latest RepositoryVersion for this Repository will be served.  # noqa: E501

        :return: The repository of this ContainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._repository

    @repository.setter
    def repository(self, repository):
        """Sets the repository of this ContainerContainerDistribution.

        The latest RepositoryVersion for this Repository will be served.  # noqa: E501

        :param repository: The repository of this ContainerContainerDistribution.  # noqa: E501
        :type: str
        """

        self._repository = repository

    @property
    def repository_version(self):
        """Gets the repository_version of this ContainerContainerDistribution.  # noqa: E501

        RepositoryVersion to be served  # noqa: E501

        :return: The repository_version of this ContainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._repository_version

    @repository_version.setter
    def repository_version(self, repository_version):
        """Sets the repository_version of this ContainerContainerDistribution.

        RepositoryVersion to be served  # noqa: E501

        :param repository_version: The repository_version of this ContainerContainerDistribution.  # noqa: E501
        :type: str
        """

        self._repository_version = repository_version

    @property
    def private(self):
        """Gets the private of this ContainerContainerDistribution.  # noqa: E501

        Restrict pull access to explicitly authorized users. Defaults to unrestricted pull access.  # noqa: E501

        :return: The private of this ContainerContainerDistribution.  # noqa: E501
        :rtype: bool
        """
        return self._private

    @private.setter
    def private(self, private):
        """Sets the private of this ContainerContainerDistribution.

        Restrict pull access to explicitly authorized users. Defaults to unrestricted pull access.  # noqa: E501

        :param private: The private of this ContainerContainerDistribution.  # noqa: E501
        :type: bool
        """

        self._private = private

    @property
    def description(self):
        """Gets the description of this ContainerContainerDistribution.  # noqa: E501

        An optional description.  # noqa: E501

        :return: The description of this ContainerContainerDistribution.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ContainerContainerDistribution.

        An optional description.  # noqa: E501

        :param description: The description of this ContainerContainerDistribution.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 1):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `1`")  # noqa: E501

        self._description = description

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ContainerContainerDistribution):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ContainerContainerDistribution):
            return True

        return self.to_dict() != other.to_dict()
