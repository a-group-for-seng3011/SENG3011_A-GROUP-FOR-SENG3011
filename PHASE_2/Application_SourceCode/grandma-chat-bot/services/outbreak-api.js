"use strict";

// Imports dependencies
const axios = require("axios"),
    config = require("./config");

module.exports = class OutbreakAPI {

    // Set positional parameters to undefined for the default values
    constructor(start_date="2001-01-01T00:00:00",
        end_date="2020-12-31T23:59:59",
        keyterms,
        location) {
            this.start_date = start_date;
            this.end_date = end_date;
            this.keyterms = keyterms;
            this.location = location;
        }

    async getArticles() {
        const params = {
            start_date: this.start_date,
            end_date: this.end_date,
            keyterms: this.keyterms,
            location: this.location,
            token: config.outbreakToken
        }
        // Send the HTTP request to the Outbreak API
        try {
            const response = await axios.get(config.outbreakUrl, { params });
            // console.log(response.data.Reports);
            return response.data.Reports;
        } catch (error) {
            console.log(error);
            return "error!"
        }
    }

    async getSortedArticles() {
        const articles = await this.getArticles();

        return articles.sort((a, b) => Date.parse(b.date_of_publication) - Date.parse(a.date_of_publication));
    }
}
