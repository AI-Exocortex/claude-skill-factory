# Python Source References

## Official Repository

https://github.com/approvals/ApprovalTests.Python

## Key Source Files

- `approvaltests/approvals.py` - Core verify functions
- `approvaltests/scrubbers/` - Scrubber implementations
- `approvaltests/namer/namer_factory.py` - NamerFactory for parametrized tests
- `approvaltests/utilities/simple_logger.py` - SimpleLogger for log verification

## Python-Specific Features

- Multiple approvals per test via `NamerFactory.with_parameters()`
- Inline approvals via docstrings with `Options().inline()`
- Log output capture via `verify_logging()` and `SimpleLogger`
