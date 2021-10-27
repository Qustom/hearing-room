// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');

// Set the region 
AWS.config.update({region: 'us-west-2'});

// Create the DynamoDB service object
var ddb = new AWS.DynamoDB();

//Get json file with people data.

//
//TODO: CHANGE BELOW TO GET FROM A JSON FILE!!
const jsonArr = [{id: 'name1', test: 'test1'},{id: "name2", test: 'test2'},{id: "name3", test: 'test3'}];
//
//

jsonArr.forEach((item)=>{

    //Convert object into DynamoDB type object
    var marshalledItem =  AWS.DynamoDB.Converter.marshall(item);
    console.log(marshalledItem);

    //Insert item into DynamoDB database
    var params = {
        TableName: 'hearingroom-people',
        Item: marshalledItem
    };

    // Call DynamoDB to add the item to the table
    ddb.putItem(params, function(err, data) {
        if (err) {
        console.log("Error", err);
        } else {
        console.log("Success", data);
        }
    });
});
