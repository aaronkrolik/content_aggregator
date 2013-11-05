content_aggregator
==================

plugin framework for aggregating various data sources.

The framework automatically loads all modules in the "plugins" package that extend Plugin (or really the plugin metaclass)
by intercepting module imports in the package __init__ . This is useful if many people will contribute plugins to the
framework, but you dont want to have to modify the plugin loader each time. The particular use case outlined here is 
a content aggregator where each plugin will pull data from a different onlne source. 
