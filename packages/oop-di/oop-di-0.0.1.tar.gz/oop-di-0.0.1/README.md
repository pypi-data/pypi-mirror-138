Intro
===

Dependency Injection is the key pattern used to implement Inversion of Control and Dependency Inversion principles 
(check D in SOLID).

It makes it simple to standardize the way objects are initialized in the application.

This package provides you with the set of components to automate dependency injection through the application.

Installation
===

`pip install oop-di`

Usage
===

To make it work do the following steps:

```python
# Init the `ContainerDefinition` component
container_definition = ContainerDefinition()
# fill the service definitions
container_definition.add_service(SomeService)
# compile the container
container = container_definition.compile()

# get an instance of the service from the container ...
service = container.get(SomeService)

# ... or inject it. Kwonly arguments will be injected
@container.inject()
def something(*, service: SomeService):
    ...

something()

# partial injection is also possible
def something_else(*, wont_inject: UnknownService, service: SomeService):
    ...

something_else(wont_inject=UnknownService())
```

Why not `python-dependency-injector`?
===

`python-dependency-injector` is the most popular Python DI library with a large community, excellent docs, and tons
of features that are not available in `oop-di`. Probably, `python-dependency-injector` is the best choice for you.
I've built this small library to handle the DI of my small experiments/pet projects.

What I don't like in `python-dependency-injector` and tried to mitigate in this library:

- it requires a name for every service. `oop-di` can use class itself as the name of the service;
- it makes you pollute your function's params with ` = Provide[Container.service]` defaults to inject something. 
`oop-di` just auto-wires the services by checking the parameter's types;
- `oop-di` has the tagging feature that can gather services into an array without an explicit definition of that array.


Check `examples/` folder for more info:

- `01-simple.py` - shows the basics: how to define services and how to inject the services somewhere.
- `02-extensions.py` - how to split the definitions between modules.
- `03-tags.py` - how to use tags to group services.