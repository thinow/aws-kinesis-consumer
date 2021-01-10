# 1.1.0 (2021-01-09)

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
