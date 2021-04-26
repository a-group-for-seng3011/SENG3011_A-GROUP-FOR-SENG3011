const express = require('express');
const bodyParser = require('body-parser');
const app = express();

const diseaseRoutes = require('./routes/diseases');

app.use(bodyParser.urlencoded({ extended: false }));

app.set('view engine', 'pug');
app.set('views', './views');

// GET endpoint
app.use('/', diseaseRoutes);
app.get('/', function(request, response, next) {
    next();
});


// app.post('/attributes/reset', (request, response) => {
//     const keyNames = Object.keys(request.body);

//     let attributes = {};
//     keyNames.forEach(keyName => {
//         attributes[keyName] = null;
//     });

//     response.json({ set_attributes: attributes });
// });

// Start the server and listen for incoming requests
const listener = app.listen(process.env.PORT, function() {
    console.log('Your app is listening on port ' + listener.address().port);
});
