# Fluent stream
 
A stream abstraction with a fluent interface. Inspired by Java 8 streams, but a lot simpler and not lazy. 
It allows you to express something like: 

```python
Stream([1, 2, 3, 4, 5, 6, 7, 8, 9])\
    .filter(lambda x: x % 2 == 0)\
    .map(lambda x: x + 0.5)\
    .limit(4)\
    .fold(lambda x, y: x + y)
```