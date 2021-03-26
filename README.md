# SENG3011_A-GROUP-FOR-SENG3011

## Github repository structure

```bash
├── SENG3011_A-GROUP-FOR-SENG3011
│   ├── README.MD
│   ├── PHASE_1
│   │   ├── API_SourceCode
│   │   │   ├── Scraper
│   │   │   ├── GraphQL
│   │   ├── API_Documentation
│   │   │   ├── GraphQL
│   │   │   ├── Sample_Log.csv
│   │   ├── Test_Scripts
│   ├── PHASE_2
│   │   ├── Application_SourceCode
│   │   ├── Application_Documentation
│   ├── Reports
│   │   ├── Management Information.pdf
│   │   ├── Design Details.pdf
│   │   ├── Testing Documentation.pdf
│   │   ├── Final Report.pdf
```

## API Documentation

* URL: <http://amplify-outbreaknewstoday-doc.s3-website-ap-southeast-2.amazonaws.com/>

### Graphdoc Documentation Generator

1. Install Graphdoc: `npm install -g @2fd/graphdoc`
2. Generate the documentation: `graphdoc -e <server url>/graphql -x "x-api-key: <API key>" -o <output path>`

## Prod API Endpoint

* URL: <https://xjbexovx7fde7h6hfggtike5ey.appsync-api.ap-southeast-2.amazonaws.com/graphql>
* Headers `x-api-key: da2-jzokeb4pi5bfnjgd3s5ihjemmq`

To interactively test the endpoint, use <https://altair-gql.sirmuel.design/> setting the header in the left navigation bar.

## Copying Staging to Prod Database

1. Install copy-dynamodb-table: `npm install copy-dynamodb-table`
2. Use the `Copy_Database.js` script under `PHASE_1/API_SourceCode/Copy_Database.js` from the npm documentation to copy the tables in this order due to foreign keys:
    1. Article
    2. Report
    3. Disease, Syndrome, Location
