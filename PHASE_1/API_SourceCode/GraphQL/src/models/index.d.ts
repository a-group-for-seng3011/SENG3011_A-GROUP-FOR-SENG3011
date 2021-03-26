import { ModelInit, MutableModel, PersistentModelConstructor } from "@aws-amplify/datastore";





export declare class Article {
  readonly id: string;
  readonly url?: string;
  readonly date_of_publication?: string;
  readonly headline?: string;
  readonly main_text?: string;
  readonly Reports?: (Report | null)[];
  constructor(init: ModelInit<Article>);
  static copyOf(source: Article, mutator: (draft: MutableModel<Article>) => MutableModel<Article> | void): Article;
}

export declare class Report {
  readonly id: string;
  readonly event_date?: string;
  readonly Diseases?: (Disease | null)[];
  readonly Syndromes?: (Syndrome | null)[];
  readonly Locations?: (Location | null)[];
  readonly articleID?: string;
  constructor(init: ModelInit<Report>);
  static copyOf(source: Report, mutator: (draft: MutableModel<Report>) => MutableModel<Report> | void): Report;
}

export declare class Disease {
  readonly id: string;
  readonly name?: string;
  readonly reportID?: string;
  constructor(init: ModelInit<Disease>);
  static copyOf(source: Disease, mutator: (draft: MutableModel<Disease>) => MutableModel<Disease> | void): Disease;
}

export declare class Syndrome {
  readonly id: string;
  readonly name?: string;
  readonly reportID?: string;
  constructor(init: ModelInit<Syndrome>);
  static copyOf(source: Syndrome, mutator: (draft: MutableModel<Syndrome>) => MutableModel<Syndrome> | void): Syndrome;
}

export declare class Location {
  readonly id: string;
  readonly country?: string;
  readonly location?: string;
  readonly reportID?: string;
  constructor(init: ModelInit<Location>);
  static copyOf(source: Location, mutator: (draft: MutableModel<Location>) => MutableModel<Location> | void): Location;
}