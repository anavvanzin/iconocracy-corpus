import { z } from 'zod';

/**
 * Zod schema for the PostDataRequest model.
 * Defines the structure and validation rules for this data type.
 * This is the shape used in application code - what developers interact with.
 */
export const postDataRequest = z.lazy(() => {
  return z.object({
    name: z.string().optional().nullable(),
  });
});

/**
 *
 * @typedef  {PostDataRequest} postDataRequest
 * @property {string}
 */
export type PostDataRequest = z.infer<typeof postDataRequest>;

/**
 * Zod schema for mapping API responses to the PostDataRequest application shape.
 * Handles any property name transformations from the API schema.
 * If property names match the API schema exactly, this is identical to the application shape.
 */
export const postDataRequestResponse = z.lazy(() => {
  return z
    .object({
      name: z.string().optional().nullable(),
    })
    .transform((data) => ({
      name: data['name'],
    }));
});

/**
 * Zod schema for mapping the PostDataRequest application shape to API requests.
 * Handles any property name transformations required by the API schema.
 * If property names match the API schema exactly, this is identical to the application shape.
 */
export const postDataRequestRequest = z.lazy(() => {
  return z
    .object({
      name: z.string().optional().nullable(),
    })
    .transform((data) => ({
      name: data['name'],
    }));
});
