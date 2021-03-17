/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const onCreateLocation = /* GraphQL */ `
  subscription OnCreateLocation {
    onCreateLocation {
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
export const onUpdateLocation = /* GraphQL */ `
  subscription OnUpdateLocation {
    onUpdateLocation {
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
export const onDeleteLocation = /* GraphQL */ `
  subscription OnDeleteLocation {
    onDeleteLocation {
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
export const onCreateSyndrome = /* GraphQL */ `
  subscription OnCreateSyndrome {
    onCreateSyndrome {
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
export const onUpdateSyndrome = /* GraphQL */ `
  subscription OnUpdateSyndrome {
    onUpdateSyndrome {
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
export const onDeleteSyndrome = /* GraphQL */ `
  subscription OnDeleteSyndrome {
    onDeleteSyndrome {
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
export const onCreateDisease = /* GraphQL */ `
  subscription OnCreateDisease {
    onCreateDisease {
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
export const onUpdateDisease = /* GraphQL */ `
  subscription OnUpdateDisease {
    onUpdateDisease {
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
export const onDeleteDisease = /* GraphQL */ `
  subscription OnDeleteDisease {
    onDeleteDisease {
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
export const onCreateReport = /* GraphQL */ `
  subscription OnCreateReport {
    onCreateReport {
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
export const onUpdateReport = /* GraphQL */ `
  subscription OnUpdateReport {
    onUpdateReport {
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
export const onDeleteReport = /* GraphQL */ `
  subscription OnDeleteReport {
    onDeleteReport {
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
export const onCreateArticle = /* GraphQL */ `
  subscription OnCreateArticle {
    onCreateArticle {
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
export const onUpdateArticle = /* GraphQL */ `
  subscription OnUpdateArticle {
    onUpdateArticle {
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
export const onDeleteArticle = /* GraphQL */ `
  subscription OnDeleteArticle {
    onDeleteArticle {
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
