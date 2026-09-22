export async function onRequestGet({ env, request }) {
  const url = new URL(request.url)
  const pathParts = url.pathname.split('/')
  const id = pathParts[pathParts.length - 1]

  if (id && id !== 'corpus') {
    const result = await env.CORPUS_DB.prepare('SELECT * FROM corpus WHERE id = ?').bind(id).first()
    return result ? Response.json(result) : Response.json({ error: 'Not found' }, { status: 404 })
  }

  const results = await env.CORPUS_DB.prepare('SELECT * FROM corpus LIMIT 300').all()
  return Response.json(results.results || [])
}
