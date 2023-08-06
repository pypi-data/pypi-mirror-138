# ODD Collector SDK
##### Root project for ODD collectors

### Domain

* CollectorConfig
    Main model for collector

* Plugin
* AbstractAdapter


### How to use
The main class for using is Collector.

__Args__
config_path: str - path to collector_config.yaml ('/collector_config.yaml')
root_package: str - root package for adapters which will be loaded ('aws_collector.adapters')
plugins_union_type - needs to dynamicly create CollectorConfig model