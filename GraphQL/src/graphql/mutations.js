/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const createLocation = /* GraphQL */ `
  mutation CreateLocation(
    $input: CreateLocationInput!
    $condition: ModelLocationConditionInput
  ) {
    createLocation(input: $input, condition: $condition) {
      id
      country
      location
      reportID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const updateLocation = /* GraphQL */ `
  mutation UpdateLocation(
    $input: UpdateLocationInput!
    $condition: ModelLocationConditionInput
  ) {
    updateLocation(input: $input, condition: $condition) {
      id
      country
      location
      reportID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const deleteLocation = /* GraphQL */ `
  mutation DeleteLocation(
    $input: DeleteLocationInput!
    $condition: ModelLocationConditionInput
  ) {
    deleteLocation(input: $input, condition: $condition) {
      id
      country
      location
      reportID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const createSyndrome = /* GraphQL */ `
  mutation CreateSyndrome(
    $input: CreateSyndromeInput!
    $condition: ModelSyndromeConditionInput
  ) {
    createSyndrome(input: $input, condition: $condition) {
      id
      name
      reportID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const updateSyndrome = /* GraphQL */ `
  mutation UpdateSyndrome(
    $input: UpdateSyndromeInput!
    $condition: ModelSyndromeConditionInput
  ) {
    updateSyndrome(input: $input, condition: $condition) {
      id
      name
      reportID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const deleteSyndrome = /* GraphQL */ `
  mutation DeleteSyndrome(
    $input: DeleteSyndromeInput!
    $condition: ModelSyndromeConditionInput
  ) {
    deleteSyndrome(input: $input, condition: $condition) {
      id
      name
      reportID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const createDisease = /* GraphQL */ `
  mutation CreateDisease(
    $input: CreateDiseaseInput!
    $condition: ModelDiseaseConditionInput
  ) {
    createDisease(input: $input, condition: $condition) {
      id
      name
      reportID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const updateDisease = /* GraphQL */ `
  mutation UpdateDisease(
    $input: UpdateDiseaseInput!
    $condition: ModelDiseaseConditionInput
  ) {
    updateDisease(input: $input, condition: $condition) {
      id
      name
      reportID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const deleteDisease = /* GraphQL */ `
  mutation DeleteDisease(
    $input: DeleteDiseaseInput!
    $condition: ModelDiseaseConditionInput
  ) {
    deleteDisease(input: $input, condition: $condition) {
      id
      name
      reportID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
    }
  }
`;
export const createReport = /* GraphQL */ `
  mutation CreateReport(
    $input: CreateReportInput!
    $condition: ModelReportConditionInput
  ) {
    createReport(input: $input, condition: $condition) {
      id
      event_date
      articleID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
      Locations {
        nextToken
        startedAt
      }
      Syndromes {
        nextToken
        startedAt
      }
      Diseases {
        nextToken
        startedAt
      }
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
      event_date
      articleID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
      Locations {
        nextToken
        startedAt
      }
      Syndromes {
        nextToken
        startedAt
      }
      Diseases {
        nextToken
        startedAt
      }
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
      event_date
      articleID
      _version
      _deleted
      _lastChangedAt
      createdAt
      updatedAt
      Locations {
        nextToken
        startedAt
      }
      Syndromes {
        nextToken
        startedAt
      }
      Diseases {
        nextToken
        startedAt
      }
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
