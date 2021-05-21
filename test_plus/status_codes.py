class StatusCodeAssertionMixin(object):
    """
    The following `assert_http_###_status_name` methods were intentionally added statically instead of dynamically so
    that code completion in IDEs like PyCharm would work. It is preferred to use these methods over the response_XXX
    methods, which could be deprecated at some point. The assert methods contain both the number and the status name
    slug so that people that remember them best by their numeric code and people that remember best by their name will
    be able to easily find the assertion they need. This was also directly patterned off of what the `Django Rest
    Framework uses <https://github.com/encode/django-rest-framework/blob/main/rest_framework/status.py>`_.
    """

    def _assert_http_status(self, status_code, response=None, msg=None, url=None):
        response = self._which_response(response)
        self.assertEqual(response.status_code, status_code, msg)
        if url is not None:
            self.assertEqual(response.url, url)

    def assert_http_100_continue(self, response=None, msg=None):
        self._assert_http_status(100, response=response, msg=msg)

    def assert_http_101_switching_protocols(self, response=None, msg=None):
        self._assert_http_status(101, response=response, msg=msg)

    def assert_http_200_ok(self, response=None, msg=None):
        self._assert_http_status(200, response=response, msg=msg)

    def assert_http_201_created(self, response=None, msg=None):
        self._assert_http_status(201, response=response, msg=msg)

    def assert_http_202_accepted(self, response=None, msg=None):
        self._assert_http_status(202, response=response, msg=msg)

    def assert_http_203_non_authoritative_information(self, response=None, msg=None):
        self._assert_http_status(203, response=response, msg=msg)

    def assert_http_204_no_content(self, response=None, msg=None):
        self._assert_http_status(204, response=response, msg=msg)

    def assert_http_205_reset_content(self, response=None, msg=None):
        self._assert_http_status(205, response=response, msg=msg)

    def assert_http_206_partial_content(self, response=None, msg=None):
        self._assert_http_status(206, response=response, msg=msg)

    def assert_http_207_multi_status(self, response=None, msg=None):
        self._assert_http_status(207, response=response, msg=msg)

    def assert_http_208_already_reported(self, response=None, msg=None):
        self._assert_http_status(208, response=response, msg=msg)

    def assert_http_226_im_used(self, response=None, msg=None):
        self._assert_http_status(226, response=response, msg=msg)

    def assert_http_300_multiple_choices(self, response=None, msg=None):
        self._assert_http_status(300, response=response, msg=msg)

    def assert_http_301_moved_permanently(self, response=None, msg=None, url=None):
        self._assert_http_status(301, response=response, msg=msg, url=url)

    def assert_http_302_found(self, response=None, msg=None, url=None):
        self._assert_http_status(302, response=response, msg=msg, url=url)

    def assert_http_303_see_other(self, response=None, msg=None):
        self._assert_http_status(303, response=response, msg=msg)

    def assert_http_304_not_modified(self, response=None, msg=None):
        self._assert_http_status(304, response=response, msg=msg)

    def assert_http_305_use_proxy(self, response=None, msg=None):
        self._assert_http_status(305, response=response, msg=msg)

    def assert_http_306_reserved(self, response=None, msg=None):
        self._assert_http_status(306, response=response, msg=msg)

    def assert_http_307_temporary_redirect(self, response=None, msg=None):
        self._assert_http_status(307, response=response, msg=msg)

    def assert_http_308_permanent_redirect(self, response=None, msg=None):
        self._assert_http_status(308, response=response, msg=msg)

    def assert_http_400_bad_request(self, response=None, msg=None):
        self._assert_http_status(400, response=response, msg=msg)

    def assert_http_401_unauthorized(self, response=None, msg=None):
        self._assert_http_status(401, response=response, msg=msg)

    def assert_http_402_payment_required(self, response=None, msg=None):
        self._assert_http_status(402, response=response, msg=msg)

    def assert_http_403_forbidden(self, response=None, msg=None):
        self._assert_http_status(403, response=response, msg=msg)

    def assert_http_404_not_found(self, response=None, msg=None):
        self._assert_http_status(404, response=response, msg=msg)

    def assert_http_405_method_not_allowed(self, response=None, msg=None):
        self._assert_http_status(405, response=response, msg=msg)

    def assert_http_406_not_acceptable(self, response=None, msg=None):
        self._assert_http_status(406, response=response, msg=msg)

    def assert_http_407_proxy_authentication_required(self, response=None, msg=None):
        self._assert_http_status(407, response=response, msg=msg)

    def assert_http_408_request_timeout(self, response=None, msg=None):
        self._assert_http_status(408, response=response, msg=msg)

    def assert_http_409_conflict(self, response=None, msg=None):
        self._assert_http_status(409, response=response, msg=msg)

    def assert_http_410_gone(self, response=None, msg=None):
        self._assert_http_status(410, response=response, msg=msg)

    def assert_http_411_length_required(self, response=None, msg=None):
        self._assert_http_status(411, response=response, msg=msg)

    def assert_http_412_precondition_failed(self, response=None, msg=None):
        self._assert_http_status(412, response=response, msg=msg)

    def assert_http_413_request_entity_too_large(self, response=None, msg=None):
        self._assert_http_status(413, response=response, msg=msg)

    def assert_http_414_request_uri_too_long(self, response=None, msg=None):
        self._assert_http_status(414, response=response, msg=msg)

    def assert_http_415_unsupported_media_type(self, response=None, msg=None):
        self._assert_http_status(415, response=response, msg=msg)

    def assert_http_416_requested_range_not_satisfiable(self, response=None, msg=None):
        self._assert_http_status(416, response=response, msg=msg)

    def assert_http_417_expectation_failed(self, response=None, msg=None):
        self._assert_http_status(417, response=response, msg=msg)

    def assert_http_422_unprocessable_entity(self, response=None, msg=None):
        self._assert_http_status(422, response=response, msg=msg)

    def assert_http_423_locked(self, response=None, msg=None):
        self._assert_http_status(423, response=response, msg=msg)

    def assert_http_424_failed_dependency(self, response=None, msg=None):
        self._assert_http_status(424, response=response, msg=msg)

    def assert_http_426_upgrade_required(self, response=None, msg=None):
        self._assert_http_status(426, response=response, msg=msg)

    def assert_http_428_precondition_required(self, response=None, msg=None):
        self._assert_http_status(428, response=response, msg=msg)

    def assert_http_429_too_many_requests(self, response=None, msg=None):
        self._assert_http_status(429, response=response, msg=msg)

    def assert_http_431_request_header_fields_too_large(self, response=None, msg=None):
        self._assert_http_status(431, response=response, msg=msg)

    def assert_http_451_unavailable_for_legal_reasons(self, response=None, msg=None):
        self._assert_http_status(451, response=response, msg=msg)

    def assert_http_500_internal_server_error(self, response=None, msg=None):
        self._assert_http_status(500, response=response, msg=msg)

    def assert_http_501_not_implemented(self, response=None, msg=None):
        self._assert_http_status(501, response=response, msg=msg)

    def assert_http_502_bad_gateway(self, response=None, msg=None):
        self._assert_http_status(502, response=response, msg=msg)

    def assert_http_503_service_unavailable(self, response=None, msg=None):
        self._assert_http_status(503, response=response, msg=msg)

    def assert_http_504_gateway_timeout(self, response=None, msg=None):
        self._assert_http_status(504, response=response, msg=msg)

    def assert_http_505_http_version_not_supported(self, response=None, msg=None):
        self._assert_http_status(505, response=response, msg=msg)

    def assert_http_506_variant_also_negotiates(self, response=None, msg=None):
        self._assert_http_status(506, response=response, msg=msg)

    def assert_http_507_insufficient_storage(self, response=None, msg=None):
        self._assert_http_status(507, response=response, msg=msg)

    def assert_http_508_loop_detected(self, response=None, msg=None):
        self._assert_http_status(508, response=response, msg=msg)

    def assert_http_509_bandwidth_limit_exceeded(self, response=None, msg=None):
        self._assert_http_status(509, response=response, msg=msg)

    def assert_http_510_not_extended(self, response=None, msg=None):
        self._assert_http_status(510, response=response, msg=msg)

    def assert_http_511_network_authentication_required(self, response=None, msg=None):
        self._assert_http_status(511, response=response, msg=msg)
