Lazyaml  - PyYaml For Lazy People
======
A full-featured YAML processing framework for Python.

Original: [PyYaml](https://github.com/yaml/pyyaml)

Select loader automatically, that's all.

I am a lazy person, and I am willing to bear the price for it.


## Installation
```sh
pip install lazyaml
```

## Usage
```python
import yaml

yaml.load(stream)
yaml.dump(data)
```

If you don't trust the input YAML stream, you should use:

```python
yaml.safe_load(stream)
```


## Further Information

* For more information, check the
  [PyYAML homepage](https://github.com/yaml/pyyaml).

* [PyYAML tutorial and reference](http://pyyaml.org/wiki/PyYAMLDocumentation).

* Discuss PyYAML with the maintainers on
  Matrix at https://matrix.to/#/#pyyaml:yaml.io or
  IRC #pyyaml irc.libera.chat

* Submit bug reports and feature requests to the
  [PyYAML bug tracker](https://github.com/yaml/pyyaml/issues).

## License

The PyYAML module was written by Kirill Simonov <xi@resolvent.net>.
It is currently maintained by the YAML and Python communities.

PyYAML is released under the MIT license.

See the file LICENSE for more details.
