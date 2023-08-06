Elixir flavored Erlang Binary Term Format for Python
====================================

Based on (https://github.com/okeuday/erlang_py)[https://github.com/okeuday/erlang_py] however forked in order to provide semetrical encoding / decoding `a == decode(encode(a))` Also converts None -> nil for better elixir compatibility

Provides all encoding and decoding for the Erlang Binary Term Format
(as defined at [http://erlang.org/doc/apps/erts/erl_ext_dist.html](http://erlang.org/doc/apps/erts/erl_ext_dist.html))
in a single Python module.

Available as a [Python package at `https://pypi.python.org/pypi/elixir_py/`](https://pypi.python.org/pypi/elixir_py/).

Tests
-----

    python setup.py test

Author
------

Michael Truog (mjtruog at protonmail dot com)
Kyle Hanson (me at khanson dot com)

License
-------

MIT License

