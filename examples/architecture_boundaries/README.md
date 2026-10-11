# Architecture-boundary checker — executable educational fixture

Run from repository root:

~~~bash
python scripts/check_architecture_boundaries.py \
  --root examples/architecture_boundaries \
  --config examples/architecture_boundaries/boundaries.json
python -m unittest discover -s tests -p 'test_architecture_boundaries.py' -v
~~~

Orders can depend on Billing's **public** application API but not
on Billing's private domain/persistence implementation. The rules
are explicit by package prefix. Tests add forbidden absolute and
relative imports in a temporary copy to verify violations fail.

**Limitations:** this is a conservative Python AST static-import
checker. It does not resolve dynamic imports, monkey patches,
runtime dependency injection, code generation or every alias
semantics. It is not a universal clean-architecture certifier.
Use architectural integration/contract tests and code review too.
