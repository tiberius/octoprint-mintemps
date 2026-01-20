from setuptools import setup


plugin_identifier = "mintemps"
plugin_package = "octoprint_mintemps"
plugin_name = "OctoPrint-MinTemps"
plugin_version = "0.1.0"
plugin_description = (
    "Keep bed and hotend heaters at a minimum temperature after prints."
)
plugin_author = "OctoPrint-MinTemps contributors"
plugin_license = "AGPLv3"
plugin_requires = []


setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    license=plugin_license,
    packages=[plugin_package],
    include_package_data=True,
    package_data={plugin_package: ["templates/*.jinja2"]},
    install_requires=plugin_requires,
    entry_points={"octoprint.plugin": [f"{plugin_identifier} = {plugin_package}"]},
)
