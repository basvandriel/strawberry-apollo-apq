# strawberry-apollo-apq
Supporting [Apollo's automatic persisted queries](https://www.apollographql.com/docs/apollo-server/performance/apq/)
in [Strawberry GraphQL](https://github.com/strawberry-graphql/strawberry) 🍓

[![codecov](https://codecov.io/gh/basvandriel/strawberry-apollo-apq/branch/main/graph/badge.svg?token=9LERDLNBE5)](https://codecov.io/gh/basvandriel/strawberry-apollo-apq)

## Notes

- Don't use this for production yet, unless you know what you're doing.
- For persisting queries, a simple `TTLCache` is used. Will be changed later.
- Only flask views are supported for now.


## Benchmarks

|                          | min (ms) | max (ms) | average (ms) |
|--------------------------|----------|----------|--------------|
| no persisting, default   | 1.9934   | 99.0644  | 2.5739       |
| persistiging, not cached | 3.8509   | 211.6294 | 5.0793       |
| persisting, cached       | 1.8495   | 21.6539  | 2.1182       |

## License
The code in this library is licensed under MIT license. See the [LICENSE.md](LICENSE.md) file for more information.

