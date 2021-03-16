/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const createReport = /* GraphQL */ `
  mutation CreateReport(
    $input: CreateReportInput!
    $condition: ModelReportConditionInput
  ) {
    createReport(input: $input, condition: $condition) {
      id
      disease
      syndrome
      event_date
      country
      location
      articleID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const updateReport = /* GraphQL */ `
  mutation UpdateReport(
    $input: UpdateReportInput!
    $condition: ModelReportConditionInput
  ) {
    updateReport(input: $input, condition: $condition) {
      id
      disease
      syndrome
      event_date
      country
      location
      articleID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const deleteReport = /* GraphQL */ `
  mutation DeleteReport(
    $input: DeleteReportInput!
    $condition: ModelReportConditionInput
  ) {
    deleteReport(input: $input, condition: $condition) {
      id
      disease
      syndrome
      event_date
      country
      location
      articleID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const createArticle = /* GraphQL */ `
  mutation CreateArticle(
    $input: CreateArticleInput!
    $condition: ModelArticleConditionInput
  ) {
    createArticle(input: $input, condition: $condition) {
      id
      url
      date_of_publication
      headline
      main_text
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
      Report {
        nextToken
        startedAt
      }
    }
  }
`;
export const updateArticle = /* GraphQL */ `
  mutation UpdateArticle(
    $input: UpdateArticleInput!
    $condition: ModelArticleConditionInput
  ) {
    updateArticle(input: $input, condition: $condition) {
      id
      url
      date_of_publication
      headline
      main_text
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
      Report {
        nextToken
        startedAt
      }
    }
  }
`;
export const deleteArticle = /* GraphQL */ `
  mutation DeleteArticle(
    $input: DeleteArticleInput!
    $condition: ModelArticleConditionInput
  ) {
    deleteArticle(input: $input, condition: $condition) {
      id
      url
      date_of_publication
      headline
      main_text
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
      Report {
        nextToken
        startedAt
      }
    }
  }
`;
