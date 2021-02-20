# 1.3.0 (2021-02-20)

1. **Added feature** : `-r / --region` argument to define the AWS region.
2. **Added feature** : prints progress when preparing the shards.
3. **Non-breaking change** : format of the logs going to stderr is changed (e.g. prefixed with `>`).
4. **Non-breaking change** : user-friendly error when the stream is not found.
5. **Non-breaking change** : user-friendly error when the AWS session token is expired.

# 1.2.0 (2021-01-18)

1. **Added feature** : all arguments can be defined with short names. Affects `-s / --stream-name`, `-e / --endpoint`,
   `-i / --iterator-type`, and `-v / --version`.
2. **Added feature** : `-m / --max-records-per-request` argument to define the maximum number of records per request
3. **Added feature** : Printed errors

* recognized errors are printed with an explanation and potential solution
* un-recognized errors are printed without stacktrace to simplify readability

# 1.1.1 (2021-01-10)

1. **Added feature** : The command `aws-kinesis-consumer` is usable from a docker container
   (see [Docker image thinow/aws-kinesis-consumer](https://hub.docker.com/r/thinow/aws-kinesis-consumer))
2. **Added feature** : Prints the version of the binary using the argument `--version`
3. **Dependency** : upgrade the AWS library `boto3` from `1.16.25` to `1.16.39`

# 1.0.1 (2020-12-12)

1. **Bug fix** : prints the correct number of records per shard

# 1.0.0 (2020-12-01)

1. **Added feature** : Consume a stream base on the name (e.g. `--stream-name` argument)
2. **Added feature** : Consume existing records or only the new records (e.g. `--iterator-type`)
3. **Added feature** : Ability to set a different endpoint url than the default AWS endpoint (e.g. `--endpoint`)
