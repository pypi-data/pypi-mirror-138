## `test` directory structure

This test directory is structured by the class of test that is being run, as the class
of the test (unit, contract level, prop test, etc.) changes when and how you might want
to run these tests. It should be _extremely_ rare to add additional directories or files
at the top level.

### Current Classificiations

* `contract_level_test` are all tests that rely on a `network` fixture, with sub directories
  for various subtypes
* `microbench_test` is any test that performs a benchmark of our system, but without using a
  `network` fixture
* `prop_test` are property tests that do not rely on a `network` fixture
* `unit_test` are any conventional unit tests
* `testlib` is our directory of contracts used in tests
