# 3p
from nose.plugins.attrib import attr

# project
from tests.checks.common import AgentCheckTest


@attr(requires='powerdns_recursor')
class TestPowerDNSRecursorCheck(AgentCheckTest):
    CHECK_NAME = 'powerdns_recursor'

    GAUGE_METRICS_V3 = [
        'cache-entries',
        'concurrent-queries',
        'negcache-entries',
        'packetcache-entries',
    ]
    RATE_METRICS_V3 = [
        'all-outqueries',
        'answers-slow',
        'answers0-1',
        'answers1-10',
        'answers10-100',
        'answers100-1000',
        'cache-hits',
        'cache-misses',
        'dont-outqueries',
        'ipv6-outqueries',
        'ipv6-questions',
        'noerror-answers',
        'nxdomain-answers',
        'outgoing-timeouts',
        'over-capacity-drops',
        'packetcache-hits',
        'packetcache-misses',
        'questions',
        'servfail-answers',
        'tcp-client-overflow',
        'tcp-clients',
        'tcp-outqueries',
        'tcp-questions',
        'throttle-entries',
        'throttled-out',
        'throttled-outqueries',
        'unauthorized-tcp',
        'unauthorized-udp',
        'unexpected-packets',
    ]

    METRIC_FORMAT = 'powerdns.recursor.{}'

    def __init__(self, *args, **kwargs):
        AgentCheckTest.__init__(self, *args, **kwargs)
        self.config = {"instances": [{
            "host": "127.0.0.1",
            "port": "8082",
            "api_key": "pdns_api_key"
        },
        {
            "host": "127.0.0.1",
            "port": "8082",
            "api_key": "pdns_api_key",
            "version": 4
        }]}

    # Really a basic check to see if all metrics are there
    def test_check(self):
        self.run_check_twice(self.config)

        # Assert metrics v3
        for metric in self.GAUGE_METRICS_V3:
            self.assertMetric(self.METRIC_FORMAT.format(metric), tags=[])

        for metric in self.RATE_METRICS_V3:
            self.assertMetric(self.METRIC_FORMAT.format(metric), tags=[])

        # Assert metrics v4
        for metric in self.GAUGE_METRICS_V4:
            self.assertMetric(self.METRIC_FORMAT.format(metric), tags=[])

        for metric in self.RATE_METRICS_V4:
            self.assertMetric(self.METRIC_FORMAT.format(metric), tags=[])


        service_check_tags = ['recursor_host:127.0.0.1', 'recursor_port:8082']
        self.assertServiceCheckOK('powerdns.recursor.can_connect', tags=service_check_tags)

        self.coverage_report()

    def test_tags(self):
        config = self.config.copy()
        tags = ['foo:bar']
        config['instances'][0]['tags'] = ['foo:bar']
        self.run_check_twice(config)

        # Assert metrics v3
        for metric in self.GAUGE_METRICS_V3:
            self.assertMetric(self.METRIC_FORMAT.format(metric), tags=tags)

        for metric in self.RATE_METRICS_V3:
            self.assertMetric(self.METRIC_FORMAT.format(metric), tags=tags)

        # Assert metrics v4
        for metric in self.GAUGE_METRICS_V4:
            self.assertMetric(self.METRIC_FORMAT.format(metric), tags=tags)

        for metric in self.RATE_METRICS_V4:
            self.assertMetric(self.METRIC_FORMAT.format(metric), tags=tags)

        service_check_tags = ['recursor_host:127.0.0.1', 'recursor_port:8082']
        self.assertServiceCheckOK('powerdns.recursor.can_connect', tags=service_check_tags)

        self.coverage_report()

    def test_bad_config(self):
        config = self.config.copy()
        config['instances'][0]['port'] = 1111
        service_check_tags = ['recursor_host:127.0.0.1', 'recursor_port:1111']
        self.assertRaises(
            Exception,
            lambda: self.run_check(config)
        )
        self.assertServiceCheckCritical('powerdns.recursor.can_connect', tags=service_check_tags)
        self.coverage_report()

    def test_bad_api_key(self):
        config = self.config.copy()
        config['instances'][0]['api_key'] = 'nope'
        service_check_tags = ['recursor_host:127.0.0.1', 'recursor_port:8082']
        self.assertRaises(
            Exception,
            lambda: self.run_check(config)
        )
        self.assertServiceCheckCritical('powerdns.recursor.can_connect', tags=service_check_tags)
        self.coverage_report()

    def test_very_bad_config(self):
        for config in [{}, {"host": "localhost"}, {"port": 1000}, {"host": "localhost", "port": 1000}]:
            self.assertRaises(
                Exception,
                lambda: self.run_check({"instances": [config]})
            )
        self.coverage_report()
