'use strict';

const express = require('express');
const axios = require('axios');
const OutbreakAPI = require('../services/outbreak-api');

async function myfunc(start_date, end_date, keyterms, location) {
    const outbreakAPI = new OutbreakAPI(
        start_date,
        end_date,
        keyterms,
        location
    );
    const articles = await outbreakAPI.getArticles();
    return articles;
}
function removeDuplicates(data) {
    return data.filter((value, index) => data.indexOf(value) === index);
}
const router = express.Router();
router.get('/diseases', (request, response) => {
    const start_date = request.query.start_date;
    const end_date = request.query.end_date;
    const keyterms = request.query.keyterms;
    const location = request.query.location;
    if (keyterms === '') {
        keyterms = undefined;
    }
    if (location === '') {
        location = undefined;
    }
    const outbreakAPI = new OutbreakAPI(
        start_date,
        end_date,
        keyterms,
        location
    );
    const result = myfunc(start_date, end_date, keyterms, location);
    let url_list = [];
    let symptoms = [];
    result.then(function(res) {
        const sortedActivities = res.sort(
            (a, b) =>
                new Date(Date.parse(b.date_of_publication)) -
                new Date(Date.parse(a.date_of_publication))
        );
        console.log(sortedActivities);
        console.log(sortedActivities.length);
        for (var i = 0; i < sortedActivities.length; i++) {
            var r = sortedActivities[i].reports;
            for (var j = 0; j < r.length; j++) {
                if (r[j].syndromes.length !== 0) {
                    symptoms.push(r[j].syndromes);
                }
            }
            url_list.push(sortedActivities[i].url);
        }
        // var s1 = '';
        // if (url_list.length > 5) {
        //     s1 = url_list.slice(0, 5).join('\n');
        // } else {
        //     s1 = url_list.join('\n');
        // }
        var removeDup = removeDuplicates(symptoms);
        var s2 = removeDup.join(',');
        
        response.json({
            set_attributes: {
                urlLength: url_list.length,
                symptomsLength: symptoms.length,
                url1: (url_list[0] === undefined) ? "" :url_list[0],
                url2: (url_list[1] === undefined) ? "" :url_list[1],
                url3: (url_list[2] === undefined) ? "" :url_list[2],
                url4: (url_list[3] === undefined) ? "" :url_list[3],
                url5: (url_list[4] === undefined) ? "" :url_list[4],
                headline1: (sortedActivities[0] === undefined) ? "" : sortedActivities[0].headline,
                headline2: (sortedActivities[1] === undefined) ? "" : sortedActivities[1].headline,
                headline3: (sortedActivities[2] === undefined) ? "" : sortedActivities[2].headline,
                headline4: (sortedActivities[3] === undefined) ? "" : sortedActivities[3].headline,
                headline5: (sortedActivities[4] === undefined) ? "" : sortedActivities[4].headline,
                // main_text1: sortedActivities[0].main_text || '',
                // main_text2: sortedActivities[1].main_text || '',
                // main_text3: sortedActivities[2].main_text || '',
                // main_text4: sortedActivities[3].main_text || '',
                // main_text5: sortedActivities[4].main_text || '',

                // urls: s1,
                symptoms: s2,
            },
        });
    });
});

module.exports = router;
