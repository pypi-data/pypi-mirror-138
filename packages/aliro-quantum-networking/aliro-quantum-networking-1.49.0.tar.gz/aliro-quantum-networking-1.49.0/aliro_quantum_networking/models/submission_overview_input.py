# coding: utf-8

"""
    Aliro Q.Network

    This is an api for the Aliro Q.Network  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from aliro_quantum_networking.configuration import Configuration


class SubmissionOverviewInput(object):
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
        'name': 'str',
        'runs': 'int',
        'timeout': 'int',
        'timeline_stop_time': 'float',
        'submission_overview_type': 'str'
    }

    attribute_map = {
        'name': 'name',
        'runs': 'runs',
        'timeout': 'timeout',
        'timeline_stop_time': 'timelineStopTime',
        'submission_overview_type': 'submissionOverviewType'
    }

    def __init__(self, name=None, runs=1, timeout=10, timeline_stop_time=1000000000000, submission_overview_type=None, local_vars_configuration=None):  # noqa: E501
        """SubmissionOverviewInput - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._runs = None
        self._timeout = None
        self._timeline_stop_time = None
        self._submission_overview_type = None
        self.discriminator = None

        self.name = name
        if runs is not None:
            self.runs = runs
        if timeout is not None:
            self.timeout = timeout
        if timeline_stop_time is not None:
            self.timeline_stop_time = timeline_stop_time
        self.submission_overview_type = submission_overview_type

    @property
    def name(self):
        """Gets the name of this SubmissionOverviewInput.  # noqa: E501


        :return: The name of this SubmissionOverviewInput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SubmissionOverviewInput.


        :param name: The name of this SubmissionOverviewInput.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def runs(self):
        """Gets the runs of this SubmissionOverviewInput.  # noqa: E501

        Number of times simulation will be run  # noqa: E501

        :return: The runs of this SubmissionOverviewInput.  # noqa: E501
        :rtype: int
        """
        return self._runs

    @runs.setter
    def runs(self, runs):
        """Sets the runs of this SubmissionOverviewInput.

        Number of times simulation will be run  # noqa: E501

        :param runs: The runs of this SubmissionOverviewInput.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                runs is not None and runs > 100):  # noqa: E501
            raise ValueError("Invalid value for `runs`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                runs is not None and runs < 1):  # noqa: E501
            raise ValueError("Invalid value for `runs`, must be a value greater than or equal to `1`")  # noqa: E501

        self._runs = runs

    @property
    def timeout(self):
        """Gets the timeout of this SubmissionOverviewInput.  # noqa: E501

        Maximum time simulation will run, in minutes (default is 10)  # noqa: E501

        :return: The timeout of this SubmissionOverviewInput.  # noqa: E501
        :rtype: int
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Sets the timeout of this SubmissionOverviewInput.

        Maximum time simulation will run, in minutes (default is 10)  # noqa: E501

        :param timeout: The timeout of this SubmissionOverviewInput.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                timeout is not None and timeout > 360):  # noqa: E501
            raise ValueError("Invalid value for `timeout`, must be a value less than or equal to `360`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                timeout is not None and timeout < 1):  # noqa: E501
            raise ValueError("Invalid value for `timeout`, must be a value greater than or equal to `1`")  # noqa: E501

        self._timeout = timeout

    @property
    def timeline_stop_time(self):
        """Gets the timeline_stop_time of this SubmissionOverviewInput.  # noqa: E501

        The end time of the simulation, in picoseconds  # noqa: E501

        :return: The timeline_stop_time of this SubmissionOverviewInput.  # noqa: E501
        :rtype: float
        """
        return self._timeline_stop_time

    @timeline_stop_time.setter
    def timeline_stop_time(self, timeline_stop_time):
        """Sets the timeline_stop_time of this SubmissionOverviewInput.

        The end time of the simulation, in picoseconds  # noqa: E501

        :param timeline_stop_time: The timeline_stop_time of this SubmissionOverviewInput.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                timeline_stop_time is not None and timeline_stop_time < 0):  # noqa: E501
            raise ValueError("Invalid value for `timeline_stop_time`, must be a value greater than or equal to `0`")  # noqa: E501

        self._timeline_stop_time = timeline_stop_time

    @property
    def submission_overview_type(self):
        """Gets the submission_overview_type of this SubmissionOverviewInput.  # noqa: E501

        Must be \"SubmissionOverviewInput\"  # noqa: E501

        :return: The submission_overview_type of this SubmissionOverviewInput.  # noqa: E501
        :rtype: str
        """
        return self._submission_overview_type

    @submission_overview_type.setter
    def submission_overview_type(self, submission_overview_type):
        """Sets the submission_overview_type of this SubmissionOverviewInput.

        Must be \"SubmissionOverviewInput\"  # noqa: E501

        :param submission_overview_type: The submission_overview_type of this SubmissionOverviewInput.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and submission_overview_type is None:  # noqa: E501
            raise ValueError("Invalid value for `submission_overview_type`, must not be `None`")  # noqa: E501

        self._submission_overview_type = submission_overview_type

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
        if not isinstance(other, SubmissionOverviewInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SubmissionOverviewInput):
            return True

        return self.to_dict() != other.to_dict()
