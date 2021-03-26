var copy = require('copy-dynamodb-table').copy

var globalAWSConfig = { // AWS Configuration object http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Config.html#constructor-property
  accessKeyId: 'AKID',
  secretAccessKey: 'SECRET',
  region: 'ap-southeast-2'
}

copy({
    config: globalAWSConfig, // config for AWS
    source: {
      tableName: 'source_table_name', // required
    },
    destination: {
      tableName: 'destination_table_name', // required
    },
    log: true, // default false
    create : true // create destination table if not exist
  },
  function (err, result) {
    if (err) {
      console.log(err)
    }
    console.log(result)
  })