// @ts-check
import { initSchema } from '@aws-amplify/datastore';
import { schema } from './schema';



const { Location, Syndrome, Disease, Report, Article } = initSchema(schema);

export {
  Location,
  Syndrome,
  Disease,
  Report,
  Article
};