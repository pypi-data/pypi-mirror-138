import typing as t

# Known configs. The SchemaCatalog lists known schema URLs with their names.
#
# Additional config could be associated with the schemas in the future.
SCHEMA_CATALOG: t.Dict[str, t.Dict[str, t.Any]] = {
    "github-workflows": {
        "url": "https://json.schemastore.org/github-workflow",
    },
    "github-actions": {
        "url": "https://json.schemastore.org/github-action",
    },
    "azure-pipelines": {
        "url": "https://raw.githubusercontent.com/microsoft/azure-pipelines-vscode/main/service-schema.json",  # noqa: E501
    },
    "travis": {
        "url": "https://json.schemastore.org/travis",
    },
    "readthedocs": {
        "url": "https://raw.githubusercontent.com/readthedocs/readthedocs.org/master/readthedocs/rtd_tests/fixtures/spec/v2/schema.json",  # noqa: E501
    },
    "renovate": {
        "url": "https://docs.renovatebot.com/renovate-schema.json",
    },
}
