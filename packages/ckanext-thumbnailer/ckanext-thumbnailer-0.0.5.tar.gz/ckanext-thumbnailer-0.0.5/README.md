[![Tests](https://github.com//ckanext-thumbnailer/workflows/Tests/badge.svg?branch=main)](https://github.com//ckanext-thumbnailer/actions)

# ckanext-thumbnailer


## Requirements

Compatibility with core CKAN versions:

| CKAN version | Compatible? |
|--------------|-------------|
| 2.9          | yes         |
| master       | yes         |

## Installation

1. Install extension. It may fail because of missing system packages. Check
   [preview-generator](https://pypi.org/project/preview-generator/)
   documentation for details.

        pip install ckanext-thumbnailer

1. Add `files` and `thumbnailer` to the list of enabled plugins

        ckan.plugins = ... thumbnailer files

## Config settings

	# If greater than 0, make an attempt to download linked resource as long as it's side is under this limit
	# (optional, default: 0).
    ckanext.thumbnailer.max_remote_size = 0

	# List of formats that will get thumbnails when resource is created/updated
	# (optional, default: None).
    ckanext.thumbnailer.auto_formats = pdf png
