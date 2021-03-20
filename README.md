# SENG3011_A-GROUP-FOR-SENG3011

## Github repository structure

```bash
├── SENG3011_A-GROUP-FOR-SENG3011
│   ├── README.MD
│   ├── PHASE_1
│   │   ├── API_SourceCode
│   │   ├── API_Documentation
│   │   ├── TestScripts
│   ├── PHASE_2
│   │   ├── Application_SourceCode
│   │   ├── Application_Documentation
│   ├── Reports
│   │   ├── Management Information
│   │   ├── Design Details
│   │   ├── Testing Documentation
│   │   ├── Final Report
```

## API Documentation

* URL: http://amplify-outbreaknewstoday-doc.s3-website-ap-southeast-2.amazonaws.com/

### Graphdoc Documentation Generator

1. Install Graphdoc: `npm install -g @2fd/graphdoc`
2. Generate the documentation: `graphdoc -e <server url>/graphql -x "x-api-key: <API key>" -o <output path>`

## Prod API Endpoint

* URL: https://xjbexovx7fde7h6hfggtike5ey.appsync-api.ap-southeast-2.amazonaws.com/graphql
* Headers `x-api-key: da2-jzokeb4pi5bfnjgd3s5ihjemmq`

To interactively test the endpoint, use https://altair-gql.sirmuel.design/ setting the header in the left navigation bar.
