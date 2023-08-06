# attribute
Attribute management made easy

## Installation
```console
pip install git+https://github.com/tombulled/attribute@main
```

## Usage
```python
>>> import attribute
>>>
>>> def foo(): pass
>>>
>>> name = attribute.Attribute('__name__')
>>>
>>> name.get(foo)
'foo'
```