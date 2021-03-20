// @ts-check
import { initSchema } from '@aws-amplify/datastore';
import { schema } from './schema';



const { Article, Report, Disease, Syndrome, Location } = initSchema(schema);

export {
  Article,
  Report,
  Disease,
  Syndrome,
  Location
};