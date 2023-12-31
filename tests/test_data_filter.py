import unittest
import json

from data_filter import DataFilter


class ParseDataTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.languages = [
            "java",
            "groovy"
        ]
        super(ParseDataTestCase, self).__init__(*args, **kwargs)

    def test_filters_payload_to_expected_files_based_on_criteria(self):
        test_json = """
{
	"sha": "1e9b47b4c35f9046cec3718cadbc7410fdd9ffe1",
	"url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/trees/1e9b47b4c35f9046cec3718cadbc7410fdd9ffe1",
	"tree": [{
			"path": ".editorconfig",
			"mode": "100644",
			"type": "blob",
			"sha": "201ab30485cae46b70f9abe2c575fd7629114e04",
			"size": 33579,
			"url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/blobs/201ab30485cae46b70f9abe2c575fd7629114e04"
		},
		{
			"path": ".gitattributes",
			"mode": "100644",
			"type": "blob",
			"sha": "3982c9ad9a59f5608d66a3f8851f235e122e486e",
			"size": 92,
			"url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/blobs/3982c9ad9a59f5608d66a3f8851f235e122e486e"
		},
		{
			"path": ".githooks",
			"mode": "040000",
			"type": "tree",
			"sha": "d83d121e48b61cd9de2a7c78940cf88fc0c07c05",
			"url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/trees/d83d121e48b61cd9de2a7c78940cf88fc0c07c05"
		},
		{
			"path": "instrumentation/src/main/java/instrumentation/TestFailableCallable.java",
			"mode": "100644",
			"type": "blob",
			"sha": "7ce45826964d8da9d33d196de1265abff5aa28d2",
			"size": 268,
			"url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/blobs/7ce45826964d8da9d33d196de1265abff5aa28d2"
		},
		{
			"path": "instrumentation/src/main/java/instrumentation/TestInstrumentationModule.java",
			"mode": "100644",
			"type": "blob",
			"sha": "e4044ababaa7ff7bd635158f8d90ee5c3894ed21",
			"size": 1986,
			"url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/blobs/e4044ababaa7ff7bd635158f8d90ee5c3894ed21"
		},
		{
			"path": "instrumentation/internal/internal-class-loader/javaagent-integration-tests/src/main/resources",
			"mode": "040000",
			"type": "tree",
			"sha": "77f51c56d577df798aebb81e60b8a084f4412966",
			"url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/trees/77f51c56d577df798aebb81e60b8a084f4412966"
		},
		{
			"path": "instrumentation/internal/internal-class-loader/javaagent-integration-tests/src/main/resources/test-resources",
			"mode": "040000",
			"type": "tree",
			"sha": "b2ec26ccf707818532735ed86f6df72528443c56",
			"url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/trees/b2ec26ccf707818532735ed86f6df72528443c56"
		},
		{
			"path": "instrumentation/internal/internal-class-loader/javaagent-integration-tests/src/main/resources/test-resources/test-resource-2.txt",
			"mode": "100644",
			"type": "blob",
			"sha": "d6613f5f8b58eb6a88ee386ea140364c8645005c",
			"size": 12,
			"url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/blobs/d6613f5f8b58eb6a88ee386ea140364c8645005c"
		}
	]
}
        """
        data = json.loads(test_json)

        data_filter = DataFilter(languages=self.languages,
                                 path_prefix="instrumentation/", keyword="test")

        test = data_filter.parse_data(payload=data)

        expects = set()
        expects.add(
            "instrumentation/src/main/java/instrumentation/TestFailableCallable.java")
        expects.add(
            "instrumentation/src/main/java/instrumentation/TestInstrumentationModule.java")
        self.assertEqual(set(test['files']), expects)

    def test_given_url_with_different_case_than_keyword_still_filters_correctly(self):
        payload = """
        {
            "sha": "1e9b47b4c35f9046cec3718cadbc7410fdd9ffe1",
            "url": "https://api.github.com/repos/open-telemetry/opentelemetry-java-instrumentation/git/trees/1e9b47b4c35f9046cec3718cadbc7410fdd9ffe1",
            "tree": [
                {
                    "type": "blob",
                    "path": "instrumentation/src/main/java/instrumentation/TestFailableCallable.java"
                }
            ]
        }
        """
        data = json.loads(payload)

        data_filter = DataFilter(languages=self.languages,
                                 path_prefix="instrumentation/", keyword="test")

        test = data_filter.parse_data(payload=data)

        expects = [
            "instrumentation/src/main/java/instrumentation/TestFailableCallable.java"]
        self.assertEqual(expects, test['files'])
