// @ts-check
import { initSchema } from '@aws-amplify/datastore';
import { schema } from './schema';



const { Article, Blog, Post, Comment } = initSchema(schema);

export {
  Article,
  Blog,
  Post,
  Comment
};