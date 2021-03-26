let jsonResponse = pm.response.json();

pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Content-Type is present", function () {
    pm.response.to.have.header("Content-Type");
});

pm.test("Content-Type is JSON", function () {
    pm.response.to.be.json;
})

pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

pm.test("Response should be a parsable JSON", function() {
    pm.expect(jsonResponse).to.be.ok;
});

pm.test("Response body should be an object", function() {
    pm.expect(jsonResponse).to.be.an('object');
});

pm.test("url key is truthy", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        pm.expect(jsonData.data.listArticles.items[i].url).to.be.ok;
    }
});

pm.test("date_of_publication key is truthy", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        pm.expect(jsonData.data.listArticles.items[i].date_of_publication).to.be.ok;
    }
});

pm.test("headline key is truthy", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        pm.expect(jsonData.data.listArticles.items[i].headline).to.be.ok;
    }
});

pm.test("main_text key is truthy", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        pm.expect(jsonData.data.listArticles.items[i].main_text).to.be.ok;
    }
});

pm.test("Reports key is truthy", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        pm.expect(jsonData.data.listArticles.items[i].Reports).to.be.ok;
    }
});

pm.test("Diseases key is truthy", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        for(j=0; j<jsonData.data.listArticles.items[i].Reports.items.length; j++){
            pm.expect(jsonData.data.listArticles.items[i].Reports.items[j].Diseases).to.be.ok;
        }
    }
});

pm.test("Syndromes key is truthy", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        for(j=0; j<jsonData.data.listArticles.items[i].Reports.items.length; j++){
            pm.expect(jsonData.data.listArticles.items[i].Reports.items[j].Syndromes).to.be.ok;
        }
    }
});

pm.test("Locations key is truthy", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        for(j=0; j<jsonData.data.listArticles.items[i].Reports.items.length; j++){
            pm.expect(jsonData.data.listArticles.items[i].Reports.items[j].Locations).to.be.ok;
        }
    }
});

pm.test("url matches standard Regex", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        pm.expect(jsonData.data.listArticles.items[i].url).to.match(/^http:\/\/.*\/$/);
    }
});

pm.test("Response body should be in the correct format", function() {
    pm.expect(jsonResponse.data).to.be.a('object');
    pm.expect(jsonResponse.data.listArticles).to.be.a('object');
    pm.expect(jsonResponse.data.listArticles.items).to.be.a('array');
    pm.expect(jsonResponse.data.listArticles.items[0].url).to.be.a('string');
    pm.expect(jsonResponse.data.listArticles.items[0].date_of_publication).to.be.a('string');
    pm.expect(jsonResponse.data.listArticles.items[0].headline).to.be.a('string');
    pm.expect(jsonResponse.data.listArticles.items[0].main_text).to.be.a('string');
    pm.expect(jsonResponse.data.listArticles.items[0].Reports).to.be.a('object');
    pm.expect(jsonResponse.data.listArticles.items[0].Reports.items).to.be.a('array');
    pm.expect(jsonResponse.data.listArticles.items[0].Reports.items[0].Diseases).to.be.a('object');
    pm.expect(jsonResponse.data.listArticles.items[0].Reports.items[0].Syndromes).to.be.a('object');
    pm.expect(jsonResponse.data.listArticles.items[0].Reports.items[0].Locations).to.be.a('object');
});

pm.test("url link is valid", function () {
    let jsonData = pm.response.json();
    for(i=0; i<jsonData.data.listArticles.items.length; i++) {
        pm.sendRequest(jsonData.data.listArticles.items[i].url, (error,response) => 
        {
            if (error){
                console.log(error);
            }
            pm.test('response should be ok to process for the link', () => {
                pm.expect(error).to.equal(null);
                pm.expect(response).to.have.property('code', 200);
                pm.expect(response).to.have.property('status', 'OK');
            })
        
        });
    }
});
